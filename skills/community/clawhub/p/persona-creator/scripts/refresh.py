#!/usr/bin/env python3
"""
refresh.py — 增量刷新 persona/$user.json
用法:
  python3 refresh.py --user <昵称> --memory-dir <memory目录> [--persona-dir <目录>] [--force]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='增量刷新用户风格档案')
    parser.add_argument('--user', required=True, help='用户名/昵称')
    parser.add_argument('--memory-dir', default='memory', help='memory 目录')
    parser.add_argument('--persona-dir', default='persona', help='persona 目录')
    parser.add_argument('--force', action='store_true', help='强制刷新（忽略上次更新时间）')
    parser.add_argument('--days', type=int, default=7, help='多少天内有新消息才触发刷新（默认7天）')
    args = parser.parse_args()

    persona_path = Path(args.persona_dir) / f"{args.user}.json"

    # 检查档案是否存在
    if not persona_path.exists():
        print(f"ERROR: 未找到 {persona_path}，请先运行 analyze.py 创建档案", file=sys.stderr)
        sys.exit(1)

    with open(persona_path, 'r', encoding='utf-8') as f:
        persona = json.load(f)

    last_updated = persona.get('updated_at')
    if last_updated and not args.force:
        last_dt = datetime.fromisoformat(last_updated.rstrip('Z'))
        now = datetime.utcnow()
        delta = (now - last_dt).days
        if delta < args.days:
            print(f"INFO: 档案在 {delta} 天前已更新（阈值 {args.days} 天），跳过刷新。使用 --force 强制刷新。")
            print(f"SKIP:true")
            sys.exit(0)

    # 查找新增的 memory 文件
    scanned = set(persona.get('statistics', {}).get('memory_files_scanned', []))
    memory_dir = Path(args.memory_dir)
    all_files = sorted(memory_dir.glob("*.md")) if memory_dir.exists() else []
    new_files = [f for f in all_files if f.name not in scanned]

    if not new_files and not args.force:
        print(f"INFO: 没有新的 memory 文件，无需刷新。")
        print(f"SKIP:true")
        sys.exit(0)

    print(f"🔄 发现 {len(new_files)} 个新 memory 文件，准备增量刷新...")
    print(f"NEW_FILES:{','.join(f.name for f in new_files)}")
    print(f"REFRESH_NEEDED:true")
    print(f"USER:{args.user}")
    print(f"MEMORY_DIR:{args.memory_dir}")
    print(f"PERSONA_DIR:{args.persona_dir}")


if __name__ == '__main__':
    main()
