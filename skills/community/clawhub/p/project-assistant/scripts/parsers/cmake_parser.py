#!/usr/bin/env python3
"""
CMakeLists.txt 解析器
解析CMake项目配置
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_cmake(cmake_path: str) -> Dict[str, Any]:
    """解析CMakeLists.txt"""
    result = {
        'project_name': '',
        'project_version': '',
        'cmake_minimum_required': '',
        'languages': [],
        'dependencies': [],
        'targets': [],
        'options': [],
        'subdirectories': [],
        'error': None
    }

    try:
        with open(cmake_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 移除注释
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)

        # cmake_minimum_required
        match = re.search(r'cmake_minimum_required\s*\(\s*VERSION\s+([0-9.]+)', content, re.IGNORECASE)
        if match:
            result['cmake_minimum_required'] = match.group(1)

        # project
        match = re.search(r'project\s*\(\s*(\w+)(?:\s+VERSION\s+([0-9.]+))?(?:\s+LANGUAGES\s+([^)]+))?', content, re.IGNORECASE)
        if match:
            result['project_name'] = match.group(1)
            if match.group(2):
                result['project_version'] = match.group(2)
            if match.group(3):
                result['languages'] = [l.strip() for l in match.group(3).split()]

        # find_package
        for match in re.finditer(r'find_package\s*\(\s*(\w+)', content, re.IGNORECASE):
            result['dependencies'].append({
                'name': match.group(1),
                'type': 'find_package'
            })

        # FetchContent
        for match in re.finditer(r'FetchContent_Declare\s*\(\s*(\w+)', content, re.IGNORECASE):
            result['dependencies'].append({
                'name': match.group(1),
                'type': 'fetch_content'
            })

        # add_executable
        for match in re.finditer(r'add_executable\s*\(\s*(\w+)', content, re.IGNORECASE):
            result['targets'].append({
                'name': match.group(1),
                'type': 'executable'
            })

        # add_library
        for match in re.finditer(r'add_library\s*\(\s*(\w+)', content, re.IGNORECASE):
            result['targets'].append({
                'name': match.group(1),
                'type': 'library'
            })

        # option
        for match in re.finditer(r'option\s*\(\s*(\w+)\s+"([^"]*)"', content, re.IGNORECASE):
            result['options'].append({
                'name': match.group(1),
                'description': match.group(2)
            })

        # add_subdirectory
        for match in re.finditer(r'add_subdirectory\s*\(\s*([^)\s]+)', content, re.IGNORECASE):
            result['subdirectories'].append(match.group(1))

    except Exception as e:
        result['error'] = str(e)

    return result


def find_cmake_files(target_dir: str) -> List[str]:
    """查找所有CMakeLists.txt"""
    cmake_files = []
    for root, dirs, files in os.walk(target_dir):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in {'build', 'out', 'CMakeFiles', '_deps', '.git'}]
        if 'CMakeLists.txt' in files:
            cmake_files.append(os.path.join(root, 'CMakeLists.txt'))
    return cmake_files


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    cmake_files = find_cmake_files(target_dir)

    if not cmake_files:
        result = {'error': 'CMakeLists.txt not found'}
    else:
        # 解析根目录的CMakeLists.txt
        root_cmake = cmake_files[0]
        result = parse_cmake(root_cmake)
        result['all_cmake_files'] = cmake_files

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()