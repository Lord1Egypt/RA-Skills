# gpt5.5free

> 免费使用 GPT-5.5 的示例方案

## 简介

本项目演示如何通过公开渠道免费使用 GPT-5.5 级别的模型能力，利用 OpenRouter 等平台的免费模型层。

## 快速开始

```bash
npm install
node src/index.js "你好"
```

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `OPENROUTER_API_KEY` | OpenRouter API Key（免费注册获取） |

## 支持的免费模型

| 模型 | 说明 |
|------|------|
| `meta-llama/llama-4-maverick:free` | 高性能开源模型 |
| `deepseek/deepseek-chat-v3:free` | 国产高性能模型 |

## 免责声明

本方案仅用于学习与演示，请遵守相关服务条款。免费层有速率限制，不建议用于生产高并发场景。

## License

MIT
