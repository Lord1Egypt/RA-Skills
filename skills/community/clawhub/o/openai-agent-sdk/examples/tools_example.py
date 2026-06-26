"""
工具使用示例
演示如何为 Agent 添加和调用工具
"""

import asyncio
from typing import Annotated
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool


class WeatherOutput(BaseModel):
    city: str = Field(description="城市名称")
    temperature_range: str = Field(description="温度范围")
    conditions: str = Field(description="天气状况")


@function_tool
def get_weather(city: Annotated[str, "城市名称"]) -> WeatherOutput:
    """获取指定城市的天气信息"""
    print(f"[调试] 查询 {city} 的天气")
    return WeatherOutput(city=city, temperature_range="20°C", conditions="晴朗")


@function_tool
def calculate(expression: Annotated[str, "数学表达式"]) -> float:
    """计算数学表达式的结果"""
    print(f"[调试] 计算: {expression}")
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        return 0.0


async def main():
    agent = Agent(
        name="多功能助手",
        instructions="你是一个多功能助手，可以帮助查询天气和进行计算。",
        tools=[get_weather, calculate],
    )

    questions = [
        "北京今天天气怎么样？",
        "计算 123 + 456",
    ]

    for question in questions:
        print(f"\n问题: {question}")
        result = await Runner.run(agent, question)
        print(f"回答: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
