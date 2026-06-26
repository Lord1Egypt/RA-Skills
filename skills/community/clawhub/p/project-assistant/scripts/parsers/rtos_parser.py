#!/usr/bin/env python3
"""
RTOS配置解析器
解析FreeRTOS、Zephyr、RT-Thread配置
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional


def parse_freertos_config(config_path: str) -> Dict[str, Any]:
    """解析FreeRTOSConfig.h"""
    result = {
        'type': 'FreeRTOS',
        'config': {},
        'tasks': [],
        'error': None
    }

    try:
        with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 提取配置项
        configs = [
            ('configUSE_PREEMPTION', 'preemption'),
            ('configTICK_RATE_HZ', 'tick_rate'),
            ('configMAX_PRIORITIES', 'max_priorities'),
            ('configMINIMAL_STACK_SIZE', 'minimal_stack'),
            ('configTOTAL_HEAP_SIZE', 'total_heap'),
            ('configUSE_MUTEXES', 'use_mutexes'),
            ('configUSE_SEMAPHORES', 'use_semaphores'),
            ('configUSE_COUNTING_SEMAPHORES', 'use_counting_sem'),
            ('configUSE_QUEUE_SETS', 'use_queue_sets'),
            ('configUSE_RECURSIVE_MUTEXES', 'use_recursive_mutex'),
            ('configUSE_TIMERS', 'use_timers'),
            ('configTIMER_QUEUE_LENGTH', 'timer_queue_length'),
            ('configTIMER_TASK_PRIORITY', 'timer_task_priority'),
            ('configTIMER_TASK_STACK_DEPTH', 'timer_task_stack'),
        ]

        for macro, key in configs:
            match = re.search(rf'#define\s+{macro}\s+(\d+)', content)
            if match:
                result['config'][key] = int(match.group(1))

    except Exception as e:
        result['error'] = str(e)

    return result


def parse_zephyr_config(config_path: str) -> Dict[str, Any]:
    """解析Zephyr prj.conf"""
    result = {
        'type': 'Zephyr',
        'config': {},
        'error': None
    }

    try:
        with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            match = re.match(r'CONFIG_(\w+)=(y|n|\d+|".*?")', line)
            if match:
                result['config'][match.group(1)] = match.group(2)

    except Exception as e:
        result['error'] = str(e)

    return result


def find_rtos_config(target_dir: str) -> Optional[Dict[str, Any]]:
    """查找并解析RTOS配置"""

    # FreeRTOS
    freertos_paths = [
        'FreeRTOSConfig.h',
        'include/FreeRTOSConfig.h',
        'config/FreeRTOSConfig.h',
    ]
    for path in freertos_paths:
        full_path = os.path.join(target_dir, path)
        if os.path.exists(full_path):
            return parse_freertos_config(full_path)

    # Zephyr
    zephyr_paths = [
        'prj.conf',
        'boards/prj.conf',
    ]
    for path in zephyr_paths:
        full_path = os.path.join(target_dir, path)
        if os.path.exists(full_path):
            return parse_zephyr_config(full_path)

    # 搜索
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'.git', 'build', 'out', 'CMakeFiles'}]
        for f in files:
            if f == 'FreeRTOSConfig.h':
                return parse_freertos_config(os.path.join(root, f))
            if f == 'prj.conf' and 'zephyr' in root.lower():
                return parse_zephyr_config(os.path.join(root, f))

    return None


def main():
    if len(sys.argv) < 2:
        target_dir = os.getcwd()
    else:
        target_dir = sys.argv[1]

    result = find_rtos_config(target_dir)

    if not result:
        result = {'error': 'No RTOS config found'}

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()