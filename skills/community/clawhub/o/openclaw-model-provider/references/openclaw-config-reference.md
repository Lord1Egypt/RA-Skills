# OpenClaw 模型提供商配置参考

## 完整配置结构

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "provider/model-id"
      },
      "models": {
        "provider/model-id": {
          "params": {
            "temperature": 0.7,
            "maxTokens": 4096,
            "fastMode": false,
            "transport": "auto"
          }
        }
      }
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "provider-name": {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "${ENV_VAR}",
        "api": "openai-completions",
        "models": [
          {
            "id": "model-id",
            "name": "Display Name",
            "api": "openai-completions",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  },
  "env": {
    "ENV_VAR": "actual-api-key"
  }
}
```

## API 类型说明

| API 类型 | 说明 | 适用场景 |
|---------|------|----------|
| `openai-completions` | OpenAI 兼容接口 | 大多数第三方代理、OpenRouter、本地模型 |
| `anthropic-messages` | Anthropic 兼容接口 | Claude API、部分兼容代理 |

## 字段详解

### models.providers.{provider}

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `baseUrl` | string | 是 | API 基础地址，以 /v1 结尾 |
| `apiKey` | string | 是 | API 密钥，建议使用 `${ENV_VAR}` 格式引用环境变量 |
| `api` | string | 是 | API 类型，`openai-completions` 或 `anthropic-messages` |
| `models` | array | 是 | 该提供商下的模型列表 |

### models.providers.{provider}.models[]{}

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 模型 ID，用于 API 调用 |
| `name` | string | 否 | 显示名称 |
| `api` | string | 否 | 覆盖 provider 级别的 API 类型 |
| `reasoning` | boolean | 否 | 是否支持推理/thinking 模式 |
| `input` | array | 否 | 支持的输入类型，如 `["text", "image"]` |
| `contextWindow` | number | 否 | 上下文窗口大小（tokens） |
| `maxTokens` | number | 否 | 最大输出 token 数 |
| `cost` | object | 否 | 价格信息 |

### agents.defaults.model

| 字段 | 类型 | 说明 |
|------|------|------|
| `primary` | string | 默认主模型，格式 `provider/model-id` |

### agents.defaults.models.{model-ref}

| 字段 | 类型 | 说明 |
|------|------|------|
| `params` | object | 该模型的默认参数 |
| `params.temperature` | number | 温度参数 |
| `params.maxTokens` | number | 最大 token 数 |
| `params.fastMode` | boolean | 快速模式（部分提供商支持） |
| `params.transport` | string | 传输方式：`sse`, `websocket`, `auto` |

## 环境变量优先级

OpenClaw 支持多种方式设置 API Key，优先级从高到低：

1. `OPENCLAW_LIVE_{PROVIDER}_KEY` - 最高优先级，单个覆盖
2. `{PROVIDER}_API_KEYS` - 逗号分隔的密钥列表，支持轮换
3. `{PROVIDER}_API_KEY` - 主密钥
4. `{PROVIDER}_API_KEY_1`, `{PROVIDER}_API_KEY_2`... - 编号列表
5. 配置文件中 `env` 字段定义的值

## 常见错误

### 1. JSON 语法错误
```bash
# 使用 jq 验证
jq '.' ~/.openclaw/openclaw.json
```

### 2. API Key 未找到
- 确认环境变量已正确导出
- 检查变量名拼写
- 确认 OpenClaw 进程能访问该环境变量

### 3. 模型不存在
- 运行 `openclaw models list` 确认模型已加载
- 检查 `models.providers` 配置是否正确合并
- 确认 `mode` 设置为 `merge` 而非 `replace`

### 4. 连接失败
- 检查 `baseUrl` 是否正确
- 确认网络可以访问该地址
- 检查 API Key 是否有调用权限

## 内置提供商列表

以下提供商无需 `models.providers` 配置，直接设置 API Key 即可：

- `openai` - OPENAI_API_KEY
- `anthropic` - ANTHROPIC_API_KEY
- `moonshot` - MOONSHOT_API_KEY
- `zai` - ZAI_API_KEY
- `google` - GEMINI_API_KEY
- `openrouter` - OPENROUTER_API_KEY
- `groq` - GROQ_API_KEY
- `together` - TOGETHER_API_KEY
- 等...
