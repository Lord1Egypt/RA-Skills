---
name: multi-llm-adapter
description: Universal adapter for multiple LLM providers. Unified interface for OpenAI, Anthropic, Google Gemini, Ollama, and 100+ providers via LiteLLM. Automatic fallback and load balancing.
tools:
  - read
  - write
  - exec
---

# Multi-LLM Adapter - 多 LLM 适配器

统一接口调用多个 LLM 提供商，支持自动故障转移和负载均衡。

**Version**: 1.0.0  
**Features**: 统一接口、多提供商支持、自动回退、负载均衡、流式响应

## Purpose

让 OpenClaw 能够:
- 用统一接口调用不同 LLM
- 自动在多个提供商间切换
- 比较不同模型的响应
- 降低单点故障风险

## Quick Start

### 1. 配置 Providers

```bash
# 设置 API Keys
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GEMINI_API_KEY=...
export OLLAMA_HOST=http://localhost:11434
```

### 2. 基本使用

```bash
# 使用 OpenAI
python3 scripts/main.py chat --provider openai --model gpt-4 "Hello"

# 使用 Claude
python3 scripts/main.py chat --provider anthropic --model claude-3-opus "Hello"

# 使用本地 Ollama
python3 scripts/main.py chat --provider ollama --model llama2 "Hello"

# 自动选择 (按优先级)
python3 scripts/main.py chat --auto "Hello"
```

### 3. 带 Tools 的调用

```bash
python3 scripts/main.py chat \
  --provider openai \
  --model gpt-4 \
  --tools tools.json \
  --message "What's the weather in Beijing?"
```

## Python API

```python
from multi_llm_adapter import LLMClient, ProviderConfig

# 初始化客户端
client = LLMClient()

# 添加 providers
client.add_provider(ProviderConfig(
    name="openai",
    api_key="sk-...",
    model="gpt-4",
    priority=1
))

client.add_provider(ProviderConfig(
    name="anthropic", 
    api_key="sk-ant-...",
    model="claude-3-opus",
    priority=2
))

# 简单调用
response = client.chat(
    messages=[{"role": "user", "content": "Hello"}],
    provider="openai"
)

# 自动选择 provider
response = client.chat_auto(
    messages=[{"role": "user", "content": "Hello"}]
)

# 带工具调用
response = client.chat(
    messages=[...],
    tools=[...],
    provider="anthropic"
)

# 流式响应
for chunk in client.chat_stream(messages=[...]):
    print(chunk.content, end="")
```

## Supported Providers

| Provider | Models | Features |
|----------|--------|----------|
| OpenAI | GPT-4, GPT-3.5 | Tools, Vision, JSON |
| Anthropic | Claude 3, Claude 2 | Tools, Vision |
| Google | Gemini Pro, Ultra | Tools, Vision |
| Ollama | Llama, Mistral | Local, Tools |
| Azure | GPT-4, GPT-3.5 | Enterprise |
| AWS Bedrock | Claude, Llama | AWS Native |
| Cohere | Command, Generate | RAG |
| Mistral | Mistral Large | OpenAI-compatible |

## CLI Reference

### Chat

```bash
# 基本对话
python3 scripts/main.py chat --message "Hello"

# 指定 provider
python3 scripts/main.py chat \
  --provider anthropic \
  --model claude-3-haiku \
  --message "Hello"

# 多轮对话
python3 scripts/main.py chat \
  --provider openai \
  --system "You are a helpful assistant" \
  --message "Hello" \
  --message "How are you?"

# 流式输出
python3 scripts/main.py chat \
  --provider openai \
  --message "Tell me a story" \
  --stream
```

### Tools

```bash
# 使用工具
python3 scripts/main.py chat \
  --provider openai \
  --tools tools.json \
  --message "Search for Python tutorials"

# 查看工具调用结果
python3 scripts/main.py chat \
  --provider anthropic \
  --tools tools.json \
  --message "Get weather in Tokyo" \
  --execute-tools
```

### Compare

```bash
# 比较多个模型的回答
python3 scripts/main.py compare \
  --providers openai,anthropic,google \
  --message "Explain quantum computing"

# 输出为 JSON
python3 scripts/main.py compare \
  --providers openai,ollama \
  --message "Hello" \
  --output json
```

### Manage Providers

```bash
# 列出配置的 providers
python3 scripts/main.py providers list

# 测试连接
python3 scripts/main.py providers test --name openai

# 添加 provider
python3 scripts/main.py providers add \
  --name my-ollama \
  --type ollama \
  --host http://localhost:11434 \
  --model llama2

# 设置优先级
python3 scripts/main.py providers prioritize \
  --name openai \
  --priority 1
```

## Configuration

```yaml
# config.yaml
providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4
    priority: 1
    timeout: 30
    
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-3-opus
    priority: 2
    timeout: 30
    
  ollama:
    host: http://localhost:11434
    model: llama2
    priority: 3
    timeout: 60

retry:
  max_attempts: 3
  fallback_enabled: true

load_balance:
  strategy: round_robin  # or priority, random
```

## Advanced Features

### Fallback Chain

```python
# 按优先级自动回退
response = client.chat_with_fallback(
    messages=[...],
    fallback_order=["openai", "anthropic", "ollama"]
)
```

### Load Balancing

```python
# 轮询多个相同 provider 的实例
client.enable_load_balancing("openai", [
    {"api_key": "key1"},
    {"api_key": "key2"}
])
```

### Cost Tracking

```python
# 追踪调用成本
response = client.chat(...)
print(f"Cost: ${response.cost_usd}")
print(f"Tokens: {response.total_tokens}")
```

## Architecture

```
multi-llm-adapter/
├── SKILL.md
├── requirements.txt
├── lib/
│   ├── __init__.py
│   ├── client.py            # LLMClient 核心
│   ├── config.py            # 配置管理
│   ├── providers/           # Provider 实现
│   │   ├── __init__.py
│   │   ├── base.py          # BaseProvider
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── gemini.py
│   │   ├── ollama.py
│   │   └── litellm.py       # LiteLLM 统一接口
│   ├── fallback.py          # 故障转移
│   ├── load_balancer.py     # 负载均衡
│   └── cost_tracker.py      # 成本追踪
├── scripts/
│   └── main.py              # CLI 入口
└── examples/
    ├── basic_chat.py
    ├── with_tools.py
    └── fallback_demo.py
```

## Integration with OpenClaw

```python
from multi_llm_adapter import LLMClient

class MySkill:
    def __init__(self):
        self.llm = LLMClient()
        self.llm.load_config("config.yaml")
    
    def ask_llm(self, prompt: str):
        # 自动选择最佳 provider
        response = self.llm.chat_auto([
            {"role": "user", "content": prompt}
        ])
        return response.content
    
    def compare_models(self, prompt: str):
        return self.llm.compare(
            prompt,
            providers=["openai", "anthropic"]
        )
```

## Use Cases

1. **高可用** - Provider 故障自动切换
2. **成本控制** - 优先使用便宜模型
3. **性能优化** - 根据任务选择模型
4. **A/B 测试** - 比较不同模型效果

## License

MIT License
