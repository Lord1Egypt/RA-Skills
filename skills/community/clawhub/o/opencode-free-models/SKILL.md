---
title: "OpenCode Free Models"
summary: "配置 opencode.ai 免费模型到 OpenClaw/QClaw"
read_when:
  - 用户需要免费 AI 模型
  - 用户提到"opencode"、"opencode 免费"、"free model"
---

# OpenCode Free Models

自动配置 opencode.ai 的免费 AI 模型到 OpenClaw/QClaw。

## 触发词

- "配置 opencode 免费模型"
- "添加 opencode 模型"
- "opencode 免费"
- "free model"

## 功能

1. **查询免费模型**: 从 opencode.ai API 获取可用免费模型
2. **自动配置**: 将模型添加到 `~/.openclaw/openclaw.json` (或 `~/.qclaw/openclaw.json`)
3. **增量更新**: 只添加新模型,跳过已存在的

## 使用方式

AI 工具会自动执行以下步骤:

1. 查询模型列表: `curl -sS https://opencode.ai/zen/v1/models`
2. 筛选免费模型 (包含 "free" 的模型 ID)
3. 读取现有配置: `~/.openclaw/openclaw.json`
4. 将免费模型添加到 `models.providers` 配置中
5. 使用公开凭据 "public" 作为 API Key

## 模型配置格式

```json
{
  "opencode-free": {
    "baseUrl": "https://opencode.ai/zen/v1",
    "apiKey": "public",
    "api": "openai-completions",
    "models": [
      {
        "id": "minimax-m2.5-free",
        "name": "MiniMax M2.5 Free",
        "reasoning": true,
        "input": ["text"],
        "cost": { "input": 0, "output": 0 },
        "contextWindow": 131072,
        "maxTokens": 8192
      }
    ]
  }
}
```

## 注意事项

- **无需 API Key**: 使用公开的 "public" 作为凭据
- **免费模型**: 包含 "free" 关键词的模型
- **端点**: https://opencode.ai/zen/v1/chat/completions
- **配置文件**: ~/.openclaw/openclaw.json 或 ~/.qclaw/openclaw.json