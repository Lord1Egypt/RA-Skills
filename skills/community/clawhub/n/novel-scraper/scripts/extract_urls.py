#!/usr/bin/env python3
"""
按章节号范围提取 URL

用法:
  python3 extract_urls.py 301 400  # 提取第 301-400 章的 URL
  python3 extract_urls.py 1 50     # 提取第 1-50 章的 URL
"""

import json
import sys
from pathlib import Path

STATE_DIR = Path(__file__).parent.parent / "state"
CATALOG_FILE = STATE_DIR / "book_4_catalog.json"


def extract_urls(start_ch, end_ch):
    """提取指定章节范围的 URL"""
    if not CATALOG_FILE.exists():
        print(f"❌ 目录文件不存在：{CATALOG_FILE}", file=sys.stderr)
        sys.exit(1)
    
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 按章节号筛选（不是索引切片！）
    chapters = [c for c in data if start_ch <= int(c['number']) <= end_ch]
    
    if not chapters:
        print(f"❌ 未找到第{start_ch}-{end_ch}章的目录数据", file=sys.stderr)
        sys.exit(1)
    
    urls = [c['url'] for c in chapters]
    
    # 输出逗号分隔的 URL 列表
    print(','.join(urls))
    
    # 输出统计信息到 stderr
    print(f"\n# 章节范围：{chapters[0]['number']} → {chapters[-1]['number']}", file=sys.stderr)
    print(f"# 实际数量：{len(urls)}章", file=sys.stderr)
    
    # 检查缺失章节
    all_nums = set(int(c['number']) for c in data)
    missing = [i for i in range(start_ch, end_ch + 1) if i not in all_nums]
    if missing:
        print(f"# ⚠️ 缺失章节：{missing} (共{len(missing)}章)", file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"用法：{sys.argv[0]} <起始章节号> <结束章节号>", file=sys.stderr)
        print(f"示例：{sys.argv[0]} 301 400", file=sys.stderr)
        sys.exit(1)
    
    try:
        start_ch = int(sys.argv[1])
        end_ch = int(sys.argv[2])
        if start_ch > end_ch:
            raise ValueError("起始章节号不能大于结束章节号")
    except ValueError as e:
        print(f"❌ 参数错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    extract_urls(start_ch, end_ch)
