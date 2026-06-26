#!/usr/bin/env python
"""Prompt-Router 测试脚本"""

import sys
sys.path.insert(0, 'C:/Users/User/.openclaw/workspace/skills/prompt-router')

from scripts.router import PromptRouter

# 创建路由器
router = PromptRouter(
    skills_dir='C:/Users/User/.openclaw/workspace/skills',
    confidence_threshold=0.25  # 降低阈值让匹配更容易
)

# 加载技能
print("=" * 60)
print("加载技能...")
count = router.load_skills()
print(f"已加载 {count} 个技能")
print()

# 显示前 10 个技能的元数据
print("前 10 个技能元数据:")
for i, target in enumerate(router._targets[:10], 1):
    print(f"{i}. {target['name']}")
    print(f"   触发词：{target.get('triggers', [])}")
    print(f"   关键词：{target.get('keywords', [])}")
    print()

# 测试路由
print("=" * 60)
print("路由测试:")
print()

test_prompts = [
    "搜索 Python 教程",
    "读取 config.json 文件",
    "北京今天天气怎么样",
    "帮我写一篇文章",
    "打开浏览器访问 GitHub",
    "查询天气",
    "搜索新闻",
    "创建任务",
]

for prompt in test_prompts:
    result = router.route(prompt)
    matched = result.match['name'] if result.match else 'None'
    invoke = router.should_invoke_skill(result)
    
    print(f"Prompt: {prompt}")
    print(f"  匹配：{matched}")
    print(f"  分数：{result.score:.2f}")
    print(f"  置信度：{result.confidence:.2f} ({result.confidence_level})")
    print(f"  调用技能：{invoke}")
    print()
