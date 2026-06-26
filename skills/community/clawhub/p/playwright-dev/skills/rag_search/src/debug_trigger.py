#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug auto_trigger"""

import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

MEMORY_KEYWORDS = [
    "之前说过", "之前提过", "之前讲过", "之前提到",
    "我记得", "我有印象", "我好像说过",
    "上次", "上上次", "上一次",
    "以前", "过去", "曾经",
    "说过", "提过", "讲过",
    "我说过", "我提过", "我讲过",
    "你记得", "还记得", "有印象",
    "之前", "从前",
    "那个", "这个", "那些", "这些",
    "刚才", "刚刚", "之前聊",
]

MEMORY_PATTERN = re.compile('|'.join(re.escape(kw) for kw in MEMORY_KEYWORDS))

msg = "我之前说过瀑布的事情吗？"
print(f"Message: {msg}")
print(f"Message length: {len(msg)}")
print(f"Keywords count: {len(MEMORY_KEYWORDS)}")

# Test pattern
match = MEMORY_PATTERN.search(msg)
print(f"Pattern match: {match}")
if match:
    print(f"Matched text: {match.group()}")
    print(f"Match span: {match.span()}")

# Test individual keywords
print("\nKeyword matches:")
for kw in MEMORY_KEYWORDS:
    if kw in msg:
        print(f"  Found: {kw}")

# Test should_trigger
def should_trigger_search(user_message: str) -> bool:
    result = MEMORY_PATTERN.search(user_message)
    print(f"Pattern search result: {result}")
    if result:
        return True
    
    if any(pattern in user_message for pattern in ["吗？", "吗?", "？", "?"]):
        if any(word in user_message for word in ["过", "记得", "印象", "之前", "上次"]):
            return True
    
    return False

print(f"\nShould trigger: {should_trigger_search(msg)}")
