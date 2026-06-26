#!/usr/bin/env python3
"""
LLM Key Pool 使用示例
演示如何使用分层轮询的多平台API Key管理
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from llm_key_pool import TieredLLMClient


def main():
    print("=" * 60)
    print("LLM Key Pool 使用示例")
    print("=" * 60)

    # 1. 初始化客户端
    print("\n[步骤1] 初始化客户端...")
    config_path = './llm_config.yaml'
    client = TieredLLMClient(config_path)
    print(f"✓ 客户端初始化成功")

    # 2. 查看Key池状态
    print("\n[步骤2] 查看Key池状态...")
    import json
    status = client.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))

    # 3. 调用LLM（简单问题）
    print("\n[步骤3] 调用LLM - 简单问题...")
    result1, usage1 = client.call_llm(
        prompt="用一句话解释什么是人工智能",
        temperature=0.7,
        max_tokens=100
    )
    print(f"\n平台: {usage1['provider']}")
    print(f"层级: {usage1['tier']}")
    print(f"模型: {usage1['model']}")
    print(f"响应: {result1}")

    # 4. 调用LLM（复杂问题）
    print("\n" + "=" * 60)
    print("[步骤4] 调用LLM - 复杂问题...")
    result2, usage2 = client.call_llm(
        prompt="请详细介绍量子计算的基本原理和应用场景",
        system_prompt="你是一个专业的科学讲解者，请用通俗易懂的语言解释",
        temperature=0.7,
        max_tokens=300
    )
    print(f"\n平台: {usage2['provider']}")
    print(f"层级: {usage2['tier']}")
    print(f"模型: {usage2['model']}")
    print(f"响应:\n{result2}")

    # 5. 再次查看状态
    print("\n" + "=" * 60)
    print("[步骤5] 再次查看Key池状态...")
    status_after = client.get_status()
    print(json.dumps(status_after, indent=2, ensure_ascii=False))

    print("\n" + "=" * 60)
    print("✓ 示例运行完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
