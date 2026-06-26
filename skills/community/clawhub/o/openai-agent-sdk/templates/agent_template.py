"""
单 Agent 模板
使用此模板快速创建一个基本的 Agent
"""

import asyncio
from typing import Annotated
from agents import Agent, Runner, function_tool


# ============================================
# 1. 定义工具（可选）
# ============================================

@function_tool
def your_tool(
    param: Annotated[str, "参数描述"]
) -> str:
    """工具描述"""
    # 实现你的工具逻辑
    return f"处理结果: {param}"


# ============================================
# 2. 创建 Agent
# ============================================

agent = Agent(
    name="YourAgent",
    instructions="""
    在这里写 Agent 的指令。
    描述 Agent 的角色、能力和行为规范。
    """,
    tools=[your_tool],  # 添加工具
    # model="gpt-4",  # 可选：指定模型
)


# ============================================
# 3. 运行 Agent
# ============================================

async def main():
    # 方式 1: 异步运行（推荐）
    result = await Runner.run(agent, "你的输入")
    print(result.final_output)
    
    # 方式 2: 同步运行
    # result = Runner.run_sync(agent, "你的输入")
    # print(result.final_output)
    
    # 方式 3: 流式运行
    # result = Runner.run_streamed(agent, "你的输入")
    # async for event in result.stream_events():
    #     print(event)


if __name__ == "__main__":
    asyncio.run(main())
