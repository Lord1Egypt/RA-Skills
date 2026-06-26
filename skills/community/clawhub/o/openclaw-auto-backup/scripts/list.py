#!/usr/bin/env python3
"""
List Backups Script
Usage: python3 list.py
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "../config/backup-config.json"
OPENCLAW_HOME = Path.home() / ".openclaw"

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^50}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*50}{Colors.NC}\n")

def load_config():
    if not CONFIG_FILE.exists():
        return {"backupDir": str(OPENCLAW_HOME / "backups")}
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_backups(backup_dir: Path):
    if not backup_dir.exists():
        return []
    backups = []
    for item in backup_dir.iterdir():
        if item.name.startswith('backup-'):
            try:
                match = re.match(r'backup-(\d{8}-\d{6})(?:\.tar\.gz)?', item.name)
                if match:
                    timestamp_str = match.group(1)
                    timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
                    backups.append({"name": item.name, "path": item, "timestamp": timestamp})
            except:
                pass
    backups.sort(key=lambda x: x['timestamp'], reverse=True)
    return backups

def format_time(iso_string: str):
    try:
        dt = datetime.fromisoformat(iso_string)
        diff = datetime.now() - dt
        if diff.days > 0:
            return f"{diff.days}天前"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}小时前"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}分钟前"
        else:
            return f"{diff.seconds}秒前"
    except:
        return "未知"

def main():
    print_header("📦 备份列表")
    config = load_config()
    backup_dir = Path(config.get('backupDir', str(OPENCLAW_HOME / "backups")))
    
    if not backup_dir.exists():
        print(f"{Colors.YELLOW}备份目录不存在：{backup_dir}{Colors.NC}")
        return
    
    backups = get_backups(backup_dir)
    
    if not backups:
        print(f"{Colors.YELLOW}没有找到备份{Colors.NC}")
        return
    
    print(f"{Colors.BOLD}备份目录:{Colors.NC} {backup_dir}")
    print(f"{Colors.BOLD}备份数量:{Colors.NC} {len(backups)} 个\n")
    
    for idx, backup in enumerate(backups, 1):
        marker = f"{Colors.GREEN}← 最新{Colors.NC}" if idx == 1 else ""
        print(f"{Colors.BOLD}{idx}. {backup['name']}{Colors.NC} {marker}")
        print(f"   时间：{Colors.CYAN}{backup['timestamp'].isoformat()}{Colors.NC} ({Colors.YELLOW}{format_time(backup['timestamp'].isoformat())}{Colors.NC})")
        print()
    
    print(f"{Colors.BOLD}提示:{Colors.NC}")
    print(f"   恢复备份：python3 restore.py --version <备份名称>")
    print(f"   清理备份：python3 cleanup.py --keep 10")

if __name__ == '__main__':
    main()
