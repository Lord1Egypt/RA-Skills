#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Memory Retrieval
Only retrieve memories when needed
"""

import re

# Keywords that trigger memory retrieval
TRIGGER_KEYWORDS = [
    "我记得", "之前", "说过", "提过", "那个", "上次",
    "以前", "曾经", "记得", "想起",
]

# Keywords that skip retrieval
SKIP_KEYWORDS = [
    "你好", "在吗", "早", "晚安", "拜拜",
    "吃了吗", "在干嘛", "干嘛呢",
]

# Question patterns
QUESTION_PATTERNS = [
    r".*\?.*",  # Contains ?
    r".*吗.*",  # Contains 吗
    r".*什么.*",  # Contains 什么
    r".*怎么.*",  # Contains 怎么
    r".*为什么.*",  # Contains 为什么
]


def should_retrieve(message: str) -> bool:
    """
    Decide whether to retrieve memories
    
    Args:
        message: User's message
    
    Returns:
        True if should retrieve, False otherwise
    """
    message = message.strip()
    
    # Skip empty messages
    if not message:
        return False
    
    # Skip very short messages (< 3 chars)
    if len(message) < 3:
        return False
    
    # Skip greetings and small talk
    for keyword in SKIP_KEYWORDS:
        if keyword in message:
            print(f"[SMART] Skipping retrieval (greeting/small talk): '{message}'")
            return False
    
    # Trigger on memory-related keywords
    for keyword in TRIGGER_KEYWORDS:
        if keyword in message:
            print(f"[SMART] Triggering retrieval (keyword '{keyword}'): '{message}'")
            return True
    
    # Trigger on questions
    for pattern in QUESTION_PATTERNS:
        if re.match(pattern, message):
            print(f"[SMART] Triggering retrieval (question): '{message}'")
            return True
    
    # Trigger on long messages (> 15 chars)
    if len(message) > 15:
        print(f"[SMART] Triggering retrieval (long message): '{message}'")
        return True
    
    # Default: don't retrieve
    print(f"[SMART] Skipping retrieval (no trigger): '{message}'")
    return False


# Test
if __name__ == "__main__":
    test_messages = [
        ("你好", False),
        ("在吗", False),
        ("吃了吗", False),
        ("hi", False),
        ("?", False),
        ("我之前说过瀑布的事情吗？", True),
        ("我记得你提过 TTS 的用法", True),
        ("那个天台瀑布在哪里？", True),
        ("TTS 应该怎么用？", True),
        ("阿里云 Embedding 配置好了吗？", True),
        ("帮我查一下之前的对话记录", True),
        ("今天天气不错，适合出去走走", True),  # Long message
    ]
    
    print("=" * 60)
    print("Smart Retrieval Test")
    print("=" * 60)
    
    for message, expected in test_messages:
        result = should_retrieve(message)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{message}' -> {result} (expected: {expected})")
    
    print("=" * 60)
