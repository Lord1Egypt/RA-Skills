---
name: openai-agent-sdk
description: Build multi-agent AI systems with OpenAI Agents SDK. Create, orchestrate, and manage AI agents with tools, handoffs, guardrails, and tracing. Supports 100+ LLMs via LiteLLM.
metadata: 
  version: "1.0.0"
  author: "mathematician"
  tags: ["ai", "agent", "openai", "multi-agent", "orchestration", "llm"]
  emoji: "🤖"
  requirements:
    python: ">=3.10"
    packages:
      - "openai-agents>=0.1.0"
---

# OpenAI Agent SDK 技能

使用 OpenAI Agents SDK 构建多 Agent AI 系统。轻量级但强大的框架，支持 Agent 协作、工具调用、交接机制和追踪调试。

## 何时使用此技能

当用户需要：
- 构建多 Agent 协作系统
- 实现 Agent 之间的任务交接
- 为 Agent 添加工具（function calling）
- 创建智能路由和编排系统
- 实现人机协作（Human in the Loop）
- 构建语音 Agent（Realtime Agents）
- 需要追踪和调试 Agent 工作流

## 核心概念

### 1. Agent（智能体）
配置了指令、工具、防护栏和交接能力的 LLM。

```python
from agents import Agent

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[...],        # 可选：工具列表
    handoffs=[...],     # 可选：可交接的其他 agent
    model="gpt-4",      # 可选：模型选择
)
```

### 2. Tools（工具）
让 Agent 执行动作的函数。

```python
from agents import function_tool
from typing import Annotated

@function_tool
def get_weather(city: Annotated[str, "城市名称"]) -> str:
    """获取指定城市的天气信息"""
    return f"{city}：晴朗，20°C"

agent = Agent(tools=[get_weather])
```

### 3. Runner（运行器）
执行 Agent 的引擎，支持三种运行模式。

```python
from agents import Runner

# 同步运行
result = Runner.run_sync(agent, "Hello")

# 异步运行（推荐）
result = await Runner.run(agent, "Hello")

# 流式运行
result = Runner.run_streamed(agent, "Hello")
async for event in result.stream_events():
    print(event)
```

### 4. Handoffs（交接）
Agent 之间传递任务的机制。

```python
french_agent = Agent(name="French", instructions="只说法语")
spanish_agent = Agent(name="Spanish", instructions="只说西班牙语")

triage_agent = Agent(
    name="Triage",
    instructions="根据语言分配给合适的 agent",
    handoffs=[french_agent, spanish_agent],
)
```

### 5. Agents as Tools（Agent 作为工具）
将 Agent 封装为工具供其他 Agent 调用。

```python
translator = Agent(name="Translator", ...)

orchestrator = Agent(
    name="Orchestrator",
    tools=[
        translator.as_tool(
            tool_name="translate",
            tool_description="翻译文本"
        )
    ],
)
```

### 6. Guardrails（防护栏）
输入输出验证和安全检查。

```python
from agents import input_guardrail, GuardrailFunctionOutput

@input_guardrail
def check_input(ctx, agent, input):
    if "敏感词" in input:
        return GuardrailFunctionOutput(
            output_info="包含敏感内容",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(
        output_info="验证通过",
        tripwire_triggered=False
    )

agent = Agent(input_guardrails=[check_input])
```

### 7. Tracing（追踪）
内置的运行追踪和调试。

```python
from agents import trace

with trace("我的工作流"):
    result = await Runner.run(agent, "任务")
```

### 8. Sessions（会话）
自动管理对话历史。

```python
from agents import Session

session = Session()
result1 = await Runner.run(agent, "问题1", session=session)
result2 = await Runner.run(agent, "问题2", session=session)  # 记住问题1的上下文
```

## 快速开始

### 安装

```bash
# 使用 pip
pip install openai-agents

# 使用 uv
uv add openai-agents

# 带语音支持
pip install 'openai-agents[voice]'

# 带 Redis 会话支持
pip install 'openai-agents[redis]'
```

### 设置环境变量

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

### Hello World 示例

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
    )
    
    result = await Runner.run(agent, "Write a haiku about programming.")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## 常见设计模式

### 模式 1: 路由（Routing）
根据输入类型分配给不同的专业 Agent。

```python
sales_agent = Agent(name="Sales", instructions="处理销售相关咨询")
support_agent = Agent(name="Support", instructions="处理技术支持")
technical_agent = Agent(name="Technical", instructions="处理技术问题")

triage_agent = Agent(
    name="Triage",
    instructions="根据用户请求类型分配给合适的 agent",
    handoffs=[sales_agent, support_agent, technical_agent],
)
```

