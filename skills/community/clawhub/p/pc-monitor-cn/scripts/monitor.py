#!/usr/bin/env python3
"""
系统监控脚本 - 监控 CPU、内存、磁盘、网络状态
"""

import psutil
import shutil
from datetime import datetime

def get_cpu_usage():
    """获取 CPU 使用率"""
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """获取内存使用情况"""
    mem = psutil.virtual_memory()
    return {
        'total': round(mem.total / (1024 ** 3), 2),  # GB
        'used': round(mem.used / (1024 ** 3), 2),    # GB
        'available': round(mem.available / (1024 ** 3), 2),  # GB
        'percent': mem.percent
    }

def get_disk_usage():
    """获取磁盘使用情况"""
    disk = shutil.disk_usage('/')
    return {
        'total': round(disk.total / (1024 ** 3), 2),  # GB
        'used': round(disk.used / (1024 ** 3), 2),    # GB
        'free': round(disk.free / (1024 ** 3), 2),    # GB
        'percent': round((disk.used / disk.total) * 100, 2)
    }

def get_network_info():
    """获取网络信息"""
    net_io = psutil.net_io_counters()
    return {
        'bytes_sent': round(net_io.bytes_sent / (1024 ** 2), 2),  # MB
        'bytes_recv': round(net_io.bytes_recv / (1024 ** 2), 2),  # MB
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv
    }

def get_temperature():
    """获取传感器温度（如果可用）"""
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    if 'cpu' in entry.label.lower() or 'core' in entry.label.lower():
                        return f"{entry.current}°C"
            # 如果没有找到 CPU 温度，返回第一个温度
            for name, entries in temps.items():
                for entry in entries:
                    return f"{entry.current}°C"
    except (AttributeError, KeyError):
        pass
    return "N/A"

def format_report():
    """格式化监控报告"""
    memory = get_memory_usage()
    disk = get_disk_usage()
    network = get_network_info()
    
    report = f"""
{'='*50}
  系统监控报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

🔸 CPU 使用率：{get_cpu_usage()}%
🔸 CPU 温度：{get_temperature()}

🔸 内存使用：{memory['used']}GB / {memory['total']}GB ({memory['percent']}%)
   可用内存：{memory['available']}GB

🔸 磁盘使用：{disk['used']}GB / {disk['total']}GB ({disk['percent']}%)
   可用空间：{disk['free']}GB

🔸 网络流量:
   发送：{network['bytes_sent']}MB ({network['packets_sent']} 包)
   接收：{network['bytes_recv']}MB ({network['packets_recv']} 包)

{'='*50}
"""
    return report

def get_status_json():
    """获取 JSON 格式的状态（用于程序调用）"""
    memory = get_memory_usage()
    disk = get_disk_usage()
    network = get_network_info()
    
    return {
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': get_cpu_usage(),
        'cpu_temp': get_temperature(),
        'memory': memory,
        'disk': disk,
        'network': network
    }

if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(get_status_json(), indent=2))
    else:
        print(format_report())
