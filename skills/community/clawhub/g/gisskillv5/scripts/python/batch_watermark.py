#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# wm:坤图_GIS:V5.0
"""批量注入坤图_GIS V5.0水印到所有缺失文件"""

import os
import re

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WATERMARK = "<!-- wm:坤图_GIS:V5.0 -->\n"
EXCLUDE_DIRS = {'delivery', '__pycache__', '.git'}

def has_watermark(content: str) -> bool:
    return '坤图_GIS' in content

def add_watermark_to_file(filepath: str) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if has_watermark(content):
            return False
        
        # Add watermark at the very beginning
        new_content = WATERMARK + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"  ERROR: {filepath} - {e}")
        return False

def main():
    count = 0
    for root, dirs, files in os.walk(SKILL_ROOT):
        # Skip excluded dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for fname in files:
            if fname.endswith(('.md', '.py', '.txt', '.json')):
                fpath = os.path.join(root, fname)
                if add_watermark_to_file(fpath):
                    rel = os.path.relpath(fpath, SKILL_ROOT)
                    print(f"  ✓ {rel}")
                    count += 1
    
    print(f"\n总计注入: {count} 个文件")

if __name__ == '__main__':
    main()
