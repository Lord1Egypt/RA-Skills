#!/usr/bin/env python3
"""智能章节分割脚本 - 按章节将大文件分成多个小文件"""

import re
import os
import sys

def split_by_chapters(file_path, output_dir=None):
    """检测章节标题并分割文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 常见章节标题正则（第X章 / 第X卷 / 第X部）
    chapter_pattern = re.compile(
        r'^第[一二三四五六七八九十百千\d]+[章节卷部篇]\s*[：:]\s*.+$',
        re.MULTILINE
    )

    chapters = chapter_pattern.split(content)
    if len(chapters) <= 1:
        # 备选：简单按"第X章"分割
        chapter_pattern = re.compile(r'第[一二三四五六七八九十百千\d]+章')
        chapters = chapter_pattern.split(content)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = output_dir or os.path.dirname(file_path)

    for i, chapter_content in enumerate(chapters):
        if chapter_content.strip():
            output_path = os.path.join(output_dir, f"{base_name}_第{i+1}章.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(chapter_content.strip())
            print(f"OK: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chapter_split.py <novel.txt>")
        sys.exit(1)
    split_by_chapters(sys.argv[1])
