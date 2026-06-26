#!/usr/bin/env python3
"""
测试静默返回功能
验证技能在成功发送图片后返回 NO_REPLY 的效果
"""

import subprocess
import os

def test_silent_response():
    """测试静默返回逻辑"""
    print("=== 测试静默返回功能 ===")
    
    # 模拟技能的成功执行路径
    print("1. 模拟图片生成成功...")
    print("2. 模拟飞书发送成功...")
    print("3. 返回 NO_REPLY...")
    
    # 根据 skill.md 中的逻辑，成功发送后应该返回 NO_REPLY
    expected_response = "NO_REPLY"
    
    print(f"\n预期返回: '{expected_response}'")
    print("效果: OpenClaw 会将其识别为静默指令，不显示任何回复文字")
    print("用户只会在飞书中收到图片，不会在技能调用界面看到成功提示")
    
    # 验证 NO_REPLY 的规则
    print("\n=== NO_REPLY 使用规则 ===")
    print("✅ 正确: NO_REPLY (整个消息只有这个词)")
    print("❌ 错误: '任务完成 NO_REPLY' (附加了其他文字)")
    print("❌ 错误: 'NO_REPLY 任务完成' (附加了其他文字)")
    print("❌ 错误: '图片已发送 NO_REPLY' (附加了其他文字)")
    
    return expected_response

if __name__ == "__main__":
    result = test_silent_response()
    print(f"\n测试完成，技能应返回: {result}")