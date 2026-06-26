# Node.js 调用模板

> 这里放不同平台的最小 Node.js 调用骨架。

## Moonshot / Kimi

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.MOONSHOT_API_KEY,
  baseURL: "https://api.moonshot.cn/v1"
});

const resp = await client.chat.completions.create({
  model: "kimi-k2.5",
  messages: [{ role: "user", content: "你好" }]
});

console.log(resp.choices[0].message.content);
```

## 阿里云百炼

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

const resp = await client.chat.completions.create({
  model: "qwen-plus",
  messages: [{ role: "user", content: "你好" }]
});

console.log(resp.choices[0].message.content);
```

## DeepSeek

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: "https://api.deepseek.com/v1"
});

const resp = await client.chat.completions.create({
  model: "deepseek-chat",
  messages: [{ role: "user", content: "你好" }]
});

console.log(resp.choices[0].message.content);
```

## OpenRouter

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENROUTER_API_KEY,
  baseURL: "https://openrouter.ai/api/v1"
});

const resp = await client.chat.completions.create({
  model: "YOUR_ROUTE_MODEL",
  messages: [{ role: "user", content: "你好" }]
});

console.log(resp.choices[0].message.content);
```
