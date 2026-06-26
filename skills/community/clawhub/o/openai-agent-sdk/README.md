# OpenAI Agent SDK 技能

这是为 CoPaw Worker Agent 创建的 OpenAI Agent SDK 技能包。

## 技能信息

- **名称**: openai-agent-sdk
- **版本**: 1.0.0
- **作者**: mathematician
- **描述**: 使用 OpenAI Agents SDK 构建多 Agent AI 系统

## 安装要求

- Python >= 3.10
- openai-agents >= 0.1.0

## 目录结构

```
openai-agent-sdk/
├── SKILL.md              # 技能主文档
├── README.md             # 本文件
├── examples/             # 示例代码
│   ├── basic_agent.py
│   ├── tools_example.py
│   └── handoffs_example.py
└── templates/            # 模板文件
    ├── agent_template.py
    └── multi_agent_template.py
```

## 使用方法

1. 阅读 SKILL.md 了解核心概念和 API
2. 查看 examples/ 目录中的示例代码
3. 使用 templates/ 中的模板快速开始

## 快速开始

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="助手", instructions="你是一个有帮助的助手")
    result = await Runner.run(agent, "你好")
    print(result.final_output)

asyncio.run(main())
```

## 学习资源

- 官方文档: https://openai.github.io/openai-agents-python/
- GitHub: https://github.com/openai/openai-agents-python

## 许可证

MIT License
