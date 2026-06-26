---
name: openrouter-free
description: 查询 OpenRouter 上所有免费模型并调用进行智能对话。支持 Gemma、Llama、MiniMax 等 27 个免费大模型，无需付费即可使用。
metadata:
  version: 1.0.0
  homepage: https://clawhub.ai/skills/openrouter-free
  topics:
    - openrouter
    - free-models
    - llm
    - chat
  license: MIT
---

# OpenRouter 免费模型查询与调用

通过 OpenRouter API 查询并调用所有免费模型，无需付费即可使用大模型对话能力。

## 功能

1. **查询免费模型** — 列出 OpenRouter 上所有 27+ 个免费模型及其信息
2. **免费对话** — 调用免费模型进行智能对话

## 使用前提

需要配置 OpenRouter API Key：

```bash
# 在 .env 文件中添加
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

API Key 获取地址：https://openrouter.ai/settings/keys

## 使用方式

```bash
# 查询免费模型列表
python3 openrouter_free.py list

# 调用免费模型对话
python3 openrouter_free.py chat "你的问题"
```

## 推荐免费模型

| 模型 ID | 名称 | 上下文长度 | 适用场景 |
|---------|------|-----------|---------|
| `openrouter/free` | 自动路由 | 200K | 通用首选 |
| `meta-llama/llama-3.3-70b-instruct:free` | Llama 3.3 70B | 131K | 长文本对话 |
| `minimax/minimax-m2.5:free` | MiniMax M2.5 | 196K | 高质量对话 |
| `google/gemma-4-26b-it:free` | Gemma 4 26B | 262K | 快速推理 |

## 全部免费模型

当前共 **27** 个免费模型，涵盖：
- Google Gemma 系列
- Meta Llama 系列
- NVIDIA Nemotron 系列
- Qwen 系列
- MiniMax 等国产模型

## 注意事项

- 图片生成模型在中国大陆地区可能不可用（403），本技能仅提供对话和列表能力
- 免费模型响应速度因运营商而异
- 建议使用 `openrouter/free` 自动路由，系统自动选择最佳免费模型
