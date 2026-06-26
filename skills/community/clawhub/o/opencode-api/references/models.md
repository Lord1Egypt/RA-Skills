# 模型速查

## OpenCode 原生支援

OpenCode 使用 AI SDK + Models.dev，支援 75+ LLM 提供商。

### 設定模型

```json
{
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5"
}
```

`small_model` 用於標題生成等輕量任務，節省成本。

### 常用模型 ID 格式

| Provider | 格式 | 範例 |
|----------|------|------|
| Anthropic | `anthropic/model-id` | `anthropic/claude-sonnet-4-5` |
| OpenAI | `openai/model-id` | `openai/gpt-4o` |
| OpenRouter | `openrouter/model-id` | `openrouter/anthropic/claude-sonnet-4-5` |
| MiniMax | `minimax/model-id` | `minimax/MiniMax-M2.7` |
| Ollama（本地）| `ollama/model-id` | `ollama/llama2` |
| LM Studio（本地）| `lmstudio/model-id` | `lmstudio/gemma-3n` |

### 思考深度（reasoningEffort）

| 值 | 說明 |
|----|------|
| `none` | 關閉思考 |
| `minimal` | 輕量思考 |
| `medium` | 標準（預設）|
| `high` | 深度分析 |
| `xhigh` | 極深度推理 |

### 本地模型設定

**Ollama**：
```json
{
  "provider": {
    "ollama": {
      "options": { "baseURL": "http://localhost:11434/v1" }
    }
  }
}
```

**LM Studio**：
```json
{
  "provider": {
    "lmstudio": {
      "options": { "baseURL": "http://127.0.0.1:1234/v1" }
    }
  }
}
```

### 模型限制設定

```json
{
  "provider": {
    "myprovider": {
      "models": {
        "my-model": {
          "limit": {
            "context": 128000,
            "output": 65536
          }
        }
      }
    }
  }
}
```

### 查看可用模型

```python
from opencode_api import OpenCodeClient
client = OpenCodeClient()
providers = client.get_providers()
print(providers["providers"])   # 所有 provider
print(providers["default"])      # 預設模型
```

或透過 CLI：
```bash
opencode models
```

### OpenCode Zen

OpenCode 團隊驗證過的模型列表，可透過 `/connect` 指令設定。

### Provider 特定選項

**Anthropic**：
```json
{
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 600000,
        "setCacheKey": true
      }
    }
  }
}
```

**Amazon Bedrock**：
```json
{
  "provider": {
    "amazon-bedrock": {
      "options": {
        "region": "us-east-1",
        "profile": "my-aws-profile",
        "endpoint": "https://..."
      }
    }
  }
}
```
