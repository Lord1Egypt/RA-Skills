# 月之暗面 / Moonshot / Kimi API 参考摘要

> 这是整理版摘要，实际字段和模型清单以官方文档为准。
>
> 官方入口：
> - https://platform.kimi.com/docs/guide/start-using-kimi-api
> - https://platform.kimi.com/docs/api/chat

## 速览

- 平台：Moonshot AI / Kimi 开放平台
- 鉴权：`Authorization: Bearer $MOONSHOT_API_KEY`
- OpenAI 兼容：是
- Base URL：`https://api.moonshot.cn/v1`
- 典型接口：`POST /chat/completions`

## 最小 Python 示例

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_MOONSHOT_API_KEY",
    base_url="https://api.moonshot.cn/v1",
)

resp = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ]
)

print(resp.choices[0].message.content)
```

## 最小 curl 示例

```bash
curl https://api.moonshot.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  -d '{
    "model": "kimi-k2.5",
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

## 常见模型名

从当前抓到的文档里可见：

- `kimi-k2.5`
- `kimi-k2-0905-preview`
- `kimi-k2-0711-preview`
- `kimi-k2-turbo-preview`
- `kimi-k2-thinking`
- `kimi-k2-thinking-turbo`
- `moonshot-v1-8k`
- `moonshot-v1-32k`
- `moonshot-v1-128k`
- `moonshot-v1-auto`
- 若干 vision preview 模型

## 接口特点

- 支持 OpenAI 风格 `chat.completions.create`
- 支持流式输出
- 支持工具调用 / function calling
- 支持多模态 content 数组
- 文档里明确给出了 `thinking` 控制字段（至少部分模型支持）

## 多模态输入格式

`content` 可以是：

1. 字符串
2. 数组，元素类型包括：
   - `text`
   - `image_url`
   - `video_url`

图片/视频既可以传 data URL，也可以传文件引用，例如：

- `data:image/png;base64,...`
- `ms://<file_id>`

## 常见注意事项

- 用 OpenAI SDK 时，关键是把 `base_url` 改成 `https://api.moonshot.cn/v1`
- 认证环境变量通常叫 `MOONSHOT_API_KEY`
- 具体模型名更新较快，回答时优先提醒用户以控制台模型列表为准
