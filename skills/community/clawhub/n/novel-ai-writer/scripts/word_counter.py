#!/usr/bin/env python3
"""
Word Counter for Novels
小说字数统计工具 - 统计章节/全文字数

用法：
    python3 word_counter.py chapter1.txt                    # 统计单个文件
    python3 word_counter.py chapter*.txt                     # 统计多个文件
    python3 word_counter.py --dir ./novel                    # 统计目录下所有txt文件
    python3 word_counter.py --watch chapter1.txt              # 实时监控文件变化
"""

import sys
import os
import time
from pathlib import Path
import re

def count_chinese_chars(text):
    """统计中文字符数（不含标点）"""
    # 只统计汉字
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)

def count_chars_with_punctuation(text):
    """统计中文字符数（含标点）"""
    # 统计汉字和中文标点
    pattern = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'
    chars = re.findall(pattern, text)
    return len(chars)

def count_words(text):
    """统计总字符数（所有字符）"""
    return len(text)

def analyze_text(text):
    """分析文本，返回各项统计"""
    # 去除空白字符进行统计
    clean_text = re.sub(r'\s+', '', text)
    
    chinese_chars = count_chinese_chars(text)
    chinese_with_punct = count_chars_with_punctuation(text)
    total_chars = count_words(clean_text)
    
    # 统计标点数量
    punct_pattern = r'[。！？，、；：""''【】《》…—～]' 
    punctuation_count = len(re.findall(punct_pattern, text))
    
    # 统计段落数
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    paragraph_count = len(paragraphs)
    
    # 统计行数
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    line_count = len(lines)
    
    return {
        'chinese_chars': chinese_chars,
        'chinese_with_punct': chinese_with_punct,
        'total_chars': total_chars,
        'punctuation': punctuation_count,
        'paragraphs': paragraph_count,
        'lines': line_count
    }

def format_number(num):
    """格式化数字，千分位分隔"""
    return f"{num:,}"

def print_report(stats, filename="总计"):
    """打印统计报告"""
    print(f"\n{'=' * 50}")
    print(f"📊 {filename}")
    print('=' * 50)
    print(f"  📝 中文字符（不含标点）：{format_number(stats['chinese_chars']):>10}")
    print(f"  📝 中文字符（含标点）  ：{format_number(stats['chinese_with_punct']):>10}")
    print(f"  📝 总字符数            ：{format_number(stats['total_chars']):>10}")
    print(f"  💬 标点符号            ：{format_number(stats['punctuation']):>10}")
    print(f"  📄 段落数              ：{format_number(stats['paragraphs']):>10}")
    print(f"  📏 行数                ：{format_number(stats['lines']):>10}")
    
    # 估算字数（按中文字符计算，一般每1000字约1500-2000字符）
    if stats['chinese_chars'] > 0:
        estimated_words = stats['chinese_chars'] // 2  # 粗略估算
        print(f"\n  📖 估算字数（按中文字符）: {format_number(estimated_words)} 字")
    
    # 估算章节阅读时间（按每分钟300字计算）
    if stats['chinese_chars'] > 0:
        minutes = stats['chinese_chars'] // 300
        if minutes < 60:
            print(f"  ⏱️  预估阅读时间: {minutes} 分钟")
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            print(f"  ⏱️  预估阅读时间: {hours} 小时 {remaining_minutes} 分钟")

def count_file(filepath):
    """统计单个文件"""
    try:
        text = Path(filepath).read_text(encoding='utf-8')
        stats = analyze_text(text)
        print_report(stats, filepath)
        return stats
    except Exception as e:
        print(f"❌ 读取文件失败 {filepath}: {e}")
        return None

def count_directory(dirpath):
    """统计目录下所有txt文件"""
    dir_path = Path(dirpath)
    if not dir_path.exists():
        print(f"❌ 目录不存在: {dirpath}")
        return
    
    txt_files = sorted(dir_path.glob("*.txt"))
    if not txt_files:
        print(f"❌ 目录中没有 .txt 文件: {dirpath}")
        return
    
    total_stats = {
        'chinese_chars': 0,
        'chinese_with_punct': 0,
        'total_chars': 0,
        'punctuation': 0,
        'paragraphs': 0,
        'lines': 0
    }
    
    file_count = 0
    for filepath in txt_files:
        file_stats = count_file(filepath)
        if file_stats:
            for key in total_stats:
                total_stats[key] += file_stats[key]
            file_count += 1
    
    print(f"\n{'=' * 50}")
    print(f"📚 共统计 {file_count} 个文件")
    print_report(total_stats, "全 部")

def watch_file(filepath):
    """实时监控文件变化"""
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"❌ 文件不存在: {filepath}")
        return
    
    print(f"\n👀 实时监控文件: {filepath}")
    print("按 Ctrl+C 退出\n")
    
    last_size = 0
    last_mtime = 0
    
    try:
        while True:
            current_size = filepath.stat().st_size
            current_mtime = filepath.stat().st_mtime
            
            if current_size != last_size or current_mtime != last_mtime:
                text = filepath.read_text(encoding='utf-8')
                stats = analyze_text(text)
                
                # 清除上一行并打印新统计
                print(f"\r  📝 字数: {format_number(stats['chinese_chars'])} | 字符: {format_number(stats['total_chars'])} | 段落: {stats['paragraphs']}    ", end='')
                
                last_size = current_size
                last_mtime = current_mtime
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 监控结束")

def main():
    args = sys.argv[1:]
    
    if not args:
        print(__doc__)
        print("\n📌 示例：")
        print("  python3 word_counter.py chapter1.txt")
        print("  python3 word_counter.py --dir ./novel")
        print("  python3 word_counter.py --watch chapter1.txt")
        return
    
    # 解析参数
    if '--watch' in args:
        idx = args.index('--watch')
        if idx + 1 < len(args):
            watch_file(args[idx + 1])
    elif '--dir' in args:
        idx = args.index('--dir')
        if idx + 1 < len(args):
            count_directory(args[idx + 1])
    else:
        # 统计文件列表
        files = [arg for arg in args if not arg.startswith('--')]
        
        if not files:
            print("❌ 请指定要统计的文件")
            return
        
        # 统计多个文件
        if len(files) == 1:
            count_file(files[0])
        else:
            total_stats = {
                'chinese_chars': 0,
                'chinese_with_punct': 0,
                'total_chars': 0,
                'punctuation': 0,
                'paragraphs': 0,
                'lines': 0
            }
            
            file_count = 0
            for filepath in files:
                file_stats = count_file(filepath)
                if file_stats:
                    for key in total_stats:
                        total_stats[key] += file_stats[key]
                    file_count += 1
            
            print(f"\n{'=' * 50}")
            print(f"📚 共统计 {file_count} 个文件")
            print_report(total_stats, "全 部")

if __name__ == "__main__":
    main()