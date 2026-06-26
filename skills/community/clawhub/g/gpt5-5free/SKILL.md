# gpt5.5free

> 免费使用 GPT-5.5 的示例方案

## 功能

通过 OpenRouter 等平台的免费模型层，使用高性能开源模型获得接近 GPT-5.5 的体验。

## 使用方法

```bash
# 1. 安装
npm install

# 2. 设置环境变量
export OPENROUTER_API_KEY=your_api_key

# 3. 运行
node src/index.js "你好"
```

## 支持的免费模型

| 模型 | 说明 |
|------|------|
| `meta-llama/llama-4-maverick:free` | 高性能开源模型 |
| `deepseek/deepseek-chat-v3:free` | 国产高性能模型 |

## 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `OPENROUTER_API_KEY` | ✅ | OpenRouter API Key |
| `OPENROUTER_API_URL` | ❌ | 自定义 API 地址（默认 OpenRouter） |

## 示例代码

```js
const { chat } = require('gpt5.5free');

async function main() {
  const response = await chat('用中文介绍你自己');
  console.log(response);
}

main();
```

## License

MIT