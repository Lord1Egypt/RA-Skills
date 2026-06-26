#!/usr/bin/env python3
"""
File Naming - 生成标准化文件名
"""

import argparse
import re
from datetime import datetime


def sanitize_slug(text):
    """将文本转换为 kebab-case slug。"""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text


def generate_filename(requirement_id, slug, date_str=None, ext='md'):
    """生成标准化文件名：cr-{id}-{slug}-{date}.{ext}"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y%m%d')
    clean_slug = sanitize_slug(slug)
    return f"cr-{requirement_id}-{clean_slug}-{date_str}.{ext}"


def main():
    parser = argparse.ArgumentParser(description='Proflow File Naming')
    parser.add_argument('--id', required=True, help='需求ID')
    parser.add_argument('--slug', required=True, help='功能标识（英文或中文）')
    parser.add_argument('--date', help='日期，格式 YYYYMMDD，默认今天')
    parser.add_argument('--ext', default='md', help='文件扩展名')
    args = parser.parse_args()

    fname = generate_filename(args.id, args.slug, args.date, args.ext)
    print(fname)


if __name__ == '__main__':
    main()
