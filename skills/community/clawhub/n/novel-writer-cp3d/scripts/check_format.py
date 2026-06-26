#!/usr/bin/env python3
"""
Check novel chapter formatting consistency.
Usage: python check_format.py <novel_folder>
"""

import os
import sys
import re
from pathlib import Path
from collections import defaultdict

def read_file_with_encoding(filepath):
    """Try multiple encodings to read a file."""
    encodings = ['utf-8', 'gb2312', 'gbk', 'latin-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(filepath, 'rb') as f:
        return f.read().decode('utf-8', errors='ignore')

def check_chapter_format(filepath, content):
    """Check a single chapter for formatting issues."""
    issues = []
    filename = filepath.name
    
    # Check for frontmatter
    if not re.search(r'^#\s+\d+[-–]第[一二三四五六七八九十\d]+章', content, re.MULTILINE):
        issues.append("Missing or incorrect chapter title format")
    
    # Check for author line
    if not re.search(r'##?\s*作者[：:]', content):
        issues.append("Missing author line")
    
    # Check for date line
    if not re.search(r'##?\s*日期[：:]', content):
        issues.append("Missing date line")
    
    # Check for section separators
    if '---' not in content:
        issues.append("Missing section separator (---)")
    
    # Check paragraph lengths
    paragraphs = content.split('\n\n')
    long_paragraphs = 0
    for p in paragraphs:
        if len(p) > 500:
            long_paragraphs += 1
    if long_paragraphs > 0:
        issues.append(f"{long_paragraphs} very long paragraphs (>500 chars)")
    
    # Check for consistent ending format
    if not re.search(r'\*\*.*?(结束|完).*?\*\*', content):
        issues.append("Missing ending marker (e.g., '**第X天，结束。**')")
    
    # Check line endings
    lines = content.split('\n')
    very_short_lines = sum(1 for line in lines if 0 < len(line) < 10)
    if very_short_lines > 50:
        issues.append(f"Many very short lines ({very_short_lines}), possible formatting issues")
    
    return issues

def check_novel_format(novel_folder):
    """Check all chapters in a novel folder."""
    novel_path = Path(novel_folder)
    
    if not novel_path.exists():
        print(f"Error: Folder not found: {novel_folder}")
        return False
    
    # Find all markdown files
    md_files = sorted(novel_path.glob('*.md'))
    
    if not md_files:
        print(f"Error: No markdown files found in {novel_folder}")
        return False
    
    print(f"Checking {len(md_files)} chapters...\n")
    
    all_issues = defaultdict(list)
    total_issues = 0
    
    for md_file in md_files:
        content = read_file_with_encoding(md_file)
        issues = check_chapter_format(md_file, content)
        
        if issues:
            all_issues[md_file.name] = issues
            total_issues += len(issues)
            print(f"❌ {md_file.name}:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ {md_file.name}: OK")
    
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Total chapters: {len(md_files)}")
    print(f"  Chapters with issues: {len(all_issues)}")
    print(f"  Total issues: {total_issues}")
    
    if all_issues:
        print(f"\nChapters needing attention:")
        for chapter, issues in all_issues.items():
            print(f"  - {chapter} ({len(issues)} issues)")
    else:
        print(f"\n✨ All chapters look good!")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_format.py <novel_folder>")
        print("Example: python check_format.py 'X:/《觉醒之鬼》'")
        sys.exit(1)
    
    novel_folder = sys.argv[1]
    success = check_novel_format(novel_folder)
    sys.exit(0 if success else 1)
