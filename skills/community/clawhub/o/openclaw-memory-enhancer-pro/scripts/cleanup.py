#!/usr/bin/env python3
"""
Memory Enhancer - Memory Cleanup
记忆清理脚本

Usage: python3 cleanup.py --days 30

功能：清理过期记忆文件（可选：先压缩再删除）
"""

import argparse
import re
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def ensure_daily_memory():
    """确保今日记忆文件存在"""
    today = datetime.now().strftime('%Y-%m-%d')
    today_file = MEMORY_DIR / f"{today}.md"
    
    if not today_file.exists():
        today_file.parent.mkdir(parents=True, exist_ok=True)
        content = f"""# Daily Memory - {today}

## 日期
{datetime.now().strftime('%Y 年 %m 月 %d 日 %A')}

## 主要工作

[待填写]

## 系统状态

[待填写]

---
*最后更新：{today}*
"""
        today_file.write_text(content, encoding='utf-8')
        log_success(f"已创建今日记忆文件：{today_file.name}")
        return True
    else:
        log_info(f"今日记忆文件已存在：{today_file.name}")
        return False

def cleanup_memory(days: int = 30, dry_run: bool = False):
    """清理过期记忆文件
    
    Args:
        days: 保留最近多少天的记忆
        dry_run: 模拟运行，不实际删除
    """
    print(f"🧹 Memory Cleaner - 记忆清理工具")
    print("=" * 50)
    
    # 确保今日记忆文件存在
    ensure_daily_memory()
    
    if not MEMORY_DIR.exists():
        log_warning("记忆目录不存在")
        return
    
    cutoff_date = datetime.now() - timedelta(days=days)
    log_info(f"清理 {days} 天前的记忆文件")
    log_info(f"截止日期：{cutoff_date.strftime('%Y-%m-%d')}")
    
    if dry_run:
        log_warning("[模拟运行] 不会实际删除文件\n")
    
    deleted = 0
    kept = 0
    total_size = 0
    
    for md_file in sorted(MEMORY_DIR.glob("*.md")):
        # 从文件名提取日期
        match = re.match(r'(\d{4}-\d{2}-\d{2})\.md', md_file.name)
        if not match:
            continue
        
        file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
        file_size = md_file.stat().st_size
        
        if file_date < cutoff_date:
            # 过期文件
            if dry_run:
                log_info(f"将删除：{md_file.name} ({file_size/1024:.1f} KB)")
            else:
                md_file.unlink()
                log_success(f"已删除：{md_file.name}")
            deleted += 1
            total_size += file_size
        else:
            kept += 1
    
    print(f"\n{'='*50}")
    print(f"清理完成：")
    print(f"  - 保留：{kept} 个文件")
    print(f"  - 删除：{deleted} 个文件")
    print(f"  - 释放空间：{total_size/1024:.1f} KB")
    
    if dry_run:
        log_warning("\n以上是模拟运行，实际未删除任何文件")
        log_info("添加 --execute 参数执行实际删除")

def main():
    parser = argparse.ArgumentParser(description='记忆清理工具')
    parser.add_argument('--days', type=int, default=30, help='保留最近多少天的记忆（默认 30）')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际删除')
    parser.add_argument('--execute', action='store_true', help='执行实际删除（与 --dry-run 互斥）')
    
    args = parser.parse_args()
    
    dry_run = args.dry_run or not args.execute
    
    if args.execute and args.dry_run:
        log_error("--execute 和 --dry-run 不能同时使用")
        return
    
    cleanup_memory(args.days, dry_run)

if __name__ == "__main__":
    main()
