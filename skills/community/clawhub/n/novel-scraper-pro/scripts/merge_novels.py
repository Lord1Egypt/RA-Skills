#!/usr/bin/env python3
"""
合并小说文件并检查完整性

用法:
    python3 merge_novels.py --book "书名"
    python3 merge_novels.py --book "书名" --range 1 100
"""

import re
import argparse
from pathlib import Path

NOVELS_DIR = Path.home() / ".openclaw" / "workspace" / "novels"


def extract_chapter_range(filename):
    """从文件名提取章节范围"""
    # 匹配 "第 X-Y 章" 格式（允许空格）
    match = re.search(r'第\s*(\d+)-(\d+)\s*章', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    
    # 匹配 "第 X 章" 格式（允许空格）
    match = re.search(r'第\s*(\d+)\s*章', filename)
    if match:
        ch = int(match.group(1))
        return ch, ch
    
    return None, None


def extract_chapters_from_file(filepath):
    """从文件提取所有章节号"""
    chapters = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # 匹配 "第 X 章" 格式（标题行，允许空格）
        for match in re.finditer(r'^第\s*(\d+)\s*章', content, re.MULTILINE):
            chapters.append(int(match.group(1)))
    return chapters


def parse_args():
    parser = argparse.ArgumentParser(description="合并小说文件并检查完整性")
    parser.add_argument("--book", "-b", required=True, help="书名")
    parser.add_argument("--range", "-r", nargs=2, type=int, metavar=("START", "END"),
                        help="合并范围（例：--range 1 100）")
    parser.add_argument("--output", "-o", help="输出文件名（可选）")
    return parser.parse_args()


def main():
    args = parse_args()
    book_name = args.book
    
    print("=" * 60)
    print("小说合并与完整性检查")
    print("=" * 60)
    
    # 获取所有小说文件
    files = list(NOVELS_DIR.glob(f"{book_name}_第*.txt"))
    
    # 排除已合并的大文件
    files = [f for f in files if not any(x in f.name for x in ["第 1-100", "第 101-200", "第 201-300"])]
    
    if not files:
        print("❌ 未找到小说文件")
        return
    
    print(f"\n找到 {len(files)} 个文件")
    
    # 提取章节范围
    file_ranges = []
    for f in files:
        start, end = extract_chapter_range(f.name)
        if start and end:
            file_ranges.append((start, end, f))
            print(f"  {f.name}: 第{start}-{end}章")
    
    # 按章节号排序
    file_ranges.sort(key=lambda x: x[0])
    
    # 检查章节连续性
    print("\n" + "=" * 60)
    print("章节连续性检查")
    print("=" * 60)
    
    all_chapters = set()
    
    for start, end, filepath in file_ranges:
        chapters = extract_chapters_from_file(filepath)
        all_chapters.update(chapters)
        print(f"  {filepath.name}: {len(chapters)}章 ({min(chapters)}-{max(chapters)})")
    
    # 找到最大章节号
    max_chapter = max(all_chapters) if all_chapters else 0
    
    # 检查缺失的章节
    missing_chapters = []
    for i in range(1, max_chapter + 1):
        if i not in all_chapters:
            missing_chapters.append(i)
    
    if missing_chapters:
        print(f"\n⚠️  发现 {len(missing_chapters)} 章缺失:")
        # 分组显示缺失章节
        ranges = []
        start = missing_chapters[0]
        end = start
        for ch in missing_chapters[1:]:
            if ch == end + 1:
                end = ch
            else:
                ranges.append((start, end))
                start = ch
                end = ch
        ranges.append((start, end))
        
        for start, end in ranges[:10]:
            if start == end:
                print(f"  第{start}章")
            else:
                print(f"  第{start}-{end}章 ({end-start+1}章)")
        if len(ranges) > 10:
            print(f"  ... 还有 {len(ranges)-10} 组缺失")
    else:
        print("\n✅ 章节连续，无缺失")
    
    # 合并文件
    print("\n" + "=" * 60)
    print("合并文件")
    print("=" * 60)
    
    # 确定合并范围
    if args.range:
        merge_ranges = [(args.range[0], args.range[1], args.output or f"第{args.range[0]}-{args.range[1]}章.txt")]
    else:
        merge_ranges = [
            (1, 100, "第 1-100 章.txt"),
            (101, 200, "第 101-200 章.txt"),
            (201, 300, "第 201-300 章.txt"),
        ]
    
    for start_target, end_target, output_name in merge_ranges:
        print(f"\n合并第{start_target}-{end_target}章...")
        
        merged_content = []
        chapters_found = set()
        
        for start, end, filepath in file_ranges:
            # 检查是否有重叠
            if start > end_target or end < start_target:
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 提取本文件中的章节
                file_chapters = extract_chapters_from_file(filepath)
                
                # 只保留目标范围内的章节
                for ch in file_chapters:
                    if start_target <= ch <= end_target:
                        chapters_found.add(ch)
                
                merged_content.append(content)
        
        if merged_content:
            output_file = NOVELS_DIR / f"{book_name}_{output_name}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(merged_content))
            
            print(f"  ✅ 保存到：{output_file}")
            print(f"  📖 包含 {len(chapters_found)} 章 (第{min(chapters_found)}-{max(chapters_found)}章)")
            
            # 检查该范围内是否有缺失
            expected_chapters = set(range(start_target, end_target + 1))
            missing_in_range = expected_chapters - chapters_found
            if missing_in_range:
                print(f"  ⚠️  该范围缺失 {len(missing_in_range)} 章：{sorted(missing_in_range)[:10]}...")
        else:
            print("  ❌ 无内容可合并")
    
    print("\n" + "=" * 60)
    print("合并完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
