#!/usr/bin/env python3
"""
批量优化 SKILL.md 元数据
- 补充 allowed-tools
- 规范化 skill_type
"""

import os
import re

BASE_DIR = '/home/admin/.openclaw/workspace/investment-framework-skill'

# 技能类型映射
SKILL_TYPE_MAP = {
    '核心🔴': ['value-analyzer', 'intrinsic-value-calculator', 'moat-evaluator', 'asset-allocator'],
    '通用🟡': 'all_others',
}

# 工具映射（根据技能类型）
TOOLS_MAP = {
    'value-analyzer': 'allowed-tools: [Bash, Read, Exec]',
    'stock-picker': 'allowed-tools: [Bash, Read, Exec]',
    'simple-investor': 'allowed-tools: [Bash, Read, Exec]',
    'intrinsic-value-calculator': 'allowed-tools: [Bash, Read, Exec]',
    'industry-analyst': 'allowed-tools: [Bash, Read, Exec]',
    'cycle-locator': 'allowed-tools: [Bash, Read, Exec]',
    'decision-checklist': 'allowed-tools: [Read]',
    'bias-detector': 'allowed-tools: [Read]',
    'second-level-thinker': 'allowed-tools: [Read]',
    'future-forecaster': 'allowed-tools: [Bash, Read, Exec]',
    'moat-evaluator': 'allowed-tools: [Bash, Read, Exec]',
    'asset-allocator': 'allowed-tools: [Read]',
    'portfolio-designer': 'allowed-tools: [Read]',
    'global-allocator': 'allowed-tools: [Read]',
    'default': 'allowed-tools: [Read]',
}

def optimize_skill_file(filepath):
    """优化单个 SKILL.md 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取技能名称
    name_match = re.search(r'^name:\s*(\S+)', content, re.MULTILINE)
    if not name_match:
        return False
    
    skill_name = name_match.group(1)
    
    # 检查是否已有 allowed-tools
    if 'allowed-tools:' in content:
        return False
    
    # 获取工具配置
    tools = TOOLS_MAP.get(skill_name, TOOLS_MAP['default'])
    
    # 在 skill_type 后插入 allowed-tools
    content = re.sub(
        r'^(skill_type:\s*\S+)',
        rf'\1\n{tools}',
        content,
        flags=re.MULTILINE
    )
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {skill_name}: 补充 allowed-tools")
    return True

def main():
    """主函数"""
    optimized = 0
    
    # 遍历所有 SKILL.md
    for root, dirs, files in os.walk(BASE_DIR):
        # 跳过特定目录
        if '__pycache__' in root or '.git' in root:
            continue
        
        if 'SKILL.md' in files:
            filepath = os.path.join(root, 'SKILL.md')
            if optimize_skill_file(filepath):
                optimized += 1
    
    print(f"\n🎉 优化完成：{optimized} 个技能")

if __name__ == '__main__':
    main()
