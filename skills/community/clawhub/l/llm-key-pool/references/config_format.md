# 配置文件格式说明（分层轮询版）

## 目录
- [格式概述](#格式概述)
- [分层策略](#分层策略)
- [完整示例](#完整示例)
- [字段说明](#字段说明)
- [验证规则](#验证规则)
- [常见错误](#常见错误)

## 格式概述

配置文件使用YAML格式，文件名默认为 `llm_config.yaml`，支持多平台分层配置。

**分层策略：**
- **primary（主力层）**：高额度平台，处理大部分日常任务
- **daily（每日回血层）**：每日刷新额度，保证基本可用性
- **fallback（兜底层）**：开源/聚合平台，保证服务不中断

**基本结构：**
```yaml
providers:
  <platform_name>:
    tier: "primary|daily|fallback"  # 层级（必需）
    model: "model_name"             # 模型名称（必需）
    api_keys:                       # API Key列表（必需）
      - "key_1"
      - "key_2"
    base_url: "https://api.example.com/v1"  # API基础URL（必需）

global:
  max_retries: 3                   # 最大重试次数
  retry_delay: 1                   # 重试延迟（秒）
  error_threshold: 5               # 错误阈值
  cooldown_seconds: 300            # 冷却时间（秒）
  quota_check_enabled: true        # 是否启用配额检查
```

## 分层策略

### 主力层（primary）
**特点：** 初始赠送额度极大，适合处理大部分日常任务

**推荐平台：**
- 阿里云百炼（DashScope）
- 智谱AI（BigModel）

**配置示例：**
```yaml
alibaba_bailian:
  tier: primary
  model: "qwen-max"
  api_keys:
    - "sk-xxxxxxxxxxxxxxxx"
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"

zhipu:
  tier: primary
  model: "glm-4"
  api_keys:
    - "xxxxxxxxxxxxxxxx"
  base_url: "https://open.bigmodel.cn/api/paas/v4"
```

### 每日回血层（daily）
**特点：** 额度每日刷新，即使主力层耗尽也能保证基本可用性

**推荐平台：**
- 火山引擎（字节跳动）
- Google AI Studio

**配置示例：**
```yaml
volcengine:
  tier: daily
  model: "doubao-pro-256k"
  api_keys:
    - "xxxxxxxxxxxxxxxx"
  base_url: "https://ark.cn-beijing.volces.com/api/v3"

google_aistudio:
  tier: daily
  model: "gemini-1.5-pro"
  api_keys:
    - "AIzaSyxxxxxxxxxxxxxxxx"
  base_url: "https://generativelanguage.googleapis.com/v1beta"
```

### 兜底层（fallback）
**特点：** 开源模型/聚合平台，当大厂API都限流时保证服务不中断

**推荐平台：**
- 硅基流动（SiliconFlow）
- OpenRouter
- GitHub Models
- Groq
- 腾讯混元

**配置示例：**
```yaml
siliconflow:
  tier: fallback
  model: "Qwen/Qwen2.5-7B-Instruct"
  api_keys:
    - "sk-xxxxxxxxxxxxxxxx"
  base_url: "https://api.siliconflow.cn/v1"

openrouter:
  tier: fallback
  model: "meta-llama/llama-3.1-8b-instruct:free"
  api_keys:
    - "sk-or-xxxxxxxxxxxxxxxx"
  base_url: "https://openrouter.ai/api/v1"
```

## 完整示例

```yaml
# 多平台分层配置示例
providers:
  # 主力层：阿里云百炼
  alibaba_bailian:
    tier: primary
    model: "qwen-max"
    api_keys:
      - "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
      - "sk-yyyyyyyyyyyyyyyyyyyyyyyy"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"

  # 主力层：智谱AI
  zhipu:
    tier: primary
    model: "glm-4"
    api_keys:
      - "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      - "yyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    base_url: "https://open.bigmodel.cn/api/paas/v4"

  # 每日回血层：火山引擎
  volcengine:
    tier: daily
    model: "doubao-pro-256k"
    api_keys:
      - "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    base_url: "https://ark.cn-beijing.volces.com/api/v3"

  # 每日回血层：Google AI Studio
  google_aistudio:
    tier: daily
    model: "gemini-1.5-pro"
    api_keys:
      - "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxx"
    base_url: "https://generativelanguage.googleapis.com/v1beta"

  # 兜底层：硅基流动
  siliconflow:
    tier: fallback
    model: "Qwen/Qwen2.5-7B-Instruct"
    api_keys:
      - "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
    base_url: "https://api.siliconflow.cn/v1"

  # 兜底层：OpenRouter
  openrouter:
    tier: fallback
    model: "meta-llama/llama-3.1-8b-instruct:free"
    api_keys:
      - "sk-or-xxxxxxxxxxxxxxxxxxxxxxxx"
    base_url: "https://openrouter.ai/api/v1"

# 全局配置
global:
  max_retries: 3              # 最大重试次数
  retry_delay: 1              # 重试延迟（秒）
  error_threshold: 5          # 错误阈值
  cooldown_seconds: 300       # 冷却时间（秒）
  quota_check_enabled: true   # 是否启用配额检查
```

## 字段说明

### providers（必需）
各平台的配置集合，每个平台是一个独立的配置对象。

#### 平台配置字段

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `tier` | 是 | string | 层级（primary/daily/fallback） |
| `model` | 是 | string | 模型名称 |
| `api_keys` | 是 | array | API Key数组，至少包含一个有效的Key |
| `base_url` | 是 | string | API基础URL |

### global（可选）
全局配置项，影响所有平台的行为。

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `max_retries` | 3 | 最大重试次数 |
| `retry_delay` | 1 | 重试延迟（秒） |
| `error_threshold` | 5 | 错误阈值，超过则暂时禁用Key |
| `cooldown_seconds` | 300 | 冷却时间（秒） |
| `quota_check_enabled` | true | 是否启用配额检查 |

## 验证规则

配置文件必须满足以下规则：

1. **格式正确性**
   - 必须是有效的YAML格式
   - `providers` 字段必须存在且非空

2. **平台配置**
   - 每个平台必须包含 `tier`、`model`、`api_keys`、`base_url` 字段
   - `tier` 必须是以下值之一：`primary`、`daily`、`fallback`
   - `api_keys` 数组必须包含至少一个非空字符串

3. **值类型**
   - `tier`、`model` 和 `base_url` 必须是字符串
   - `api_keys` 必须是数组
   - 全局配置中的数值字段必须是非负整数
   - `quota_check_enabled` 必须是布尔值

4. **URL格式**
   - `base_url` 必须是有效的HTTP/HTTPS URL

## 常见错误

### 错误1：缺少tier字段
```yaml
# 错误：缺少tier字段
providers:
  alibaba_bailian:
    model: "qwen-max"
    api_keys:
      - "sk-xxxxxxxx"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

**修正：**
```yaml
providers:
  alibaba_bailian:
    tier: primary  # 添加tier字段
    model: "qwen-max"
    api_keys:
      - "sk-xxxxxxxx"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

### 错误2：tier值无效
```yaml
# 错误：tier值无效
providers:
  alibaba_bailian:
    tier: "high"  # 应该是 primary/daily/fallback
    model: "qwen-max"
    api_keys:
      - "sk-xxxxxxxx"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

**修正：**
```yaml
providers:
  alibaba_bailian:
    tier: primary  # 使用正确的层级值
    model: "qwen-max"
    api_keys:
      - "sk-xxxxxxxx"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

## 配置模板

```yaml
providers:
  # 主力层
  alibaba_bailian:
    tier: primary
    model: "qwen-max"
    api_keys:
      - "your-api-key-1"
      - "your-api-key-2"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"

  # 每日回血层
  volcengine:
    tier: daily
    model: "doubao-pro-256k"
    api_keys:
      - "your-api-key"
    base_url: "https://ark.cn-beijing.volces.com/api/v3"

  # 兜底层
  siliconflow:
    tier: fallback
    model: "Qwen/Qwen2.5-7B-Instruct"
    api_keys:
      - "your-api-key"
    base_url: "https://api.siliconflow.cn/v1"

global:
  max_retries: 3
  retry_delay: 1
  error_threshold: 5
  cooldown_seconds: 300
  quota_check_enabled: true
```

## OpenAI兼容接口说明

本Skill优先使用OpenAI兼容接口，所有配置的平台都应提供OpenAI兼容的API端点：

**标准请求格式：**
```
POST {base_url}/chat/completions
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "model": "model_name",
  "messages": [...],
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**标准响应格式：**
```json
{
  "choices": [
    {
      "message": {
        "content": "响应内容"
      }
    }
  ]
}
```

各平台的OpenAI兼容接口地址请参考 [supported_providers.md](supported_providers.md)
