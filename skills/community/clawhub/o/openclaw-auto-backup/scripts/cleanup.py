#!/usr/bin/env python3
"""
Cleanup Backups Script
Usage: python3 cleanup.py [--keep 10] [--older-than 30d]
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta
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

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

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

def parse_days(days_str: str) -> int:
    match = re.match(r'(\d+)(d|days?)?', days_str.lower())
    return int(match.group(1)) if match else 0

def confirm_deletion(backups_to_delete: list):
    if not backups_to_delete:
        return False
    print(f"\n{Colors.YELLOW}⚠️  警告：以下备份将被永久删除！{Colors.NC}\n")
    for backup in backups_to_delete:
        age_days = (datetime.now() - backup['timestamp']).days
        print(f"  - {backup['name']} ({age_days}天前)")
    print()
    try:
        response = input(f"{Colors.YELLOW}确认删除？(y/N): {Colors.NC}").strip().lower()
        return response == 'y'
    except EOFError:
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description='清理旧备份')
    parser.add_argument('--keep', type=int, help='保留最近 N 个备份')
    parser.add_argument('--older-than', type=str, help='删除超过指定天数的备份 (如：30d)')
    parser.add_argument('--dry-run', action='store_true', help='仅显示，不实际删除')
    parser.add_argument('--no-confirm', action='store_true', help='跳过确认')
    args = parser.parse_args()
    
    print_header("🧹 清理备份")
    config = load_config()
    backup_dir = Path(config.get('backupDir', str(OPENCLAW_HOME / "backups")))
    
    if not backup_dir.exists():
        log_error(f"备份目录不存在：{backup_dir}")
        return
    
    backups = get_backups(backup_dir)
    
    if not backups:
        log_warning("没有找到备份")
        return
    
    log_info(f"找到 {len(backups)} 个备份")
    
    to_delete = []
    
    if args.keep:
        if args.keep >= len(backups):
            log_info(f"当前备份数量 ({len(backups)}) 不超过保留数量 ({args.keep})，无需清理")
            return
        to_delete = backups[args.keep:]
        log_info(f"将保留最近 {args.keep} 个备份，删除 {len(to_delete)} 个旧备份")
    
    elif args.older_than:
        days = parse_days(args.older_than)
        if days <= 0:
            log_error(f"无效的天数：{args.older_than}")
            return
        cutoff_date = datetime.now() - timedelta(days=days)
        to_delete = [b for b in backups if b['timestamp'] < cutoff_date]
        log_info(f"将删除 {days} 天前的备份，共 {len(to_delete)} 个")
    
    else:
        log_error("请指定 --keep 或 --older-than 参数")
        parser.print_help()
        return
    
    if not to_delete:
        log_info("没有需要清理的备份")
        return
    
    if not args.no_confirm:
        if not confirm_deletion(to_delete):
            log_warning("已取消清理")
            return
    
    deleted = 0
    freed_space = 0
    
    for backup in to_delete:
        if args.dry_run:
            log_info(f"[模拟] 删除：{backup['name']}")
            deleted += 1
        else:
            try:
                if backup['path'].is_file():
                    freed_space += backup['path'].stat().st_size
                    backup['path'].unlink()
                elif backup['path'].is_dir():
                    freed_space += sum(f.stat().st_size for f in backup['path'].rglob('*') if f.is_file())
                    shutil.rmtree(backup['path'])
                log_success(f"已删除：{backup['name']}")
                deleted += 1
            except Exception as e:
                log_error(f"删除失败 {backup['name']}: {e}")
    
    print_header("✅ 清理完成")
    print(f"删除备份：{Colors.BOLD}{deleted}{Colors.NC} 个")
    if freed_space > 0:
        freed_str = f"{freed_space / 1024:.2f} KB" if freed_space < 1024*1024 else f"{freed_space / (1024*1024):.2f} MB"
        print(f"释放空间：{Colors.BOLD}{freed_str}{Colors.NC}")

if __name__ == '__main__':
    main()