### 模式 2: 编排者（Orchestrator）
一个主 Agent 协调多个专业 Agent。

```python
researcher = Agent(name="Researcher", instructions="搜索和收集信息")
analyst = Agent(name="Analyst", instructions="分析数据")
writer = Agent(name="Writer", instructions="撰写报告")

orchestrator = Agent(
    name="Orchestrator",
    instructions="协调各个专业 agent 完成复杂任务",
    tools=[
        researcher.as_tool(tool_name="research", tool_description="搜索信息"),
        analyst.as_tool(tool_name="analyze", tool_description="分析数据"),
        writer.as_tool(tool_name="write", tool_description="撰写内容"),
    ],
)
```

### 模式 3: 并行执行（Parallelization）
多个 Agent 同时执行独立任务。

```python
import asyncio

async def parallel_workflow():
    results = await asyncio.gather(
        Runner.run(agent1, input),
        Runner.run(agent2, input),
        Runner.run(agent3, input),
    )
    return results
```

### 模式 4: 人机协作（Human in the Loop）
在关键决策点请求人工确认。

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="帮助用户做决策，在重要决策前请求确认",
)

# 使用流式输出来实现实时交互
result = Runner.run_streamed(agent, "帮我规划旅行")
async for event in result.stream_events():
    # 检测需要人工确认的事件
    if needs_human_approval(event):
        approval = await get_human_input()
        # 继续执行
```

## 高级功能

### 使用其他 LLM

SDK 支持通过 LiteLLM 接入 100+ LLM。

```python
from agents import Agent
from openai import AsyncOpenAI

# 使用 Anthropic Claude
claude_client = AsyncOpenAI(
    api_key="your-anthropic-key",
    base_url="https://api.anthropic.com/v1"
)

agent = Agent(
    name="ClaudeAgent",
    model="claude-3-opus-20240229",
    model_settings={"client": claude_client}
)
```

### Realtime Agents（语音 Agent）

```python
from agents import Agent, Runner
from agents.voice import VoiceAgent

voice_agent = VoiceAgent(
    name="VoiceAssistant",
    instructions="You are a helpful voice assistant",
)

# 实时语音交互
result = await Runner.run(voice_agent, audio_input)
```

### MCP（Model Context Protocol）

```python
from agents import Agent
from agents.mcp import MCPServer

mcp_server = MCPServer("path/to/mcp/config")

agent = Agent(
    name="MCPAgent",
    mcp_servers=[mcp_server],
)
```

## 最佳实践

### 1. 异步优先
推荐使用 `await Runner.run()` 而非 `Runner.run_sync()`。

### 2. 类型提示
使用 Pydantic 和 Annotated 提供清晰的类型信息。

```python
from pydantic import BaseModel, Field

class WeatherOutput(BaseModel):
    city: str = Field(description="城市名称")
    temperature: int = Field(description="温度（摄氏度）")
    conditions: str = Field(description="天气状况")

@function_tool
def get_weather(city: str) -> WeatherOutput:
    return WeatherOutput(city=city, temperature=20, conditions="晴朗")
```

### 3. 工具描述
为工具提供清晰的 docstring 和参数描述。

```python
@function_tool
def calculate(
    expression: Annotated[str, "数学表达式，如 '2+2' 或 'sqrt(16)'"]
) -> float:
    """
    计算数学表达式的结果。
    支持基本运算、三角函数、对数等。
    """
    return eval(expression)
```

### 4. 追踪调试
使用 `with trace()` 包裹工作流以便调试。

```python
from agents import trace

with trace("客户服务流程"):
    result = await Runner.run(customer_service_agent, user_query)
```

### 5. 错误处理
SDK 内置重试机制，可自定义重试策略。

```python
from agents import Agent, Runner

agent = Agent(
    name="RobustAgent",
    retry_config={
        "max_retries": 3,
        "retry_delay": 1.0,
    }
)
```

### 6. 资源清理
使用上下文管理器确保资源正确释放。

```python
async with AgentSession() as session:
    result = await Runner.run(agent, input, session=session)
```

## 完整示例

### 示例 1: 多语言客服系统

```python
import asyncio
from agents import Agent, Runner

# 创建专业 Agent
chinese_agent = Agent(
    name="中文客服",
    instructions="用中文提供客户服务",
    handoff_description="中文客服支持"
)

english_agent = Agent(
    name="English Support",
    instructions="Provide customer service in English",
    handoff_description="English support"
)

