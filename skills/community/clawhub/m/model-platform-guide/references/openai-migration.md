# OpenAI 兼容迁移模板

> 用于把现有 OpenAI 调用改到其他模型平台。核心思路永远先检查三件事：`api_key`、`base_url`、`model`。

## 通用迁移清单

把 OpenAI 代码迁移到其他平台时，优先检查：

1. API Key 环境变量名是否变化
2. `base_url` / `baseURL` 是否需要改
3. 模型名是否属于目标平台
4. endpoint 路径是否仍然兼容 `/chat/completions`
5. 平台是否支持：
   - stream
   - tool calling
   - 多模态输入
   - reasoning/thinking 字段

## Python 通用骨架

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="YOUR_BASE_URL",
)

resp = client.chat.completions.create(
    model="YOUR_MODEL",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ]
)

print(resp.choices[0].message.content)
```

## Node.js 通用骨架

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.YOUR_API_KEY_NAME,
  baseURL: "YOUR_BASE_URL"
});

const resp = await client.chat.completions.create({
  model: "YOUR_MODEL",
  messages: [
    { role: "user", content: "你好" }
  ]
});

console.log(resp.choices[0].message.content);
```

## 平台替换速查

### Moonshot / Kimi
- API Key: `MOONSHOT_API_KEY`
- Base URL: `https://api.moonshot.cn/v1`
- Model example: `kimi-k2.5`

### 阿里云百炼
- API Key: `DASHSCOPE_API_KEY`
- Base URL: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- Model example: `qwen-plus`

### SiliconFlow
- API Key: 以控制台为准
- Base URL: `https://api.siliconflow.cn/v1`
- Model example: `Pro/zai-org/GLM-4.7`

### DeepSeek
- API Key: `DEEPSEEK_API_KEY`
- Base URL: `https://api.deepseek.com` 或 `https://api.deepseek.com/v1`
- Model example: `deepseek-chat`

### OpenRouter
- API Key: 以控制台为准
- Base URL: `https://openrouter.ai/api/v1`
- Model: 以路由模型名为准

## 易踩坑

- 只换 key，不换 base URL
- 模型名写成别家平台的
- 把 OpenAI 的 endpoint 默认当成所有平台都完全兼容
- 忘记检查平台是否支持 thinking / reasoning / tools / multimodal
