#!/usr/bin/env python3
"""
链接脚本解析器
解析嵌入式项目中的.ld链接脚本文件
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_linker_script(ld_path: str) -> Dict[str, Any]:
    """解析链接脚本"""
    result = {
        'memory_regions': [],
        'sections': [],
        'entry_point': '',
        'stack_size': None,
        'heap_size': None,
        'error': None
    }

    try:
        with open(ld_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 移除注释
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)

        # ENTRY point
        match = re.search(r'ENTRY\s*\(\s*(\w+)\s*\)', content)
        if match:
            result['entry_point'] = match.group(1)

        # MEMORY块
        memory_match = re.search(r'MEMORY\s*\{([^}]+)\}', content)
        if memory_match:
            memory_block = memory_match.group(1)
            # 解析每个内存区域
            for match in re.finditer(r'(\w+)\s*\((\w+)\)\s*:\s*ORIGIN\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*,\s*LENGTH\s*=\s*(0x[0-9a-fA-F]+|\d+[KM]?)', memory_block):
                region = {
                    'name': match.group(1),
                    'attrs': match.group(2),
                    'origin': match.group(3),
                    'length': match.group(4)
                }
                result['memory_regions'].append(region)

        # SECTIONS块
        sections_match = re.search(r'SECTIONS\s*\{(.+)\}', content, re.DOTALL)
        if sections_match:
            sections_block = sections_match.group(1)
            # 解析每个section
            for match in re.finditer(r'\.(\w+)\s+([^\{]*)\{([^}]*)\}', sections_block):
                section = {
                    'name': match.group(1),
                    'address': match.group(2).strip(),
                    'content': match.group(3).strip()[:100]  # 截断
                }
                result['sections'].append(section)

        # 常见的堆栈大小定义
        stack_patterns = [
            r'_Stack_Size\s*=\s*(0x[0-9a-fA-F]+|\d+)',
            r'STACK_SIZE\s*=\s*(0x[0-9a-fA-F]+|\d+)',
            r'__stack\s*=\s*(0x[0-9a-fA-F]+|\d+)',
        ]
        for pattern in stack_patterns:
            match = re.search(pattern, content)
            if match:
                result['stack_size'] = match.group(1)
                break

        heap_patterns = [
            r'_Heap_Size\s*=\s*(0x[0-9a-fA-F]+|\d+)',
            r'HEAP_SIZE\s*=\s*(0x[0-9a-fA-F]+|\d+)',
            r'__heap_size\s*=\s*(0x[0-9a-fA-F]+|\d+)',
        ]
        for pattern in heap_patterns:
            match = re.search(pattern, content)
            if match:
                result['heap_size'] = match.group(1)
                break

    except Exception as e:
        result['error'] = str(e)

    return result


def find_linker_scripts(target_dir: str) -> List[str]:
    """查找链接脚本"""
    ld_files = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'build', 'out', '.git', 'CMakeFiles'}]
        for f in files:
            if f.endswith('.ld') or f.endswith('.x'):
                ld_files.append(os.path.join(root, f))
    return ld_files


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    ld_files = find_linker_scripts(target_dir)

    if not ld_files:
        result = {'error': 'No linker scripts found'}
    else:
        result = {
            'files': ld_files,
            'parsed': {}
        }
        for ld in ld_files:
            name = os.path.basename(ld)
            result['parsed'][name] = parse_linker_script(ld)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()