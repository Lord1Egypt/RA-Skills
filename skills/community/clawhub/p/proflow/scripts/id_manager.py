#!/usr/bin/env python3
"""
ID Manager - 扫描文档、生成唯一需求ID、支持自定义ID
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

ID_PATTERN = re.compile(r'cr-(\d+)-')


def find_existing_ids(docs_path, prefix='cr-'):
    """扫描 docs 目录下所有 prefix 开头的文件，提取已有 ID 集合。"""
    ids = set()
    docs_dir = Path(docs_path)
    if not docs_dir.exists():
        return ids

    for root, _, files in os.walk(docs_dir):
        for fname in files:
            if fname.startswith(prefix):
                match = ID_PATTERN.match(fname)
                if match:
                    ids.add(int(match.group(1)))
    return ids


def generate_unique_id(docs_path='./docs', custom_id=None):
    """生成或校验唯一需求ID。

    规则：
    - 用户显式指定了 custom_id：仅校验唯一性，无大小限制
    - 自动生成 ID：使用当前时间的 hhmmss（6位数字），若已存在则递增直到唯一
    """
    existing = find_existing_ids(docs_path)

    if custom_id is not None:
        cid = int(custom_id)
        if cid in existing:
            print(f"ERROR: 自定义ID {cid} 已存在，请更换。", file=sys.stderr)
            sys.exit(1)
        return cid

    # 自动生成：基于当前时间 hhmmss
    base_id = int(datetime.now().strftime('%H%M%S'))
    new_id = base_id
    while new_id in existing:
        new_id += 1
    return new_id


def main():
    parser = argparse.ArgumentParser(description='Proflow ID Manager')
    parser.add_argument('--path', default='./docs', help='文档扫描路径')
    parser.add_argument('--prefix', default='cr-', help='文件名前缀')
    parser.add_argument('--id', type=int, dest='custom_id', help='自定义ID')
    args = parser.parse_args()

    existing = find_existing_ids(args.path, args.prefix)
    new_id = generate_unique_id(args.path, args.custom_id)

    print(f"EXISTING_IDS={' '.join(str(i) for i in sorted(existing))}")
    print(f"NEW_ID={new_id}")


if __name__ == '__main__':
    main()
