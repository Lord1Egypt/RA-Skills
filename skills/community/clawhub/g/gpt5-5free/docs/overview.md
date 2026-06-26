# GPT-5.5 免费方案概述

## 原理

通过 OpenRouter 等平台的免费模型层，使用高性能开源模型（如 Llama 4、Qwen3、DeepSeek-V3 等）获得接近 GPT-5.5 的体验。

## 支持的免费模型

| 模型 | 提供商 | 说明 |
|------|--------|------|
| meta-llama/llama-4-maverick:free | OpenRouter | 高性能开源模型 |
| deepseek/deepseek-chat-v3:free | OpenRouter | 国产高性能模型 |

## 使用限制

- 免费层有速率限制（通常 RPM < 20）
- 不建议用于生产环境高并发场景
- 模型能力虽接近，但不等同于 GPT-5.5 官方版本

## 快速开始

1. 注册 [OpenRouter](https://openrouter.ai) 获取免费 API Key
2. 设置环境变量 `OPENROUTER_API_KEY`
3. 运行 `node src/index.js "你的问题"`

## 进阶配置

可通过环境变量 `OPENROUTER_API_URL` 切换到其他兼容 OpenAI API 格式的服务商。
