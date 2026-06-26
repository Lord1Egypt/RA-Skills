#!/usr/bin/env python3
"""
backup.py — PassManager 自动备份脚本

用法:
  python3 backup.py                  # 默认备份到配置目录
  python3 backup.py --output /path   # 自定义备份路径
  python3 backup.py --daily          # 每日备份模式（带日期命名）
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.passmanager import PassManager


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PassManager 自动备份")
    parser.add_argument("--output", "-o", help="备份文件路径")
    parser.add_argument("--daily", action="store_true", help="每日备份模式")

    args = parser.parse_args()

    pm = PassManager()
    output = args.output

    if args.daily and not output:
        from datetime import datetime
        output = os.path.join(pm.backup_dir, f"daily_{datetime.now().strftime('%Y%m%d')}.db")

    path = pm.backup(output)
    if path:
        size = os.path.getsize(path) / 1024
        print(f"✅ 备份成功: {path} ({size:.1f} KB)")
    else:
        print("❌ 备份失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
