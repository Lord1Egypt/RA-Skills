"""
Agent 交接示例
演示如何实现多 Agent 协作的交接机制
"""

import asyncio
from agents import Agent, Runner


# 创建专业 Agent
chinese_agent = Agent(
    name="中文助手",
    instructions="你只说中文，帮助用户解决问题。",
    handoff_description="处理中文问题"
)

english_agent = Agent(
    name="English Assistant",
    instructions="You only speak English.",
    handoff_description="Handle English questions"
)

math_agent = Agent(
    name="数学专家",
    instructions="你是数学专家，专门解答数学问题。",
    handoff_description="处理数学问题"
)

# 路由 Agent
triage_agent = Agent(
    name="总调度",
    instructions="根据用户语言和问题类型，交接给合适的助手。",
    handoffs=[chinese_agent, english_agent, math_agent],
)


async def main():
    print("多语言智能客服系统")
    
    test_inputs = [
        "你好，请介绍一下你自己",
        "Hello, can you help me?",
        "什么是斐波那契数列？",
    ]

    for user_input in test_inputs:
        print(f"\n问题: {user_input}")
        result = await Runner.run(triage_agent, user_input)
        print(f"当前 Agent: {result.current_agent.name}")
        print(f"回复: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
