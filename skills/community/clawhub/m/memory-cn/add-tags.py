#!/usr/bin/env python3
"""
批量给 memory/projects/*.md 文件添加 tags 标签行。
根据文件名和内容自动生成中文+英文关键词标签。

用法: python3 add-tags.py /path/to/memory/projects/
"""

import os
import sys
import re

def extract_tags_from_content(filepath, content):
    """从文件内容中提取关键词作为 tags"""
    tags = set()
    basename = os.path.basename(filepath).replace('.md', '')
    
    # 从文件名提取
    tags.add(basename)
    
    # 提取中文标题（# 开头的行）
    for line in content.split('\n')[:5]:
        m = re.match(r'^#\s+(.+?)[\s(（]', line)
        if m:
            title = m.group(1).strip()
            if title:
                tags.add(title)
    
    # 提取技术栈关键词
    tech_patterns = [
        r'技术栈[：:]\s*(.+)',
        r'Express|Phaser|Socket\.IO|React|Vue|Node\.js|SQLite|PostgreSQL|Redis',
        r'PM2|nginx|Docker',
    ]
    for pattern in tech_patterns:
        for m in re.finditer(pattern, content):
            if m.groups():
                tags.update(t.strip() for t in m.group(1).split('+'))
            else:
                tags.add(m.group(0))
    
    # 提取域名关键词
    m = re.search(r'域名[：:]\s*(\S+)', content)
    if m:
        domain = m.group(1).strip()
        # 提取主域名部分
        parts = domain.replace('https://', '').replace('http://', '').split('/')
        if parts:
            tags.add(parts[0])
    
    # 提取端口
    m = re.search(r'端口[：:]\s*(\d+)', content)
    if m:
        tags.add(f"port:{m.group(1)}")
    
    # 清理
    tags = {t for t in tags if t and len(t) > 1 and len(t) < 30}
    
    return ', '.join(sorted(tags))

def process_file(filepath, dry_run=False):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 已有 tags 则跳过
    if content.startswith('<!-- tags:'):
        return False, "already tagged"
    
    tags = extract_tags_from_content(filepath, content)
    if not tags:
        return False, "no tags extracted"
    
    tag_line = f"<!-- tags: {tags} -->\n"
    
    if dry_run:
        print(f"  WOULD ADD: {tag_line.strip()}")
        return True, "dry run"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(tag_line + content)
    
    return True, tags

def main():
    if len(sys.argv) < 2:
        print("用法: python3 add-tags.py /path/to/memory/projects/ [--dry-run]")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    if not os.path.isdir(target_dir):
        print(f"❌ 目录不存在: {target_dir}")
        sys.exit(1)
    
    files = sorted(f for f in os.listdir(target_dir) if f.endswith('.md'))
    
    if not files:
        print("没有找到 .md 文件")
        sys.exit(0)
    
    tagged = 0
    skipped = 0
    
    for filename in files:
        filepath = os.path.join(target_dir, filename)
        success, msg = process_file(filepath, dry_run)
        
        if success:
            tagged += 1
            print(f"✅ {filename}: {msg}")
        else:
            skipped += 1
            if msg != "already tagged":
                print(f"⏭️ {filename}: {msg}")
    
    mode = "(dry run) " if dry_run else ""
    print(f"\n{mode}完成: {tagged} 个文件添加了标签, {skipped} 个跳过")

if __name__ == '__main__':
    main()
