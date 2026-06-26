#!/usr/bin/env python
"""批量修复关键技能的 triggers/keywords"""

from pathlib import Path

SKILLS_DIR = Path('C:/Users/User/.openclaw/workspace/skills')

# 关键技能的手动 triggers/keywords 配置
SKILL_FIXES = {
    'multi-search-engine': {
        'triggers': ['搜索', '查找', 'search', 'find', '查询', '检索'],
        'keywords': ['search', 'engine', 'multi', '搜索', '查找', '查询', 'google', 'baidu', 'bing'],
    },
    'agent-browser': {
        'triggers': ['浏览器', 'browser', '打开网页', '访问', '点击', '截图'],
        'keywords': ['browser', 'automation', 'click', 'navigate', 'screenshot', '网页', '自动化'],
    },
    'excel-xlsx': {
        'triggers': ['Excel', '表格', 'xlsx', 'xls', '电子表格', '创建表格', '读取表格'],
        'keywords': ['excel', 'xlsx', 'xls', 'spreadsheet', '表格', '单元格', '公式', 'chart'],
    },
    'word-docx': {
        'triggers': ['Word', '文档', 'docx', 'doc', '创建文档', '读取文档'],
        'keywords': ['word', 'docx', 'doc', 'document', '文档', '样式', '段落', 'table'],
    },
    'github-trending-cn': {
        'triggers': ['GitHub', 'trending', '热门项目', '开源', '趋势'],
        'keywords': ['github', 'trending', 'repository', '开源', '热门', '项目', 'star'],
    },
    'task-decomposer': {
        'triggers': ['任务分解', '规划', '计划', '拆解', '工作流', '自动化'],
        'keywords': ['task', 'decompose', 'plan', 'workflow', '任务', '分解', '规划', '自动化'],
    },
    'planning-with-files': {
        'triggers': ['规划', '计划', '任务管理', '进度跟踪', '长期任务'],
        'keywords': ['planning', 'files', 'task', 'progress', '规划', '任务', '进度', '文件'],
    },
    'ppt-generator': {
        'triggers': ['PPT', '演示文稿', '幻灯片', '生成 PPT', '演示'],
        'keywords': ['ppt', 'presentation', 'slides', '演示', '幻灯片', 'HTML', '生成'],
    },
    'humanizer': {
        'triggers': ['改写', '润色', '人性化', '去 AI 味', '优化文本'],
        'keywords': ['humanizer', 'rewrite', 'polish', 'AI', '改写', '润色', '优化'],
    },
    'memory-system': {
        'triggers': ['记忆', 'memory', '笔记', '记录', '长期记忆'],
        'keywords': ['memory', 'notes', 'obsidian', '记忆', '笔记', '记录', '长期'],
    },
}

def update_skill(skill_name, fixes):
    """更新技能的元数据"""
    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists():
        print(f"[跳过] {skill_name} 目录不存在")
        return False
    
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        print(f"[跳过] {skill_name} 无 SKILL.md")
        return False
    
    content = skill_md.read_text(encoding='utf-8')
    
    # 找到 frontmatter
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
    for line in lines[1:fm_end]:
        if ':' in line:
            key = line.split(':')[0].strip()
            if key in ('name', 'description', 'version'):
                new_fm_lines.append(line)
    
    # 添加新的 triggers
    if 'triggers' in fixes:
        triggers_str = ', '.join(fixes['triggers'])
        new_fm_lines.append(f'triggers: {triggers_str}')
    
    # 添加新的 keywords
    if 'keywords' in fixes:
        keywords_str = ', '.join(fixes['keywords'])
        new_fm_lines.append(f'keywords: {keywords_str}')
    
    new_fm_lines.append('---')
    
    # 拼接新内容
    new_content = '\n'.join(new_fm_lines) + '\n\n' + '\n'.join(lines[fm_end+1:])
    
    # 写回文件
    skill_md.write_text(new_content, encoding='utf-8')
    print(f"[OK] {skill_name}")
    return True

def main():
    print("修复关键技能元数据...")
    print("=" * 60)
    
    updated = 0
    for skill_name, fixes in SKILL_FIXES.items():
        if update_skill(skill_name, fixes):
            updated += 1
    
    print("=" * 60)
    print(f"完成！更新 {updated}/{len(SKILL_FIXES)} 个技能")

if __name__ == '__main__':
    main()
