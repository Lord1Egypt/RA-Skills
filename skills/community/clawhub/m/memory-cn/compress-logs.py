#!/usr/bin/env python3
"""
压缩膨胀的 memory 日志文件。
保留: section 标题、完成项、关键发现、踩坑记录、部署信息
删除: 调试过程、中间步骤、大段代码、重复内容

用法: python3 compress-logs.py /path/to/memory/ [--max-kb 5] [--min-kb 8] [--dry-run] [--backup-dir /path/to/archive/]
"""

import os
import sys
import re
import argparse
from datetime import datetime

def is_valuable_line(line):
    """判断一行是否有保留价值"""
    stripped = line.strip()
    
    # 始终保留
    if stripped.startswith('#'):  # 标题
        return True
    if stripped.startswith('- [x]') or stripped.startswith('- [X]'):  # 完成项
        return True
    if any(kw in stripped for kw in ['部署', '上线', '修复', '发现', '踩坑', '根因', '解决', 'Bug', 'bug', '关键']):
        return True
    if re.match(r'^- \*\*', stripped):  # 加粗的列表项通常是重要的
        return True
    if stripped.startswith('<!-- tags:'):  # tags 行
        return True
    
    # 可能删除
    if stripped.startswith('```'):  # 代码块
        return False
    if len(stripped) > 200:  # 超长行通常是代码或日志
        return False
    
    return True  # 默认保留

def compress_content(content, max_bytes):
    """压缩内容，保留有价值的行"""
    lines = content.split('\n')
    result = []
    in_code_block = False
    current_section = None
    section_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # 跟踪代码块
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            continue  # 跳过代码块内容
        
        # section 标题
        if stripped.startswith('##'):
            if current_section and section_lines:
                result.append(current_section)
                # 每个 section 最多保留 10 行
                result.extend(section_lines[:10])
                if len(section_lines) > 10:
                    result.append(f'  _(... {len(section_lines) - 10} more lines)_')
                result.append('')
            current_section = line
            section_lines = []
            continue
        
        if is_valuable_line(line):
            section_lines.append(line)
    
    # 最后一个 section
    if current_section and section_lines:
        result.append(current_section)
        result.extend(section_lines[:10])
        if len(section_lines) > 10:
            result.append(f'  _(... {len(section_lines) - 10} more lines)_')
    
    compressed = '\n'.join(result)
    
    # 如果还是太大，进一步截断
    if len(compressed.encode('utf-8')) > max_bytes:
        while len(compressed.encode('utf-8')) > max_bytes and result:
            result.pop()
            compressed = '\n'.join(result)
    
    return compressed

def main():
    parser = argparse.ArgumentParser(description='压缩 OpenClaw 日志文件')
    parser.add_argument('memory_dir', help='memory 目录路径')
    parser.add_argument('--max-kb', type=int, default=5, help='压缩目标大小 (KB)')
    parser.add_argument('--min-kb', type=int, default=8, help='只压缩大于此大小的文件 (KB)')
    parser.add_argument('--dry-run', action='store_true', help='只显示会做什么，不实际执行')
    parser.add_argument('--backup-dir', default=None, help='备份目录 (默认: memory/archive/)')
    args = parser.parse_args()
    
    memory_dir = args.memory_dir
    backup_dir = args.backup_dir or os.path.join(memory_dir, 'archive')
    max_bytes = args.max_kb * 1024
    min_bytes = args.min_kb * 1024
    
    if not os.path.isdir(memory_dir):
        print(f"❌ 目录不存在: {memory_dir}")
        sys.exit(1)
    
    # 找到日志文件（YYYY-MM-DD.md 格式）
    log_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
    files = sorted(f for f in os.listdir(memory_dir) 
                   if log_pattern.match(f) and os.path.isfile(os.path.join(memory_dir, f)))
    
    if not files:
        print("没有找到日志文件")
        sys.exit(0)
    
    compressed_count = 0
    total_saved = 0
    
    for filename in files:
        filepath = os.path.join(memory_dir, filename)
        size = os.path.getsize(filepath)
        
        if size <= min_bytes:
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        compressed = compress_content(content, max_bytes)
        new_size = len(compressed.encode('utf-8'))
        saved = size - new_size
        
        if saved <= 0:
            continue
        
        ratio = (1 - new_size / size) * 100
        print(f"📄 {filename}: {size // 1024}KB → {new_size // 1024}KB (-{ratio:.0f}%)")
        
        if not args.dry_run:
            # 备份原文
            os.makedirs(backup_dir, exist_ok=True)
            backup_name = filename.replace('.md', '-full.md')
            backup_path = os.path.join(backup_dir, backup_name)
            
            if not os.path.exists(backup_path):  # 不覆盖已有备份
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   💾 备份: {backup_path}")
            
            # 写入压缩版
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(compressed)
        
        compressed_count += 1
        total_saved += saved
    
    mode = "(dry run) " if args.dry_run else ""
    print(f"\n{mode}完成: {compressed_count} 个文件压缩, 节省 {total_saved // 1024}KB")

if __name__ == '__main__':
    main()
