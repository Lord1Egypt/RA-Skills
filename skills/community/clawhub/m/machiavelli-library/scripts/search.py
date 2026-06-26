#!/usr/bin/env python3
"""精确原文搜索工具。用法：python3 search.py "<关键词>" [--lang zh|en] [--limit 10]"""
import os, sys, subprocess, argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY = os.path.join(BASE, 'library')

def search(keyword, lang=None, limit=10):
    cmd = ['grep', '-rnH', '-i', '--color=never', keyword, LIBRARY]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]

        if lang == 'en':
            lines = [l for l in lines if '/en/' in l.split(':', 1)[0]]
        elif lang == 'zh':
            lines = [l for l in lines if '/en/' not in l.split(':', 1)[0]]

        lines = lines[:limit]
        for line in lines:
            parts = line.split(':', 2)
            if len(parts) >= 3:
                path = parts[0].replace(LIBRARY + '/', '')
                print(f"{path}:{parts[1]}")
                print(f"  {parts[2][:200]}")
                print()
        if not lines:
            print("找不到匹配内容")
    except Exception as e:
        print(f"搜索出错: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='马基雅维利图书馆精确原文搜索')
    parser.add_argument('keyword', help='搜索关键词（支持中英文）')
    parser.add_argument('--lang', choices=['zh', 'en'], help='限定语言')
    parser.add_argument('--limit', type=int, default=10, help='返回条数上限')
    args = parser.parse_args()
    search(args.keyword, args.lang, args.limit)
