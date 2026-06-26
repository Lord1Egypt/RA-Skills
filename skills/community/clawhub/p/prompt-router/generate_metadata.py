#!/usr/bin/env python
"""为所有技能生成缺失的 triggers 和 keywords 元数据"""

import re
from pathlib import Path

SKILLS_DIR = Path('C:/Users/User/.openclaw/workspace/skills')

def extract_words(text):
    """从文本中提取关键词"""
    # 提取英文单词
    en_words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9_-]*\b', text)
    # 提取中文词汇（简单分词：按标点分割）
    cn_words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
    return en_words + cn_words

def generate_metadata(skill_dir):
    """为技能生成元数据"""
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return None
    
    content = skill_md.read_text(encoding='utf-8')
    
    # 解析现有 frontmatter
    in_frontmatter = False
    frontmatter_lines = []
    body_start = 0
    
    for i, line in enumerate(content.split('\n')):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                body_start = i + 1
                break
        elif in_frontmatter:
            frontmatter_lines.append(line)
    
    # 解析现有元数据
    meta = {}
    for line in frontmatter_lines:
        if ':' in line:
            key = line.split(':')[0].strip()
            value = ':'.join(line.split(':')[1:]).strip()
            meta[key] = value
    
    # 必须有 name
    if 'name' not in meta:
        return None
    
    # 检查是否已有 triggers/keywords
    has_triggers = 'triggers' in meta or 'trigger' in meta
    has_keywords = 'keywords' in meta
    
    if has_triggers and has_keywords:
        return None  # 不需要生成
    
    # 从 description 和文件名生成
    description = meta.get('description', '')
    name = meta['name']
    
    # 生成 triggers（从 description 前 50 字提取）
    if not has_triggers:
        desc_words = extract_words(description[:100])
        # 添加常见触发模式
        triggers = []
        for word in desc_words[:10]:  # 最多 10 个
            triggers.append(word)
        
        # 添加中文名
        cn_name = re.findall(r'[\u4e00-\u9fa5]{2,}', name)
        if cn_name:
            triggers.insert(0, cn_name[0])
        
        meta['triggers'] = triggers
    
    # 生成 keywords（从 description 提取）
    if not has_keywords:
        keywords = extract_words(description)
        # 添加技能名
        keywords.insert(0, name)
        meta['keywords'] = keywords[:15]  # 最多 15 个
    
    return meta

def update_skill_md(skill_dir, new_meta):
    """更新 SKILL.md 文件"""
    skill_md = skill_dir / 'SKILL.md'
    content = skill_md.read_text(encoding='utf-8')
    
    # 找到 frontmatter 结束位置
    lines = content.split('\n')
    fm_end = 0
    in_fm = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_fm:
                in_fm = True
            else:
                fm_end = i
                break
    
    # 构建新的 frontmatter
    new_fm_lines = ['---']
    
    # 保留原有字段
    for key, value in new_meta.items():
        if key in ('name', 'description', 'version'):
            new_fm_lines.append(f'{key}: {value}')
    
    # 添加 triggers
    if 'triggers' in new_meta:
        triggers_str = ', '.join(new_meta['triggers'])
        new_fm_lines.append(f'triggers: {triggers_str}')
    
    # 添加 keywords
    if 'keywords' in new_meta:
        keywords_str = ', '.join(new_meta['keywords'])
        new_fm_lines.append(f'keywords: {keywords_str}')
    
    new_fm_lines.append('---')
    
    # 拼接新内容
    new_content = '\n'.join(new_fm_lines) + '\n\n' + '\n'.join(lines[fm_end+1:])
    
    # 写回文件
    skill_md.write_text(new_content, encoding='utf-8')
    print(f"[OK] 更新 {skill_dir.name}")

def main():
    print("扫描技能目录...")
    updated = 0
    skipped = 0
    
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('.') or skill_dir.name in ['tests', 'data', 'references']:
            continue
        
        meta = generate_metadata(skill_dir)
        if meta:
            update_skill_md(skill_dir, meta)
            updated += 1
        else:
            skipped += 1
    
    print(f"\n完成！更新 {updated} 个技能，跳过 {skipped} 个技能（已有元数据或无 SKILL.md）")

if __name__ == '__main__':
    main()
