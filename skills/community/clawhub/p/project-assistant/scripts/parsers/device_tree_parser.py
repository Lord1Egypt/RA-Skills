#!/usr/bin/env python3
"""
设备树解析器
解析DTS/DTSI设备树文件
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_device_tree(dts_path: str) -> Dict[str, Any]:
    """解析设备树文件"""
    result = {
        'compatible': [],
        'model': '',
        'cpus': [],
        'memory': {},
        'peripherals': [],
        'error': None
    }

    try:
        with open(dts_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # compatible
        match = re.search(r'compatible\s*=\s*"([^"]+)"', content)
        if match:
            result['compatible'] = [match.group(1)]

        # 多个compatible
        for match in re.finditer(r'compatible\s*=\s*"([^"]+)"', content):
            if match.group(1) not in result['compatible']:
                result['compatible'].append(match.group(1))

        # model
        match = re.search(r'model\s*=\s*"([^"]+)"', content)
        if match:
            result['model'] = match.group(1)

        # memory
        match = re.search(r'memory@([0-9a-fA-F]+)\s*\{[^}]*reg\s*=\s*<([^>]+)>', content, re.DOTALL)
        if match:
            result['memory'] = {
                'address': match.group(1),
                'reg': match.group(2).strip()
            }

        # cpus
        for match in re.finditer(r'cpu\d+[^{]*\{[^}]*device_type\s*=\s*"cpu"[^}]*}', content, re.DOTALL):
            cpu_block = match.group(0)
            cpu_info = {}
            m = re.search(r'compatible\s*=\s*"([^"]+)"', cpu_block)
            if m:
                cpu_info['compatible'] = m.group(1)
            m = re.search(r'clock-frequency\s*=\s*<([^>]+)>', cpu_block)
            if m:
                cpu_info['clock'] = m.group(1)
            if cpu_info:
                result['cpus'].append(cpu_info)

        # 简单外设检测
        peripheral_patterns = {
            'uart': r'uart@\w+|serial@\w+',
            'i2c': r'i2c@\w+|i2c\d+',
            'spi': r'spi@\w+|spi\d+',
            'gpio': r'gpio@\w+|gpio\d+',
            'ethernet': r'ethernet@\w+|mac@\w+',
            'usb': r'usb@\w+|usb\d+',
            'mmc': r'mmc@\w+|sdhci@\w+',
            'can': r'can@\w+',
            'pwm': r'pwm@\w+',
            'adc': r'adc@\w+',
        }

        for ptype, pattern in peripheral_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                result['peripherals'].append(ptype)

    except Exception as e:
        result['error'] = str(e)

    return result


def find_device_tree_files(target_dir: str) -> List[str]:
    """查找设备树文件"""
    dts_files = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'.git', 'build', 'out'}]
        for f in files:
            if f.endswith('.dts') or f.endswith('.dtsi'):
                dts_files.append(os.path.join(root, f))
    return dts_files


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    dts_files = find_device_tree_files(target_dir)

    if not dts_files:
        result = {'error': 'No device tree files found'}
    else:
        # 解析找到的第一个主DTS文件
        main_dts = None
        for f in dts_files:
            if f.endswith('.dts'):
                main_dts = f
                break
        if not main_dts:
            main_dts = dts_files[0]
        result = parse_device_tree(main_dts)
        result['files'] = dts_files

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()