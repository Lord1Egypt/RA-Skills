#!/usr/bin/env python3
"""
Test script for human-like reply formatter
"""

import sys
import os
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reply_formatter import ReplyState, format_reply, should_use_greeting, detect_topic_change, DEFAULT_CONFIG

def test_scenario(name, messages, config=None):
    """Simulate a conversation scenario."""
    print(f"\n{'='*60}")
    print(f"场景: {name}")
    print(f"{'='*60}")

    if config is None:
        config = DEFAULT_CONFIG.copy()

    state = ReplyState()
    session_key = "test-session-1"

    # Clear any existing state for clean test
    state.state["conversations"] = {}

    history = []
    for i, (user_msg, original_reply) in enumerate(messages):
        print(f"\n用户: {user_msg}")
        print(f"AI 原回复: {original_reply}")

        # Detect topic change
        is_new_topic = False
        if history:
            is_new_topic = detect_topic_change(
                state.get_conversation(session_key).get("current_topic", ""),
                user_msg,
                history
            )

        # Decide whether to use greeting
        use_greet, greeting = should_use_greeting(state, session_key, config, is_new_topic)

        # Format reply
        formatted = format_reply(original_reply, config, use_greet, greeting)

        print(f"AI 格式化后: {formatted}")

        # Simulate sending
        state.update_conversation(session_key, use_greet,
                                 topic=user_msg[:20] if is_new_topic else None)

        history.append(user_msg)

def run_tests():
    random.seed(42)  # For reproducibility

    # Test 1: Early rounds - greeting will be used
    test_scenario("早期对话（称呼正常）", [
        ("老板，明天天气怎么样？", "老板，明天是多云转晴，温度18-25度。"),
        ("需要带伞吗？", "好的，不用带伞，没有雨。"),
        ("那空气质量呢？", "老板，空气质量良，PM2.5指数45。"),
    ])

    # Test 2: Later rounds - greeting should reduce
    test_scenario("后期对话（称呼减少）", [
        ("老板，帮我查一下股票。", "老板，601138现在价格是..."),
        ("那个基金呢？", "好的，那个基金最近表现不错。"),
        ("还有其他的吗？", "老板，还有几个关注的股票。"),
        ("今天有什么新闻？", "今天的财经新闻主要有..."),
        ("谢谢。", "不客气！"),
    ])

    # Test 3: New topic after silence (simulate)
    config = DEFAULT_CONFIG.copy()
    config["silence_minutes"] = 0.1  # 6 seconds for test

    test_scenario("话题切换（开启新话题称呼）", [
        ("老板，帮我买杯奶茶。", "老板，你想喝哪种？"),
        ("珍珠奶茶吧。", "好的，点一杯珍珠奶茶。"),
        ("加冰。", "加冰，记住了。"),
    ], config=config)

    # Test 4: Mechanical phrases removal
    test_scenario("机械词清理", [
        ("这个bug怎么修？", "好的，我已经找到问题所在了。"),
        ("那快点修复。", "收到，正在处理。"),
        ("搞定没有？", "明白了，马上就好。"),
    ])

    # Test 5: Casual level effect
    config_casual = DEFAULT_CONFIG.copy()
    config_casual["formal_level"] = 0.1

    test_scenario("非常随意的语气", [
        ("这个怎么搞？", "好的，我看看。"),
        ("搞定了吗？", "收到了，在弄了。"),
    ], config=config_casual)

    print(f"\n{'='*60}")
    print("测试完成！")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_tests()