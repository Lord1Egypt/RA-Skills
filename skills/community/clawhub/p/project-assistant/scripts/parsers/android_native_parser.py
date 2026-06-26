#!/usr/bin/env python3
"""
Android NDK Native项目解析器
解析Android.mk, Application.mk, CMakeLists.txt
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_android_mk(mk_path: str) -> Dict[str, Any]:
    """解析Android.mk"""
    result = {
        'local_path': '',
        'local_module': '',
        'local_src_files': [],
        'local_cflags': [],
        'local_ldlibs': [],
        'local_static_libraries': [],
        'local_shared_libraries': [],
        'local_c_includes': [],
        'error': None
    }

    try:
        with open(mk_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # LOCAL_PATH
        match = re.search(r'LOCAL_PATH\s*:=\s*(\S+)', content)
        if match:
            result['local_path'] = match.group(1)

        # LOCAL_MODULE
        match = re.search(r'LOCAL_MODULE\s*:=\s*(\S+)', content)
        if match:
            result['local_module'] = match.group(1)

        # LOCAL_SRC_FILES
        match = re.search(r'LOCAL_SRC_FILES\s*:=\s*(.+?)(?:\n\S|\n\n|$)', content, re.DOTALL)
        if match:
            files = match.group(1).strip()
            result['local_src_files'] = files.split()

        # LOCAL_CFLAGS
        match = re.search(r'LOCAL_CFLAGS\s*:=\s*(.+?)(?:\n\S|\n\n|$)', content, re.DOTALL)
        if match:
            flags = match.group(1).strip()
            result['local_cflags'] = flags.split()

        # LOCAL_LDLIBS
        match = re.search(r'LOCAL_LDLIBS\s*:=\s*(.+?)(?:\n\S|\n\n|$)', content, re.DOTALL)
        if match:
            libs = match.group(1).strip()
            result['local_ldlibs'] = [l for l in libs.split() if l.startswith('-l')]

        # LOCAL_STATIC_LIBRARIES
        match = re.search(r'LOCAL_STATIC_LIBRARIES\s*:=\s*(.+?)(?:\n\S|\n\n|$)', content, re.DOTALL)
        if match:
            result['local_static_libraries'] = match.group(1).strip().split()

        # LOCAL_SHARED_LIBRARIES
        match = re.search(r'LOCAL_SHARED_LIBRARIES\s*:=\s*(.+?)(?:\n\S|\n\n|$)', content, re.DOTALL)
        if match:
            result['local_shared_libraries'] = match.group(1).strip().split()

    except Exception as e:
        result['error'] = str(e)

    return result


def parse_application_mk(mk_path: str) -> Dict[str, Any]:
    """解析Application.mk"""
    result = {
        'app_platform': '',
        'app_abi': [],
        'app_stl': '',
        'app_cppflags': [],
        'error': None
    }

    try:
        with open(mk_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # APP_PLATFORM
        match = re.search(r'APP_PLATFORM\s*:=\s*(\S+)', content)
        if match:
            result['app_platform'] = match.group(1)

        # APP_ABI
        match = re.search(r'APP_ABI\s*:=\s*(.+?)(?:\n\S|\n\n|$)', content, re.DOTALL)
        if match:
            abis = match.group(1).strip()
            result['app_abi'] = abis.split()

        # APP_STL
        match = re.search(r'APP_STL\s*:=\s*(\S+)', content)
        if match:
            result['app_stl'] = match.group(1)

    except Exception as e:
        result['error'] = str(e)

    return result


def find_native_files(target_dir: str) -> Dict[str, List[str]]:
    """查找Native相关文件"""
    files = {
        'android_mk': [],
        'application_mk': [],
        'cmake_lists': [],
        'jni_sources': []
    }

    for root, dirs, filenames in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'.git', 'build', '.gradle'}]

        for f in filenames:
            full_path = os.path.join(root, f)

            if f == 'Android.mk':
                files['android_mk'].append(full_path)
            elif f == 'Application.mk':
                files['application_mk'].append(full_path)
            elif f == 'CMakeLists.txt' and ('jni' in root or 'native' in root):
                files['cmake_lists'].append(full_path)
            elif f.endswith('.cpp') or f.endswith('.c'):
                if 'jni' in root:
                    files['jni_sources'].append(full_path)

    return files


def find_jni_functions(target_dir: str) -> List[Dict[str, str]]:
    """查找JNI函数"""
    jni_functions = []

    for root, dirs, filenames in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'.git', 'build', '.gradle'}]

        for f in filenames:
            if not (f.endswith('.cpp') or f.endswith('.c')):
                continue

            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()

                # JNI_OnLoad
                if 'JNI_OnLoad' in content:
                    jni_functions.append({
                        'file': os.path.join(root, f),
                        'function': 'JNI_OnLoad'
                    })

                # Java_开头的函数
                for match in re.finditer(r'(Java_\w+)', content):
                    jni_functions.append({
                        'file': os.path.join(root, f),
                        'function': match.group(1)
                    })

            except:
                continue

    return jni_functions


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    files = find_native_files(target_dir)

    result = {
        'files_found': files,
        'android_mk': [],
        'application_mk': None,
        'jni_functions': find_jni_functions(target_dir)
    }

    for amk in files['android_mk']:
        result['android_mk'].append(parse_android_mk(amk))

    if files['application_mk']:
        result['application_mk'] = parse_application_mk(files['application_mk'][0])

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()