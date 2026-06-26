# 模型信息参考

## 提供商 API 格式

| 提供商 | API 类型 | Base URL | 测试端点 |
|--------|----------|----------|----------|
| bailian | openai-completions | `https://coding.dashscope.aliyuncs.com/v1` | `/chat/completions` |
| bailian2 | openai-completions | `https://coding.dashscope.aliyuncs.com/v1` | `/chat/completions` |
| volcano | openai-completions | `https://ark.cn-beijing.volces.com/api/coding/v3` | `/chat/completions` |
| siliconflow | openai-completions | `https://api.siliconflow.cn/v1` | `/chat/completions` |
| minmax | anthropic-messages | `https://api.minimaxi.com/anthropic` | `/v1/messages` |
| 注册机 | openai-completions | `https://wbz-api.939593.xyz/v1` | `/chat/completions` |

## 测试请求格式

### openai-completions

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer <apiKey>"
}
$body = @{
    model = "<model-id>"
    messages = @(@{role="user"; content="hi"})
    max_tokens = 5
} | ConvertTo-Json -Depth 3 -Compress
Invoke-RestMethod -Uri "<baseUrl>/chat/completions" -Method Post -Headers $headers -Body $body
```

### anthropic-messages

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "<apiKey>"
    "anthropic-version" = "2023-06-01"
}
$body = @{
    model = "<model-id>"
    max_tokens = 5
    messages = @(@{role="user"; content="hi"})
} | ConvertTo-Json -Depth 3 -Compress
Invoke-RestMethod -Uri "<baseUrl>/v1/messages" -Method Post -Headers $headers -Body $body
```

## 响应状态码解读

| 状态码 | 含义 | 分类 |
|--------|------|------|
| 200 | OK | ✅ 可用 |
| 401/403 | Unauthorized/Forbidden | ❌ 认证失败 |
| 429 | Too Many Requests | ⚠️ RateLimit |
| 400 | Bad Request | ❌ 请求格式错误 |
| 404 | Not Found | ❌ 模型不存在 |
| 500/502/503 | Server Error | ❌ 服务端错误 |

## 上下文窗口参考

| 模型 | 上下文 | 推理 |
|------|--------|------|
| gpt-5-codex | 400K | ❌ |
| gpt-5.4 | 400K | ❌ |
| MiniMax-M2.7 | 204K | ✅ |
| MiniMax-M2.5 | 204K | ✅ |
| GLM-4.7 | 200K | ❌ |
| DeepSeek-V3.2 | 200K | ❌ |
| DeepSeek-V3.2-Pro | 200K | ✅ |
| GLM-4.6 | 200K | ❌ |
| qwen3-max | 128K | ✅ |
| qwen2.5 | 32K | ❌ |
| glm-5 | 32K | ❌ |

## 能力排序规则

1. contextWindow 大者优先
2. reasoning=true 优先（同 contextWindow 时）

排序示例：
- 400K ❌ > 200K ✅ > 200K ❌ > 32K ✅ > 32K ❌
