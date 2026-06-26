#!/usr/bin/env python
"""测试单个技能解析"""

import sys
sys.path.insert(0, 'C:/Users/User/.openclaw/workspace/skills/prompt-router')

from scripts.router import PromptRouter

# 创建路由器
router = PromptRouter()

# 测试解析 prompt-router 自己的 SKILL.md
skill_md_path = 'C:/Users/User/.openclaw/workspace/skills/prompt-router/SKILL.md'
content = open(skill_md_path, 'r', encoding='utf-8').read()

print("解析 prompt-router/SKILL.md:")
print("=" * 60)
meta = router._parse_skill_md(content)
print(f"name: {meta.get('name')}")
print(f"description: {meta.get('description', '')[:50]}...")
print(f"triggers: {meta.get('triggers', [])}")
print(f"keywords: {meta.get('keywords', [])}")
print()

# 测试解析 multi-search-engine
print("解析 multi-search-engine/SKILL.md:")
print("=" * 60)
skill_md_path = 'C:/Users/User/.openclaw/workspace/skills/multi-search-engine/SKILL.md'
content = open(skill_md_path, 'r', encoding='utf-8').read()
meta = router._parse_skill_md(content)
print(f"name: {meta.get('name')}")
print(f"description: {meta.get('description', '')[:50]}...")
print(f"triggers: {meta.get('triggers', [])}")
print(f"keywords: {meta.get('keywords', [])}")
