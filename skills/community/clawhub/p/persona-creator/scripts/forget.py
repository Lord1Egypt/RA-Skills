#!/usr/bin/env python3
"""
forget.py — 删除/重置用户风格档案（遗忘功能）
用法:
  python3 forget.py --user <昵称> [--persona-dir <目录>] [--reset]
  --reset: 仅重置为模板（不删除文件），保留文件名
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='删除或重置用户风格档案')
    parser.add_argument('--user', required=True, help='用户名/昵称')
    parser.add_argument('--persona-dir', default='persona', help='persona 目录')
    parser.add_argument('--reset', action='store_true', help='重置为空模板（而非删除文件）')
    args = parser.parse_args()

    persona_path = Path(args.persona_dir) / f"{args.user}.json"
    template_path = Path(args.persona_dir) / "yourself.json"

    if not persona_path.exists():
        print(f"INFO: {persona_path} 不存在，无需操作。")
        sys.exit(0)

    if args.reset:
        # 重置为模板
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
            template['user_id'] = args.user
            template['display_name'] = args.user
            template['created_at'] = None
            template['updated_at'] = None
            template['statistics'] = {"analyzed_messages": 0, "date_range": [None, None], "memory_files_scanned": []}
            with open(persona_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
            print(f"✅ 已重置 {args.user} 的风格档案（保留文件）")
        else:
            print(f"ERROR: 模板文件 {template_path} 不存在", file=sys.stderr)
            sys.exit(1)
    else:
        # 备份后删除
        backup_path = persona_path.with_suffix(f".bak.{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json")
        shutil.copy2(persona_path, backup_path)
        os.remove(persona_path)
        print(f"🗑️  已删除 {args.user} 的风格档案（备份: {backup_path.name}）")

    print(f"FORGOTTEN:true")
    print(f"USER:{args.user}")


if __name__ == '__main__':
    main()
