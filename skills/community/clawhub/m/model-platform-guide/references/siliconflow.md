# 硅基流动 / SiliconFlow API 参考摘要

> 这是整理版摘要，实际字段和支持模型以官方文档为准。
>
> 官方入口：
> - https://docs.siliconflow.cn/cn/api-reference/chat-completions/chat-completions

## 速览

- 平台：SiliconFlow / 硅基流动
- 鉴权：Bearer Token
- OpenAI 兼容：是
- Base URL：`https://api.siliconflow.cn/v1`
- 典型接口：`POST /chat/completions`

## 最小 Python 示例

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.siliconflow.cn/v1"
)

response = client.chat.completions.create(
    model="Pro/zai-org/GLM-4.7",
    messages=[
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "你好"}
    ]
)

print(response.choices[0].message.content)
```

## 接口特点

从当前文档摘要可以看到：

- OpenAPI 描述完整
- 支持标准 chat completions
- 支持流式输出（`text/event-stream`）
- 支持视觉输入 / image input
- 支持函数调用 / tool calls
- 响应头里包含 `x-siliconcloud-trace-id`，便于排障

## 返回内容要点

响应里常见：

- `choices[].message.content`
- `choices[].message.reasoning_content`
- `usage.prompt_tokens`
- `usage.completion_tokens`
- `usage.total_tokens`
- `prompt_cache_hit_tokens`
- `prompt_cache_miss_tokens`

这说明它在文档层面暴露了较丰富的 token / cache 统计信息。

## 常见模型名

当前抓到的页面示例里出现：

- `Pro/zai-org/GLM-4.7`
- `zai-org/GLM-4.6V`

说明 SiliconFlow 的模型命名风格通常带供应商/版本路径，回答用户时要提醒不要直接套用 OpenAI 或 Kimi 的模型名。

## 常见注意事项

- 使用 OpenAI SDK 时，把 `base_url` 指向 `https://api.siliconflow.cn/v1`
- 模型名格式和其他平台差异较大
- 如果用户排查请求问题，可以优先让他记录 `x-siliconcloud-trace-id`
