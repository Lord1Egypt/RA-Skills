#!/usr/bin/env python3
"""
NAS System Monitor - 飞牛 NAS 系统监控
"""
import os
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path

class NASMonitor:
    def __init__(self):
        self.config = {
            'disk_warning': 80,
            'disk_critical': 90,
            'cpu_temp_warning': 70,
            'cpu_temp_critical': 85,
            'memory_warning': 85,
            'memory_critical': 95,
        }
        self.alerts = []
        
    def check_disk_usage(self):
        """检查磁盘使用率"""
        result = subprocess.run(['df', '-h'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 6:
                filesystem, size, used, available, percent, mount = parts[:6]
                usage = int(percent.rstrip('%'))
                
                if usage >= self.config['disk_critical']:
                    self._alert(f'🚨 磁盘紧急: {mount} 使用率 {usage}%')
                elif usage >= self.config['disk_warning']:
                    self._alert(f'⚠️ 磁盘警告: {mount} 使用率 {usage}%')
    
    def check_memory(self):
        """检查内存使用"""
        with open('/proc/meminfo') as f:
            meminfo = f.read()
        
        total = int(re.search(r'MemTotal:\s+(\d+)', meminfo).group(1))
        available = int(re.search(r'MemAvailable:\s+(\d+)', meminfo).group(1))
        usage = (total - available) / total * 100
        
        if usage >= self.config['memory_critical']:
            self._alert(f'🚨 内存紧急: 使用率 {usage:.1f}%')
        elif usage >= self.config['memory_warning']:
            self._alert(f'⚠️ 内存警告: 使用率 {usage:.1f}%')
    
    def check_cpu_temp(self):
        """检查 CPU 温度"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                temp = int(f.read()) / 1000
            
            if temp >= self.config['cpu_temp_critical']:
                self._alert(f'🚨 CPU温度紧急: {temp}°C')
            elif temp >= self.config['cpu_temp_warning']:
                self._alert(f'⚠️ CPU温度警告: {temp}°C')
        except:
            pass
    
    def _alert(self, message):
        """发送告警"""
        self.alerts.append({
            'time': datetime.now().isoformat(),
            'message': message
        })
        print(message)
    
    def run(self, interval=60):
        """持续监控"""
        print(f"NAS Monitor started (interval: {interval}s)")
        while True:
            self.alerts = []
            self.check_disk_usage()
            self.check_memory()
            self.check_cpu_temp()
            
            if self.alerts:
                self._send_notifications()
            
            time.sleep(interval)
    
    def _send_notifications(self):
        """发送通知到配置渠道"""
        # TODO: 实现飞书/Discord webhook
        pass

if __name__ == "__main__":
    import re
    monitor = NASMonitor()
    monitor.run()