# 路由 Agent
triage_agent = Agent(
    name="Triage",
    instructions="根据用户语言分配给合适的客服",
    handoffs=[chinese_agent, english_agent],
)

async def main():
    result = await Runner.run(triage_agent, "你好，我需要帮助")
    print(f"当前 Agent: {result.current_agent.name}")
    print(f"回复: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 示例 2: 研究助手

```python
import asyncio
from agents import Agent, Runner, function_tool
from typing import Annotated

@function_tool
def search_web(query: Annotated[str, "搜索查询"]) -> str:
    """在网络上搜索信息"""
    # 实现搜索逻辑
    return f"搜索结果：{query}"

@function_tool
def analyze_data(data: Annotated[str, "要分析的数据"]) -> str:
    """分析数据并返回洞察"""
    # 实现分析逻辑
    return f"分析结果：{data}"

# 专业 Agent
researcher = Agent(
    name="Researcher",
    instructions="搜索和收集相关信息",
    tools=[search_web],
)

analyst = Agent(
    name="Analyst",
    instructions="分析数据并提供洞察",
    tools=[analyze_data],
)

writer = Agent(
    name="Writer",
    instructions="基于研究和分析撰写报告",
)

# 编排 Agent
orchestrator = Agent(
    name="ResearchOrchestrator",
    instructions="协调研究、分析和写作流程",
    tools=[
        researcher.as_tool(tool_name="research", tool_description="搜索信息"),
        analyst.as_tool(tool_name="analyze", tool_description="分析数据"),
        writer.as_tool(tool_name="write", tool_description="撰写报告"),
    ],
)

async def main():
    result = await Runner.run(
        orchestrator, 
        "研究人工智能的最新发展趋势并撰写报告"
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## 调试技巧

### 1. 查看完整对话历史

```python
result = await Runner.run(agent, input)
print(result.to_input_list())  # 完整对话历史
```

### 2. 检查当前 Agent

```python
print(result.current_agent)  # 当前运行的 agent
print(result.current_agent.name)  # Agent 名称
```

### 3. 追踪执行过程

```python
from agents import trace

with trace("调试工作流") as t:
    result = await Runner.run(agent, input)
    # 在 OpenAI 后台查看详细追踪信息
```

### 4. 流式调试

```python
result = Runner.run_streamed(agent, input)
async for event in result.stream_events():
    print(f"Event: {event.type}")
    if hasattr(event, 'data'):
        print(f"Data: {event.data}")
```

## 性能优化

### 1. 并行工具调用

```python
# SDK 自动并行调用独立的工具
agent = Agent(
    name="ParallelAgent",
    tools=[tool1, tool2, tool3],
    parallel_tool_calls=True,  # 启用并行调用
)
```

### 2. 缓存策略

```python
from agents import Agent

agent = Agent(
    name="CachedAgent",
    cache_settings={
        "enable_cache": True,
        "cache_ttl": 3600,  # 1小时
    }
)
```

### 3. 批处理

```python
async def batch_process(inputs):
    tasks = [Runner.run(agent, input) for input in inputs]
    results = await asyncio.gather(*tasks)
    return results
```

## 常见问题

### Q: 如何使用其他 LLM？
A: 通过 LiteLLM 配置其他模型提供商，详见"高级功能"部分。

### Q: 如何实现流式输出？
A: 使用 `Runner.run_streamed()` 并遍历 `stream_events()`。

### Q: 如何保存对话历史？
A: 使用 `Session` 功能自动管理历史。

### Q: 如何调试 Agent 行为？
A: 使用 `with trace()` 包裹代码，在 OpenAI 后台查看详细执行过程。

### Q: 如何限制 Agent 的输出格式？
A: 使用 Pydantic 模型定义输出类型。

```python
from pydantic import BaseModel

class Output(BaseModel):
    summary: str
    confidence: float

agent = Agent(
    name="StructuredAgent",
    output_type=Output,
)
```

## 学习资源

- 📖 官方文档: https://openai.github.io/openai-agents-python/
- 💻 GitHub: https://github.com/openai/openai-agents-python
- 📦 PyPI: https://pypi.org/project/openai-agents/
- 🎓 示例代码: https://github.com/openai/openai-agents-python/tree/main/examples

## 版本要求

- Python >= 3.10
- openai-agents >= 0.1.0

## 相关技能

- `find-skills` - 查找和安装其他技能
- `file-sync` - 同步文件到集中存储

---

**注意**: 使用此技能需要有效的 OpenAI API Key 或其他支持的 LLM API Key。
