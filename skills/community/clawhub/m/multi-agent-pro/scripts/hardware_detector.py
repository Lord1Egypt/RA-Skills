#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硬件检测器 - 多Agent协作编排引擎 v3.0

功能：检测用户电脑硬件配置，自动推荐流水线参数
零第三方依赖，仅使用 Python 标准库（platform/os/ctypes）

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 仅读取系统信息，不做任何修改
2. 不收集任何个人数据或敏感信息
3. 检测结果仅用于本地参数推荐，不上传
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import platform
import os
import sys


def get_cpu_info():
    """获取 CPU 信息"""
    info = {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor() or '未知',
    }

    # CPU 核心数
    try:
        info['cpu_count'] = os.cpu_count() or 1
    except Exception:
        info['cpu_count'] = 1

    return info


def get_memory_info():
    """获取内存信息（仅使用标准库）"""
    mem_info = {'total_mb': 0, 'available_mb': 0}

    try:
        if platform.system() == 'Windows':
            # Windows: 使用 ctypes 调用 GlobalMemoryStatusEx
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            mem_info['total_mb'] = stat.ullTotalPhys // (1024 * 1024)
            mem_info['available_mb'] = stat.ullAvailPhys // (1024 * 1024)
        else:
            # Linux/macOS: 读取 /proc/meminfo
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal'):
                        mem_info['total_mb'] = int(line.split()[1]) // 1024
                    elif line.startswith('MemAvailable'):
                        mem_info['available_mb'] = int(line.split()[1]) // 1024
                    elif line.startswith('MemFree') and mem_info['available_mb'] == 0:
                        mem_info['available_mb'] = int(line.split()[1]) // 1024
    except Exception:
        pass

    return mem_info


def recommend_settings(cpu_info, mem_info):
    """根据硬件配置推荐流水线参数"""
    cpu_count = cpu_info.get('cpu_count', 1)
    total_mem = mem_info.get('total_mb', 0)

    # 推荐并发节点数
    if cpu_count >= 8:
        recommended_concurrency = min(cpu_count - 1, 8)
    elif cpu_count >= 4:
        recommended_concurrency = cpu_count
    else:
        recommended_concurrency = max(1, cpu_count)

    # 推荐文件大小限制
    if total_mem >= 8192:
        max_file_size = 50  # MB
    elif total_mem >= 4096:
        max_file_size = 20
    else:
        max_file_size = 10

    # 推荐超时时间
    if cpu_count >= 8 and total_mem >= 8192:
        default_timeout = 120
    elif cpu_count >= 4:
        default_timeout = 90
    else:
        default_timeout = 60

    # 性能等级
    if cpu_count >= 8 and total_mem >= 16384:
        performance_level = '高'
    elif cpu_count >= 4 and total_mem >= 4096:
        performance_level = '中'
    else:
        performance_level = '低'

    return {
        'recommended_concurrency': recommended_concurrency,
        'max_file_size_mb': max_file_size,
        'default_timeout': default_timeout,
        'performance_level': performance_level,
    }


def detect():
    """执行完整硬件检测并输出报告"""
    cpu_info = get_cpu_info()
    mem_info = get_memory_info()
    settings = recommend_settings(cpu_info, mem_info)

    print("=" * 60)
    print("  🖥️ 硬件检测报告")
    print("=" * 60)
    print(f"\n  操作系统：{cpu_info['platform']} {cpu_info['platform_version']}")
    print(f"  架构：{cpu_info['architecture']}")
    print(f"  处理器：{cpu_info['processor']}")
    print(f"  CPU 核心数：{cpu_info['cpu_count']} 核")
    print(f"  内存总量：{mem_info['total_mb']} MB ({mem_info['total_mb'] // 1024} GB)")
    print(f"  可用内存：{mem_info['available_mb']} MB ({mem_info['available_mb'] // 1024} GB)")

    print(f"\n  📊 性能等级：{settings['performance_level']}")
    print(f"\n  ⚙️ 推荐流水线参数：")
    print(f"     并发节点数：{settings['recommended_concurrency']} 个")
    print(f"     文件大小限制：{settings['max_file_size_mb']} MB")
    print(f"     默认超时：{settings['default_timeout']} 秒")

    print(f"\n  💡 建议：")
    if settings['performance_level'] == '高':
        print(f"     您的配置较高，可以流畅运行复杂流水线。")
    elif settings['performance_level'] == '中':
        print(f"     您的配置中等，建议控制并发节点数以保持流畅。")
    else:
        print(f"     您的配置较低，建议减少并发节点数和文件大小限制。")

    print("\n" + "=" * 60)

    return {
        'cpu': cpu_info,
        'memory': mem_info,
        'settings': settings,
    }


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print("硬件检测器 - 多Agent协作编排引擎 v3.0")
        print("=" * 50)
        print("用法：python hardware_detector.py")
        print("")
        print("功能：")
        print("  - 检测 CPU 核心数")
        print("  - 检测内存大小")
        print("  - 自动推荐流水线参数")
        print("")
        print("安全说明：")
        print("  - 仅读取系统信息，不做任何修改")
        print("  - 不收集个人数据")
        print("  - 结果仅用于本地参数推荐")
        sys.exit(0)

    detect()
