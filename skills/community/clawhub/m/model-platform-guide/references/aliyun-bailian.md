# 阿里云百炼 / DashScope / Model Studio API 参考摘要

> 这是整理版摘要，实际字段和能力以官方文档为准。
>
> 官方入口：
> - https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen
> - https://help.aliyun.com/zh/model-studio/qwen-api-reference/

## 速览

- 平台：阿里云百炼（Model Studio / DashScope）
- 鉴权：常用 `DASHSCOPE_API_KEY`
- OpenAI 兼容：是
- 兼容 Base URL：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 国际站文档里常见另一个域名：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- 典型接口：`POST /chat/completions`

## 最小 Python 示例（OpenAI SDK 兼容方式）

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"}
    ]
)

print(completion.choices[0].message.content)
```

## 最小 Node.js 示例

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

const completion = await client.chat.completions.create({
  model: "qwen-plus",
  messages: [
    { role: "user", content: "你好" }
  ]
});

console.log(completion.choices[0].message.content);
```

## SDK 路线

百炼常见两条路：

1. **OpenAI SDK 兼容模式**
   - 适合已有 OpenAI 代码迁移
   - 改 `api_key` 和 `base_url` 即可
2. **DashScope 官方 SDK**
   - Python / Java 等语言有原生 SDK
   - 更适合百炼特有能力或阿里云生态集成

## 文档中可见的关键信息

- 环境变量名：`DASHSCOPE_API_KEY`
- 常见模型：`qwen-plus`
- 支持 Python、Node.js、Java 等调用方式
- 可直接复用 OpenAI SDK
- 北京区和新加坡区 base URL 可能不同

## 常见注意事项

- 用户最容易踩的坑是：
  - 只换了 API Key，没换 `base_url`
  - 区域搞错（北京 / 新加坡）
  - 用的是 OpenAI SDK，但模型名没换成百炼支持的模型
- 写文档时建议同时写明“兼容模式”和“官方 SDK 模式”
