#!/usr/bin/env python3
"""
Convert markdown novel chapters to plain text format.
Usage: python md_to_txt.py <novel_folder> [output_file]
"""

import os
import sys
import re
from pathlib import Path

def read_file_with_encoding(filepath):
    """Try multiple encodings to read a file."""
    encodings = ['utf-8', 'gb2312', 'gbk', 'latin-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    # If all fail, read as binary and decode with errors ignored
    with open(filepath, 'rb') as f:
        return f.read().decode('utf-8', errors='ignore')

def clean_markdown(content):
    """Remove markdown formatting for plain text."""
    # Remove YAML frontmatter
    content = re.sub(r'^---\s*\n.*?---\s*\n', '', content, flags=re.DOTALL)
    
    # Remove markdown headers but keep the text
    content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
    
    # Remove bold/italic markers
    content = re.sub(r'\*\*', '', content)
    content = re.sub(r'\*', '', content)
    content = re.sub(r'__', '', content)
    content = re.sub(r'_', '', content)
    
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`([^`]+)`', r'\1', content)
    
    # Remove links but keep text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    
    # Remove horizontal rules
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^===+$', '', content, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def convert_novel(novel_folder, output_file=None):
    """Convert all markdown chapters to a single text file."""
    novel_path = Path(novel_folder)
    
    if not novel_path.exists():
        print(f"Error: Folder not found: {novel_folder}")
        return False
    
    # Find all markdown files
    md_files = sorted(novel_path.glob('*.md'))
    
    if not md_files:
        print(f"Error: No markdown files found in {novel_folder}")
        return False
    
    # Determine output filename
    if output_file is None:
        output_file = novel_path / f"{novel_path.name}.txt"
    else:
        output_file = Path(output_file)
    
    # Compile all chapters
    all_content = []
    for md_file in md_files:
        print(f"Processing: {md_file.name}")
        content = read_file_with_encoding(md_file)
        cleaned = clean_markdown(content)
        
        # Add chapter separator
        all_content.append("=" * 50)
        all_content.append(f"Chapter: {md_file.stem}")
        all_content.append("=" * 50)
        all_content.append("")
        all_content.append(cleaned)
        all_content.append("")
        all_content.append("")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_content))
    
    print(f"\nConversion complete!")
    print(f"Output file: {output_file}")
    print(f"Total chapters: {len(md_files)}")
    print(f"File size: {output_file.stat().st_size} bytes")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python md_to_txt.py <novel_folder> [output_file]")
        print("Example: python md_to_txt.py 'X:/《觉醒之鬼》'")
        sys.exit(1)
    
    novel_folder = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_novel(novel_folder, output_file)
    sys.exit(0 if success else 1)
