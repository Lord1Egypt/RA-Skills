---
name: llm-tools
description: Universal Tool Definition System for LLM function calling. Define tools once, use with any LLM provider (OpenAI, Anthropic, Gemini, etc.). JSON Schema validation and automatic format conversion.
tools:
  - read
  - write
  - exec
---

# LLM Tools - 通用工具定义系统

基于 Bytebot Tool Definition 模式实现的 LLM 函数调用工具定义系统。

**Version**: 1.0.0  
**Features**: JSON Schema 定义、多 LLM 格式转换、工具注册中心、参数验证

## Purpose

让 OpenClaw 能够:
- 用统一格式定义 LLM 可调用的工具
- 自动转换为不同 LLM 提供商的格式
- 验证工具调用参数
- 管理工具注册和发现

## Quick Start

### 1. 定义工具

```python
from llm_tools import ToolRegistry, Tool

# 创建工具注册表
registry = ToolRegistry()

# 定义工具
@registry.register(
    name="get_weather",
    description="Get current weather for a location",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "default": "celsius"
            }
        },
        "required": ["location"]
    }
)
def get_weather(location: str, unit: str = "celsius"):
    return {"temperature": 22, "unit": unit}
```

### 2. 转换为不同 LLM 格式

```python
# OpenAI format
openai_tools = registry.to_openai()

# Anthropic format  
anthropic_tools = registry.to_anthropic()

# Google Gemini format
gemini_tools = registry.to_gemini()

# Ollama format
ollama_tools = registry.to_ollama()
```

### 3. 验证工具调用

```python
# 验证参数
is_valid, error = registry.validate_call(
    "get_weather",
    {"location": "Beijing", "unit": "celsius"}
)

# 执行工具
result = registry.execute("get_weather", {"location": "Beijing"})
```

## CLI Usage

### 转换工具格式

```bash
# 从 JSON 定义转换
python3 scripts/main.py convert --input tools.json --format openai
python3 scripts/main.py convert --input tools.json --format anthropic

# 验证工具定义
python3 scripts/main.py validate --input tools.json

# 列出所有工具
python3 scripts/main.py list --input tools.json
```

### 工具定义 JSON 格式

```json
{
  "tools": [
    {
      "name": "search_web",
      "description": "Search the web for information",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "Search query"
          },
          "limit": {
            "type": "integer",
            "default": 10
          }
        },
        "required": ["query"]
      }
    }
  ]
}
```

## Supported LLM Formats

| Provider | Format | Features |
|----------|--------|----------|
| OpenAI | Function Calling | `tools` / `functions` |
| Anthropic | Tool Use | `computer_*` 命名空间 |
| Google | Function Calling | `function_declarations` |
| Ollama | Tools | Native tool support |
| Mistral | Function Calling | OpenAI-compatible |
| Cohere | Tool Use | Custom format |

## Installation

```bash
pip3 install -r requirements.txt
```

## API Reference

### ToolRegistry

```python
from llm_tools import ToolRegistry

registry = ToolRegistry()

# 注册工具
registry.register_tool(tool_definition)

# 装饰器方式
@registry.register(name="...", description="...", parameters={...})
def my_tool():
    pass

# 批量注册
registry.register_from_dict({"tools": [...]})
registry.register_from_json_file("tools.json")

# 导出格式
openai_format = registry.to_openai()
anthropic_format = registry.to_anthropic()
gemini_format = registry.to_gemini()
ollama_format = registry.to_ollama()

# 验证和执行
registry.validate_call(name, arguments)
registry.execute(name, arguments)
```

### Tool Definition

```python
from llm_tools import Tool

tool = Tool(
    name="calculate",
    description="Perform mathematical calculation",
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string"}
        },
        "required": ["expression"]
    },
    handler=lambda expr: eval(expr)  # 可选
)
```

## Integration with OpenClaw

在 Skill 中使用:

```python
from llm_tools import ToolRegistry

class MySkill:
    def __init__(self):
        self.tools = ToolRegistry()
        
        @self.tools.register(name="read_file", ...)
        def read_file(path: str):
            return Path(path).read_text()
    
    def get_llm_tools(self, provider: str):
        if provider == "openai":
            return self.tools.to_openai()
        elif provider == "anthropic":
            return self.tools.to_anthropic()
```

## Architecture

```
llm-tools/
├── SKILL.md
├── requirements.txt
├── lib/
│   ├── __init__.py
│   ├── registry.py          # ToolRegistry 核心
│   ├── tool.py              # Tool 类定义
│   ├── formats/
│   │   ├── __init__.py
│   │   ├── openai.py        # OpenAI 格式转换
│   │   ├── anthropic.py     # Anthropic 格式转换
│   │   ├── gemini.py        # Google Gemini 格式
│   │   └── ollama.py        # Ollama 格式
│   └── validators.py        # JSON Schema 验证
├── scripts/
│   └── main.py              # CLI 入口
└── examples/
    ├── tools.json           # 示例工具定义
    └── registry_example.py  # 注册表示例
```

## Use Cases

1. **多 LLM 支持** - 一次定义，多处使用
2. **工具共享** - 在 Skills 间共享工具定义
3. **参数验证** - 自动验证 LLM 输出的参数
4. **格式转换** - 迁移到不同 LLM 提供商

## License

MIT License - 基于 Bytebot Tool Definition 模式实现
