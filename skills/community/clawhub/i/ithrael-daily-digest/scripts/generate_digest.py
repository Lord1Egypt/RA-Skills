#!/usr/bin/env python3
"""
Daily Digest Generator
Scans current directory for .md files and generates a summary report.
"""

import os
import sys
from datetime import datetime
from pathlib import Path


def extract_title(content: str) -> str:
    """Extract the first heading as title."""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        elif line and not line.startswith('---'):
            return line[:50]
    return "Untitled"


def extract_sections(content: str) -> list:
    """Extract level-2 headings as section titles."""
    sections = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            sections.append(line[2:].strip())
    return sections


def count_words(content: str) -> int:
    """Count words in content."""
    return len(content.split())


def generate_digest(directory: str = ".") -> str:
    """Generate digest report for all .md files in directory."""
    dir_path = Path(directory)
    md_files = sorted(dir_path.glob("*.md"))
    
    if not md_files:
        return "## 今日摘要报告\n\n当前目录下没有找到 .md 文件。"
    
    report = []
    report.append("# 📋 今日摘要报告")
    report.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**扫描目录**: {dir_path.absolute()}")
    report.append(f"**文件总数**: {len(md_files)}\n")
    
    report.append("---\n")
    report.append("## 📄 文件清单\n")
    
    total_words = 0
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            title = extract_title(content)
            sections = extract_sections(content)
            word_count = count_words(content)
            total_words += word_count
            
            report.append(f"### {md_file.name}")
            report.append(f"- **标题**: {title}")
            report.append(f"- **字数**: {word_count}")
            report.append(f"- **章节**: {', '.join(sections) if sections else '无二级标题'}")
            report.append("")
        except Exception as e:
            report.append(f"### {md_file.name}")
            report.append(f"- **状态**: 读取失败 - {e}")
            report.append("")
    
    report.append("---\n")
    report.append("## 📊 统计汇总\n")
    report.append(f"- **总文件数**: {len(md_files)}")
    report.append(f"- **总字数**: {total_words}")
    report.append(f"- **平均字数**: {total_words // len(md_files) if md_files else 0}")
    
    return '\n'.join(report)


if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    print(generate_digest(directory))
