"""
多 Agent 协作模板
使用此模板创建多个协作的 Agent
"""

import asyncio
from typing import Annotated
from agents import Agent, Runner, function_tool, trace


# ============================================
# 1. 定义工具
# ============================================

@function_tool
def search_tool(query: Annotated[str, "搜索查询"]) -> str:
    """搜索工具"""
    return f"搜索结果: {query}"


@function_tool
def analyze_tool(data: Annotated[str, "要分析的数据"]) -> str:
    """分析工具"""
    return f"分析结果: {data}"


# ============================================
# 2. 创建专业 Agent
# ============================================

specialist_1 = Agent(
    name="Specialist1",
    instructions="第一个专业 Agent 的指令",
    tools=[search_tool],
    handoff_description="处理第一类任务",
)

specialist_2 = Agent(
    name="Specialist2",
    instructions="第二个专业 Agent 的指令",
    tools=[analyze_tool],
    handoff_description="处理第二类任务",
)

specialist_3 = Agent(
    name="Specialist3",
    instructions="第三个专业 Agent 的指令",
    handoff_description="处理第三类任务",
)


# ============================================
# 3. 创建协调 Agent（选择一种模式）
# ============================================

# 模式 A: Handoffs（交接模式）
coordinator = Agent(
    name="Coordinator",
    instructions="""
    你是协调者，根据任务类型交接给合适的专业 Agent。
    - 任务类型1 → Specialist1
    - 任务类型2 → Specialist2
    - 任务类型3 → Specialist3
    """,
    handoffs=[specialist_1, specialist_2, specialist_3],
)

# 模式 B: Agents as Tools（工具模式）
# coordinator = Agent(
#     name="Coordinator",
#     instructions="使用专业 Agent 作为工具完成任务",
#     tools=[
#         specialist_1.as_tool(
#             tool_name="use_specialist_1",
#             tool_description="调用第一个专业 Agent"
#         ),
#         specialist_2.as_tool(
#             tool_name="use_specialist_2",
#             tool_description="调用第二个专业 Agent"
#         ),
#     ],
# )


# ============================================
# 4. 运行工作流
# ============================================

async def main():
    # 使用 trace 追踪工作流
    with trace("多 Agent 工作流"):
        result = await Runner.run(coordinator, "你的任务描述")
        
        print(f"当前 Agent: {result.current_agent.name}")
        print(f"结果: {result.final_output}")
        
        # 查看完整对话历史
        # print(result.to_input_list())


if __name__ == "__main__":
    asyncio.run(main())
