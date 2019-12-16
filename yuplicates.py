#!/usr/bin/env python

import os
import yaml
import argparse
import collections

from jinja2 import Environment, meta

# variables = []
# maybe_vars = []


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

bl = ["name"]

def parse_vars_from_file(file):
    vars = []
    with open(file, "r") as stream:
        try:
            y = yaml.safe_load(stream)
            if y is not None:
                # not an empty file or commented out
                for v in y:
                    if isinstance(v, collections.Mapping):
                        for key in v:
                            if key not in bl:
                                #print v[key]
                                #vars.append(v[key])
                                # use jinja to find out variables
                                env = Environment()
                                ast = env.parse(v[key])
                                var = meta.find_undeclared_variables(ast)
                                if len(var) > 0:
                                   print var
        except yaml.YAMLError as exc:
            raise
        return vars


def anydup(thelist):
    seen = set()
    for x in thelist:
        if x in seen:
            return True
        seen.add(x)
    return False


def read_var_files(yaml_dir):
    """
    Read and parse variables from all files.
    """
    vars = []
    for folder, subfolders, files in os.walk(yaml_dir):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                file_path = os.path.join(os.path.abspath(folder), file)
                vars = vars + parse_vars_from_file(file_path)
    return vars


def var_from_dict(d):
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some yaml shit")
    # 2 directories - variables, tasks/playbooks
    parser.add_argument("directory", type=dir_path, nargs=2, help="directories")
    args = parser.parse_args()
    d_args = vars(parser.parse_args())
    variables = read_var_files(d_args["directory"][0])
    roles = read_var_files(d_args["directory"][1])
    # are there any duplicities?
    if len(variables) != len(set(variables)):
        # retrieve the duplicates.
        s = set()
        duplicates = set(x for x in variables if x in s or s.add(x))
        #print "Possible duplicities: ", duplicates
    # for v in roles:
    #     # iterate over dict
    #     if isinstance(v, collections.Mapping):
    #         for key in v:
    #             print v[key]
    #     else:
    #         print "hovno"
    #
