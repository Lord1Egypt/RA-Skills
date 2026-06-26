#!/usr/bin/env python3
"""
内核配置解析器
解析Linux内核 .config 和 defconfig 文件
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_kernel_config(config_path: str) -> Dict[str, Any]:
    """解析内核配置文件"""
    result = {
        'architecture': '',
        'kernel_version': '',
        'configs': {},
        'enabled_features': [],
        'disabled_features': [],
        'modules': [],
        'error': None
    }

    try:
        with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # CONFIG_XXX=y
            match = re.match(r'CONFIG_(\w+)=(y|m|".*"|\d+)', line)
            if match:
                key = match.group(1)
                value = match.group(2)

                if value == 'y':
                    result['configs'][key] = 'enabled'
                    result['enabled_features'].append(key)
                elif value == 'm':
                    result['configs'][key] = 'module'
                    result['modules'].append(key)
                else:
                    result['configs'][key] = value

        # 提取架构
        if 'ARM' in result['configs']:
            result['architecture'] = 'ARM'
        elif 'ARM64' in result['configs']:
            result['architecture'] = 'ARM64'
        elif 'X86' in result['configs']:
            result['architecture'] = 'x86'
        elif 'RISCV' in result['configs']:
            result['architecture'] = 'RISC-V'

        # 重要配置
        important_configs = [
            'PREEMPT', 'SMP', 'NR_CPUS', 'HZ',
            'MODULES', 'UEVENT_HELPER', 'DEVTMPFS',
            'PRINTK', 'EARLY_PRINTK', 'DEBUG_INFO',
        ]

        result['important'] = {}
        for cfg in important_configs:
            if cfg in result['configs']:
                result['important'][cfg] = result['configs'][cfg]

    except Exception as e:
        result['error'] = str(e)

    return result


def find_kernel_configs(target_dir: str) -> Dict[str, str]:
    """查找内核配置文件"""
    configs = {}

    search_paths = [
        ('.config', 'main_config'),
        ('defconfig', 'defconfig'),
    ]

    for path, ctype in search_paths:
        full_path = os.path.join(target_dir, path)
        if os.path.exists(full_path):
            configs[ctype] = full_path

    # 查找arch相关的defconfig
    for root, dirs, files in os.walk(target_dir):
        if 'arch' in root:
            for f in files:
                if f.endswith('defconfig'):
                    configs.setdefault('arch_defconfig', os.path.join(root, f))

    return configs


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    configs = find_kernel_configs(target_dir)

    if not configs:
        result = {'error': 'No kernel config files found'}
    else:
        result = {'configs_found': list(configs.keys())}
        for ctype, path in configs.items():
            result[ctype] = parse_kernel_config(path)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()