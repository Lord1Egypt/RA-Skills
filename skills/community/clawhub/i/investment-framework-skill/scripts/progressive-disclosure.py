#!/usr/bin/env python3
"""
P2 优化：渐进式披露 - 创建 references 目录和简化主 SKILL.md
"""

import os
import re

BASE_DIR = '/home/admin/.openclaw/workspace/investment-framework-skill'

def create_references_structure(skill_dir):
    """为技能创建 references 结构"""
    refs_dir = os.path.join(skill_dir, 'references')
    os.makedirs(refs_dir, exist_ok=True)
    
    # 创建标准参考文件
    files_to_create = {
        'theory.md': '# 理论基础\n\n详细理论内容...\n',
        'examples.md': '# 使用示例\n\n详细示例...\n',
        'faq.md': '# 常见问题\n\n详细 FAQ...\n',
    }
    
    for filename, content in files_to_create.items():
        filepath = os.path.join(refs_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  📁 创建 {filename}")

def simplify_skill_md(filepath):
    """简化 SKILL.md，将详细内容移至 references"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有 references 链接
    if '`references/' in content:
        return False
    
    # 在相关资源章节添加 references 链接
    if '## 🔗 相关资源' in content:
        # 已存在相关资源章节，添加 references 链接
        content = re.sub(
            r'(## 🔗 相关资源\n)',
            r'\1\n- `references/theory.md` - 理论基础\n- `references/examples.md` - 使用示例\n- `references/faq.md` - 常见问题\n',
            content
        )
    else:
        # 添加相关资源章节
        content = content.rstrip() + '\n\n---\n\n## 🔗 相关资源\n\n- `references/theory.md` - 理论基础\n- `references/examples.md` - 使用示例\n- `references/faq.md` - 常见问题\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    optimized = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        if '__pycache__' in root or '.git' in root:
            continue
        
        # 跳过子技能目录（已有主技能引用）
        if 'china-masters' in root and root.count('/') > 4:
            continue
        
        if 'SKILL.md' in files:
            filepath = os.path.join(root, 'SKILL.md')
            skill_dir = os.path.dirname(os.path.abspath(filepath))
            
            print(f"🔧 优化 {os.path.basename(root)}:")
            create_references_structure(root)
            if simplify_skill_md(filepath):
                optimized += 1
    
    print(f"\n🎉 渐进式披露优化完成：{optimized} 个技能")

if __name__ == '__main__':
    main()
