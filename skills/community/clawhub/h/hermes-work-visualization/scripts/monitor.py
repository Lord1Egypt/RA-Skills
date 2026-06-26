#!/usr/bin/env python3
"""
实时工作监控
Real-time work monitoring
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path
from threading import Thread
import signal
import sys

# 添加技能路径以便导入 i18n_helper
SKILL_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_PATH))

try:
    from i18n_helper import get_i18n
    i18n = get_i18n(SKILL_PATH)
except ImportError:
    # Fallback if i18n not available
    class SimpleI18N:
        def get(self, key, default=None, **kwargs):
            return default or key
        def t(self, key, default=None, **kwargs):
            return default or key
        def get_language(self):
            return os.environ.get('HERMES_LANG', os.environ.get('LANG', 'en'))[:2]
    i18n = SimpleI18N()

# 配置路径
CONFIG_PATH = Path.home() / '.hermes/skills/work-visualization/config.json'
MONITOR_LOG = Path.home() / '.hermes/skills/work-visualization/cache/monitor.log'

# Language-specific strings
STRINGS = {
    'zh': {
        'monitor_started': '🔍 工作监控已启动',
        'log_file': '📝 日志文件',
        'press_ctrl_c': '按 Ctrl+C 停止监控',
        'stopped_signal': '\n收到停止信号，正在停止监控...',
        'monitor_stopped': '已停止',
        'processes': '个监控进程',
        'no_running': '没有运行中的监控进程',
        'stop_failed': '停止监控失败',
        'status_running': '✅ 监控正在运行',
        'status_not_running': '❌ 监控未运行',
        'status_check_failed': '检查状态失败',
        'monitor_start': '监控启动，间隔',
        'seconds': '秒',
        'monitor_stop': '监控停止',
        'disk_free': '磁盘剩余',
        'monitoring': '工作实时监控',
        'actions': '操作: start/stop/status',
        'monitor_interval': '监控间隔',
        'error': '错误'
    },
    'en': {
        'monitor_started': '🔍 Work monitoring started',
        'log_file': '📝 Log file',
        'press_ctrl_c': 'Press Ctrl+C to stop monitoring',
        'stopped_signal': '\nReceived stop signal, stopping monitor...',
        'monitor_stopped': 'Stopped',
        'processes': 'monitoring processes',
        'no_running': 'No running monitoring processes',
        'stop_failed': 'Failed to stop monitoring',
        'status_running': '✅ Monitoring is running',
        'status_not_running': '❌ Monitoring is not running',
        'status_check_failed': 'Failed to check status',
        'monitor_start': 'Monitor started, interval',
        'seconds': 'seconds',
        'monitor_stop': 'Monitor stopped',
        'disk_free': 'Disk free',
        'monitoring': 'Real-time Work Monitoring',
        'actions': 'Action: start/stop/status',
        'monitor_interval': 'Monitor interval',
        'error': 'Error'
    }
}

def get_str(key, lang=None):
    """Get localized string"""
    if lang is None:
        lang = i18n.get_language()
    return STRINGS.get(lang, STRINGS['en']).get(key, key)

class WorkMonitor:
    def __init__(self):
        self.running = False
        self.config = self.load_config()
        self.log_file = open(MONITOR_LOG, 'a')

    def load_config(self):
        """加载配置 / Load configuration"""
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "monitoring": {
                    "enabled": True,
                    "interval_seconds": 60
                }
            }

    def log_event(self, event_type, details):
        """记录事件 / Log event"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {event_type}: {details}\n"
        self.log_file.write(log_entry)
        self.log_file.flush()

    def check_system_status(self):
        """检查系统状态 / Check system status"""
        # 检查磁盘空间
        try:
            disk = os.statvfs(Path.home())
            free_space = (disk.f_frsize * disk.f_bavail) / (1024 ** 3)  # GB
        except:
            free_space = 0

        # 检查内存（简化版）
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                mem_total = int([line for line in meminfo.split('\n') if 'MemTotal' in line][0].split()[1]) // 1024  # MB
        except:
            mem_total = 0

        return {
            "disk_free_gb": round(free_space, 2),
            "mem_total_mb": mem_total,
        }

    def monitor_loop(self):
        """监控循环 / Monitor loop"""
        lang = i18n.get_language()
        start_str = get_str('monitor_start', lang)
        seconds = get_str('seconds', lang)
        stop_str = get_str('monitor_stop', lang)
        disk_free = get_str('disk_free', lang)
        error = get_str('error', lang)

        interval = self.config.get('monitoring', {}).get('interval_seconds', 60)

        self.log_event("MONITOR_START", f"{start_str} {interval} {seconds}")

        while self.running:
            try:
                status = self.check_system_status()
                self.log_event("STATUS_CHECK", f"{disk_free} {status['disk_free_gb']}GB")

                time.sleep(interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log_event(error, str(e))
                time.sleep(5)

        self.log_event("MONITOR_STOP", stop_str)
        self.log_file.close()

def start_monitor():
    """启动监控 / Start monitoring"""
    lang = i18n.get_language()
    started = get_str('monitor_started', lang)
    log = get_str('log_file', lang)
    ctrl_c = get_str('press_ctrl_c', lang)
    stopped = get_str('stopped_signal', lang)

    monitor = WorkMonitor()
    monitor.running = True

    # 设置信号处理
    def signal_handler(sig, frame):
        print(stopped)
        monitor.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print(f"{started}")
    print(f"{log}: {MONITOR_LOG}")
    print(f"{ctrl_c}\n")

    monitor.monitor_loop()

def stop_monitor():
    """停止监控 / Stop monitoring"""
    lang = i18n.get_language()
    stopped = get_str('monitor_stopped', lang)
    processes = get_str('processes', lang)
    no_running = get_str('no_running', lang)
    failed = get_str('stop_failed', lang)

    # 查找并终止监控进程
    import subprocess
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'work-visualization.*monitor.py'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', pid])
            print(f"{stopped} {len(pids)} {processes}")
        else:
            print(no_running)
    except Exception as e:
        print(f"{failed}: {e}")

def show_monitor_status():
    """显示监控状态 / Show monitor status"""
    lang = i18n.get_language()
    running = get_str('status_running', lang)
    not_running = get_str('status_not_running', lang)
    log = get_str('log_file', lang)
    failed = get_str('status_check_failed', lang)

    import subprocess
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'work-visualization.*monitor.py'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"{running} ({len(pids)} processes)" if lang == 'en' else f"{running} ({len(pids)} 个进程)")
            print(f"{log}: {MONITOR_LOG}")
        else:
            print(not_running)
    except Exception as e:
        print(f"{failed}: {e}")

def main():
    """主函数 / Main function"""
    import argparse

    lang = os.environ.get('HERMES_LANG', os.environ.get('LANG', 'en'))[:2]
    title = get_str('monitoring', lang)
    actions = get_str('actions', lang)

    parser = argparse.ArgumentParser(description=title)
    parser.add_argument('action', choices=['start', 'stop', 'status'], help=actions)

    args = parser.parse_args()

    if args.action == 'start':
        start_monitor()
    elif args.action == 'stop':
        stop_monitor()
    elif args.action == 'status':
        show_monitor_status()

if __name__ == "__main__":
    main()
