"""
基础 Agent 示例
演示如何创建和运行一个简单的 Agent
"""

import asyncio
from agents import Agent, Runner


async def main():
    # 创建一个简单的 Agent
    agent = Agent(
        name="助手",
        instructions="你是一个有帮助的助手，用中文回答问题。",
    )

    # 运行 Agent
    result = await Runner.run(agent, "介绍一下你自己")
    
    print("=" * 50)
    print("Agent 回复：")
    print("=" * 50)
    print(result.final_output)
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
