#!/usr/bin/env python
"""调试路由匹配过程"""

import sys
sys.path.insert(0, 'C:/Users/User/.openclaw/workspace/skills/prompt-router')

from scripts.router import PromptRouter

# 创建路由器
router = PromptRouter(
    skills_dir='C:/Users/User/.openclaw/workspace/skills',
    confidence_threshold=0.3
)

# 加载技能
router.load_skills()

# 测试"搜索 Python 教程"
prompt = "搜索 Python 教程"
print(f"Prompt: {prompt}")
print("=" * 60)

# 分词
tokens = router.tokenizer.tokenize(prompt)
print(f"Prompt 分词：{tokens}")
print()

# 查找 multi-search-engine 技能
search_skill = None
for target in router._targets:
    if target['name'] == 'multi-search-engine':
        search_skill = target
        break

if search_skill:
    print(f"找到技能：{search_skill['name']}")
    print(f"  description: {search_skill.get('description', '')[:80]}...")
    print(f"  triggers: {search_skill.get('triggers', [])}")
    print(f"  keywords: {search_skill.get('keywords', [])}")
    print()
    
    # 手动评分
    print("评分详情:")
    total_score = 0
    
    # 名称匹配
    name_tokens = router.tokenizer.tokenize(search_skill['name'])
    name_match = tokens & name_tokens
    name_score = len(name_match) / len(name_tokens) if name_tokens else 0
    print(f"  name: {name_tokens}, 匹配：{name_match}, 分数：{name_score:.2f} x {router.scorer.field_weights['name']} = {name_score * router.scorer.field_weights['name']:.2f}")
    total_score += name_score * router.scorer.field_weights['name']
    
    # 触发词匹配
    trigger_tokens = set()
    for t in search_skill.get('triggers', []):
        trigger_tokens.update(router.tokenizer.tokenize(t))
    trigger_match = tokens & trigger_tokens
    trigger_score = len(trigger_match) / len(trigger_tokens) if trigger_tokens else 0
    print(f"  triggers: {trigger_tokens}, 匹配：{trigger_match}, 分数：{trigger_score:.2f} x {router.scorer.field_weights['triggers']} = {trigger_score * router.scorer.field_weights['triggers']:.2f}")
    total_score += trigger_score * router.scorer.field_weights['triggers']
    
    # 关键词匹配
    keyword_tokens = set()
    for k in search_skill.get('keywords', []):
        keyword_tokens.update(router.tokenizer.tokenize(k))
    keyword_match = tokens & keyword_tokens
    keyword_score = len(keyword_match) / len(keyword_tokens) if keyword_tokens else 0
    print(f"  keywords: {keyword_tokens}, 匹配：{keyword_match}, 分数：{keyword_score:.2f} x {router.scorer.field_weights['keywords']} = {keyword_score * router.scorer.field_weights['keywords']:.2f}")
    total_score += keyword_score * router.scorer.field_weights['keywords']
    
    print(f"  总分：{total_score:.2f}")
    print()
else:
    print("未找到 multi-search-engine 技能")

# 测试"查询天气"
print()
print("=" * 60)
prompt = "查询天气"
print(f"Prompt: {prompt}")
tokens = router.tokenizer.tokenize(prompt)
print(f"Prompt 分词：{tokens}")

# 查找 weather 相关技能
for target in router._targets:
    if 'weather' in target['name'].lower() or '天气' in target.get('description', ''):
        print(f"\n可能匹配：{target['name']}")
        print(f"  triggers: {target.get('triggers', [])}")
        print(f"  keywords: {target.get('keywords', [])}")
        
        score = router.scorer.score(tokens, target)
        print(f"  分数：{score:.2f}")
