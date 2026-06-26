# 支持的AI平台列表（OpenAI兼容接口）

## 目录
- [主力层（primary）](#主力层primary)
- [每日回血层（daily）](#每日回血层daily)
- [兜底层（fallback）](#兜底层fallback)
- [接口标准化说明](#接口标准化说明)
- [平台对比](#平台对比)

## 主力层（primary）

### 阿里云百炼（DashScope）

**特点：** 初始赠送额度极大，适合处理大部分日常任务

**支持的模型：**
- qwen-max
- qwen-plus
- qwen-turbo

**API Key获取方式：**
1. 访问 [阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. 创建API Key
3. 复制生成的Key（格式：`sk-xxxxxxxxxxxxxxxx`）

**配置示例：**
```yaml
alibaba_bailian:
  tier: primary
  model: "qwen-max"
  api_keys:
    - "sk-xxxxxxxxxxxxxxxx"
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

**OpenAI兼容接口：**
- 端点：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- 文档：[OpenAI兼容接口文档](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope)

**速率限制：**
- Qwen-Max：约100请求/分钟
- 具体限制取决于账户类型

### 智谱AI（BigModel）

**特点：** 国产大模型，初始赠送额度大

**支持的模型：**
- glm-4
- glm-3-turbo
- glm-4-air

**API Key获取方式：**
1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册账号，创建API Key
3. 复制生成的Key

**配置示例：**
```yaml
zhipu:
  tier: primary
  model: "glm-4"
  api_keys:
    - "xxxxxxxxxxxxxxxx"
  base_url: "https://open.bigmodel.cn/api/paas/v4"
```

**OpenAI兼容接口：**
- 端点：`https://open.bigmodel.cn/api/paas/v4/chat/completions`
- 文档：[智谱AI API文档](https://open.bigmodel.cn/dev/api#glm-4)

**速率限制：**
- GLM-4：约20请求/分钟
- 具体限制取决于账户类型

### 小龙虾（XiaoLongXia）

**特点：** 专为大模型推理优化，性价比高

**支持的模型：**
- xiaolongxia-72b
- xiaolongxia-34b
- xiaolongxia-14b

**API Key获取方式：**
1. 访问小龙虾官网获取API Key
2. 注册账号，创建API Key
3. 复制生成的Key

**配置示例：**
```yaml
xiaolongxia:
  tier: primary
  model: "xiaolongxia-72b"
  api_keys:
    - "your_api_key"
  base_url: "https://api.xiaolongxia.com/v1"
```

**OpenAI兼容接口：**
- 端点：`https://api.xiaolongxia.com/v1/chat/completions`
- 支持标准OpenAI格式

**速率限制：**
- 根据套餐不同，限制不同
- 具体限制取决于账户类型

## 每日回血层（daily）

### 火山引擎（字节跳动）

**特点：** 额度每日刷新，稳定可用

**支持的模型：**
- doubao-pro-256k
- doubao-pro-32k
- doubao-lite-32k

**API Key获取方式：**
1. 访问 [火山引擎控制台](https://console.volcengine.com/ark)
2. 创建应用并获取API Key
3. 配置推理接入点

**配置示例：**
```yaml
volcengine:
  tier: daily
  model: "doubao-pro-256k"
  api_keys:
    - "xxxxxxxxxxxxxxxx"
  base_url: "https://ark.cn-beijing.volces.com/api/v3"
```

**OpenAI兼容接口：**
- 端点：`https://ark.cn-beijing.volces.com/api/v3/chat/completions`
- 文档：[火山引擎API文档](https://www.volcengine.com/docs/82379)

**速率限制：**
- 每日免费额度：根据账户类型
- 超出后按量计费

### Google AI Studio

**特点：** 每日免费额度，Gemini模型质量高

**支持的模型：**
- gemini-1.5-pro
- gemini-1.5-flash

**API Key获取方式：**
1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 创建API Key
3. 复制生成的Key（格式：`AIzaSyxxxxxxxx`）

**配置示例：**
```yaml
google_aistudio:
  tier: daily
  model: "gemini-1.5-pro"
  api_keys:
    - "AIzaSyxxxxxxxxxxxxxxxx"
  base_url: "https://generativelanguage.googleapis.com/v1beta"
```

**注意：** Google Gemini的API Key需要作为URL参数传递，需要特殊处理

**速率限制：**
- 每日免费额度：15请求/分钟（Gemini 1.5 Pro）
- 具体限制取决于账户类型

## 兜底层（fallback）

### 硅基流动（SiliconFlow）

**特点：** 提供大量开源模型，支持免费额度

**支持的模型：**
- Qwen/Qwen2.5-7B-Instruct
- meta-llama/Llama-3.1-8B-Instruct
- THUDM/glm-4-9b-chat

**API Key获取方式：**
1. 访问 [硅基流动官网](https://siliconflow.cn/)
2. 注册账号，创建API Key
3. 复制生成的Key（格式：`sk-xxxxxxxx`）

**配置示例：**
```yaml
siliconflow:
  tier: fallback
  model: "Qwen/Qwen2.5-7B-Instruct"
  api_keys:
    - "sk-xxxxxxxxxxxxxxxx"
  base_url: "https://api.siliconflow.cn/v1"
```

**OpenAI兼容接口：**
- 端点：`https://api.siliconflow.cn/v1/chat/completions`
- 文档：[硅基流动API文档](https://docs.siliconflow.cn/docs)

**速率限制：**
- 免费额度：每日一定额度
- 超出后按量计费

### OpenCode

**特点：** 专注代码生成的AI平台

**支持的模型：**
- opencode-72b
- opencode-34b
- opencode-14b

**API Key获取方式：**
1. 访问OpenCode官网
2. 注册账号，创建API Key
3. 复制生成的Key

**配置示例：**
```yaml
opencode:
  tier: fallback
  model: "opencode-72b"
  api_keys:
    - "your_api_key"
  base_url: "https://api.opencode.com/v1"
```

**OpenAI兼容接口：**
- 端点：`https://api.opencode.com/v1/chat/completions`
- 支持标准OpenAI格式

**速率限制：**
- 根据套餐不同，限制不同
- 具体限制取决于账户类型

### Qwen（通义千问独立API）

**特点：** 阿里云通义千问独立API，与百炼平台分开

**支持的模型：**
- qwen-max
- qwen-plus
- qwen-turbo
- qwen-long

**API Key获取方式：**
1. 访问通义千问官网
2. 注册账号，创建API Key
3. 复制生成的Key

**配置示例：**
```yaml
qwen:
  tier: fallback
  model: "qwen-max"
  api_keys:
    - "sk-xxxxxxxxxxxxxxxx"
  base_url: "https://api.qwen.ai/v1"
```

**OpenAI兼容接口：**
- 端点：`https://api.qwen.ai/v1/chat/completions`
- 支持标准OpenAI格式

**速率限制：**
- 免费额度：每日一定额度
- 超出后按量计费

### ClaudeCode

**特点：** Anthropic Claude代码专用版本

**支持的模型：**
- claude-3-5-sonnet-20241022
- claude-3-opus-20240229
- claude-3-sonnet-20240229

**API Key获取方式：**
1. 访问Anthropic控制台
2. 创建API Key
3. 复制生成的Key（格式：`sk-ant-xxxxxxxx`）

**配置示例：**
```yaml
claudecode:
  tier: fallback
  model: "claude-3-5-sonnet-20241022"
  api_keys:
    - "sk-ant-xxxxxxxxxxxxxxxx"
  base_url: "https://api.anthropic.com/v1"
```

**OpenAI兼容接口：**
- 端点：`https://api.anthropic.com/v1/messages`
- 需要特殊处理：使用`x-api-key`头而不是`Authorization: Bearer`
- 需要添加`anthropic-version: 2023-06-01`头

**速率限制：**
- Claude 3.5 Sonnet：约50请求/分钟
- 具体限制取决于账户类型

**注意：** ClaudeCode使用Anthropic的Messages API，虽然兼容OpenAI格式，但需要特殊的请求头处理

### OpenRouter

**特点：** 聚合多个模型，提供免费模型

**支持的模型：**
- meta-llama/llama-3.1-8b-instruct:free
- mistralai/mistral-7b-instruct:free
- google/gemma-7b-it:free

**API Key获取方式：**
1. 访问 [OpenRouter官网](https://openrouter.ai/)
2. 注册账号，创建API Key
3. 复制生成的Key（格式：`sk-or-xxxxxxxx`）

**配置示例：**
```yaml
openrouter:
  tier: fallback
  model: "meta-llama/llama-3.1-8b-instruct:free"
  api_keys:
    - "sk-or-xxxxxxxxxxxxxxxx"
  base_url: "https://openrouter.ai/api/v1"
```

**OpenAI兼容接口：**
- 端点：`https://openrouter.ai/api/v1/chat/completions`
- 文档：[OpenRouter API文档](https://openrouter.ai/docs/quick-start)

**速率限制：**
- 免费模型：有限制
- 付费模型：更高配额

### GitHub Models

**特点：** GitHub官方模型服务

**支持的模型：**
- gpt-4o
- gpt-4o-mini
- 其他开源模型

**API Key获取方式：**
1. 访问 [GitHub Marketplace](https://github.com/marketplace/models)
2. 获取GitHub Token
3. 配置模型访问权限

**配置示例：**
```yaml
github_models:
  tier: fallback
  model: "gpt-4o"
  api_keys:
    - "ghp_xxxxxxxxxxxxxxxx"
  base_url: "https://models.inference.ai.azure.com"
```

**OpenAI兼容接口：**
- 端点：`https://models.inference.ai.azure.com/chat/completions`
- 文档：[GitHub Models文档](https://docs.github.com/en/rest/models)

### Groq

**特点：** 极速推理，免费额度

**支持的模型：**
- llama3.1-70b-versatile
- llama3.1-8b-instant
- mixtral-8x7b-32768

**API Key获取方式：**
1. 访问 [Groq官网](https://groq.com/)
2. 注册账号，创建API Key
3. 复制生成的Key（格式：`gsk_xxxxxxxxxxxxxxxx`）

**配置示例：**
```yaml
groq:
  tier: fallback
  model: "llama3.1-70b-versatile"
  api_keys:
    - "gsk_xxxxxxxxxxxxxxxx"
  base_url: "https://api.groq.com/openai/v1"
```

**OpenAI兼容接口：**
- 端点：`https://api.groq.com/openai/v1/chat/completions`
- 文档：[Groq API文档](https://console.groq.com/docs)

**速率限制：**
- 免费层：30请求/分钟
- 付费层：更高配额

### 腾讯混元

**特点：** 腾讯出品，支持免费额度

**支持的模型：**
- hunyuan-lite
- hunyuan-standard
- hunyuan-pro

**API Key获取方式：**
1. 访问 [腾讯云混元](https://cloud.tencent.com/product/hunyuan)
2. 开通服务，获取SecretId和SecretKey
3. 生成API Key

**配置示例：**
```yaml
tencent_hunyuan:
  tier: fallback
  model: "hunyuan-lite"
  api_keys:
    - "xxxxxxxxxxxxxxxx"
  base_url: "https://hunyuan.tencentcloudapi.com/v1"
```

**注意：** 腾讯混元需要使用特殊的签名方式，可能需要适配

**速率限制：**
- 免费额度：每日一定额度
- 超出后按量计费

## 接口标准化说明

本Skill优先使用**OpenAI兼容接口**，所有配置的平台都应提供OpenAI兼容的API端点。

### 统一请求格式

```http
POST {base_url}/chat/completions
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "model": "model_name",
  "messages": [
    {"role": "system", "content": "系统提示词"},
    {"role": "user", "content": "用户提示词"}
  ],
  "temperature": 0.7,
  "max_tokens": 2000
}
```

### 统一响应格式

```json
{
  "choices": [
    {
      "message": {
        "content": "响应内容",
        "role": "assistant"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### 异常处理

重点监听以下错误码：

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 429 | Too Many Requests | 立即冷却Key，切换到下一个Key |
| 401 | Unauthorized | 永久禁用该Key |
| 500 | Internal Server Error | 短暂重试（最多3次） |
| 503 | Service Unavailable | 短暂重试（最多3次） |

## 平台对比

| 平台 | 层级 | 模型质量 | 速率限制 | 价格 | OpenAI兼容 |
|------|------|---------|---------|------|-----------|
| 阿里云百炼 | primary | ⭐⭐⭐⭐⭐ | 高 | 中 | ✓ |
| 智谱AI | primary | ⭐⭐⭐⭐ | 中 | 中 | ✓ |
| 小龙虾 | primary | ⭐⭐⭐⭐ | 高 | 中 | ✓ |
| 火山引擎 | daily | ⭐⭐⭐⭐ | 每日刷新 | 中 | ✓ |
| Google AI Studio | daily | ⭐⭐⭐⭐⭐ | 每日刷新 | 中 | 部分 |
| 硅基流动 | fallback | ⭐⭐⭐ | 中 | 低 | ✓ |
| OpenRouter | fallback | ⭐⭐⭐⭐ | 中 | 低 | ✓ |
| GitHub Models | fallback | ⭐⭐⭐⭐ | 中 | 低 | ✓ |
| Groq | fallback | ⭐⭐⭐⭐ | 高 | 低 | ✓ |
| 腾讯混元 | fallback | ⭐⭐⭐ | 中 | 低 | 部分 |
| OpenCode | fallback | ⭐⭐⭐⭐ | 中 | 低 | ✓ |
| Qwen独立API | fallback | ⭐⭐⭐⭐⭐ | 中 | 低 | ✓ |
| ClaudeCode | fallback | ⭐⭐⭐⭐⭐ | 中 | 高 | 特殊 |

## 配置建议

### 最小配置（3个平台）
```yaml
providers:
  alibaba_bailian:
    tier: primary
    model: "qwen-max"
    api_keys: ["sk-xxx"]
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"

  volcengine:
    tier: daily
    model: "doubao-pro-256k"
    api_keys: ["sk-xxx"]
    base_url: "https://ark.cn-beijing.volces.com/api/v3"

  siliconflow:
    tier: fallback
    model: "Qwen/Qwen2.5-7B-Instruct"
    api_keys: ["sk-xxx"]
    base_url: "https://api.siliconflow.cn/v1"
```

### 推荐配置（5个平台）
```yaml
providers:
  # 主力层
  alibaba_bailian:
    tier: primary
    model: "qwen-max"
    api_keys: ["sk-xxx1", "sk-xxx2"]
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"

  zhipu:
    tier: primary
    model: "glm-4"
    api_keys: ["sk-xxx"]
    base_url: "https://open.bigmodel.cn/api/paas/v4"

  # 每日回血层
  volcengine:
    tier: daily
    model: "doubao-pro-256k"
    api_keys: ["sk-xxx"]
    base_url: "https://ark.cn-beijing.volces.com/api/v3"

  google_aistudio:
    tier: daily
    model: "gemini-1.5-pro"
    api_keys: ["AIzaSyxxx"]
    base_url: "https://generativelanguage.googleapis.com/v1beta"

  # 兜底层
  siliconflow:
    tier: fallback
    model: "Qwen/Qwen2.5-7B-Instruct"
    api_keys: ["sk-xxx"]
    base_url: "https://api.siliconflow.cn/v1"
```

## 注意事项

1. **API Key安全**
   - 不要在代码中硬编码API Key
   - 使用配置文件管理API Key
   - 定期轮换API Key

2. **分层策略**
   - 优先使用主力层，保证服务质量
   - 主力层耗尽后自动切换到每日回血层
   - 最后使用兜底层保证服务不中断

3. **接口兼容性**
   - 优先选择支持OpenAI兼容接口的平台
   - 只需更换Base_URL和API Key
   - 统一请求/响应格式

4. **错误处理**
   - 429错误：立即冷却，无缝切换
   - 401错误：永久禁用
   - 500错误：短暂重试
