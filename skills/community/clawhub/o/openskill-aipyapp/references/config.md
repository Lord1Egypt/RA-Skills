# AIPyApp 配置模板

## OpenAI 配置

```toml
[llm.openai]
type = "openai"
api_key = "sk-your-key"
base_url = "https://api.openai.com/v1"
model = "gpt-4"
enable = true
default = true
```

## 自定义 OpenAI 兼容端点

```toml
[llm.custom]
type = "openai"
api_key = "your-key"
base_url = "https://your-proxy.com/v1"
model = "gpt-4"
enable = true
default = true
```

## Anthropic Claude

```toml
[llm.anthropic]
type = "anthropic"
api_key = "sk-ant-your-key"
model = "claude-3-sonnet-20240229"
enable = false
```

## TrustToken

```toml
[llm.trustoken]
type = "trust"
api_key = "your-tt-key"
base_url = "https://sapi.trustoken.ai/v1"
model = "auto"
enable = false
```

## 完整配置示例

```toml
workdir = "work"
share_result = true
auto_install = true

[llm.openai]
type = "openai"
api_key = "sk-xxx"
base_url = "https://api.openai.com/v1"
model = "gpt-4"
enable = true
default = true

[context_manager]
strategy = "hybrid"
max_tokens = 100000
max_rounds = 10
```
