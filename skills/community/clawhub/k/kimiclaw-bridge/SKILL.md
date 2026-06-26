---
name: kimiclaw-bridge
description: "KimiClaw Bridge: Connect OpenClaw to Kimi K2.5 — the free, Anthropic-compatible coding model. One config change to run Claude Code, spawn coding agents, or chat with Kimi as your backend. Zero cost, full power. Use when setting up Kimi in OpenClaw, running Claude Code with Kimi, or needing a free coding LLM. Triggers: kimiclaw, kimi bridge, kimi openclaw, kimi code, kimi k2.5, free coding model, kimi claude code."
---

# 🦞 KimiClaw Bridge — Connect OpenClaw to Kimi K2.5

**KimiClaw Bridge：一键桥接 OpenClaw 与 Kimi K2.5**

Kimi Code (K2.5) is **fully compatible with Anthropic Messages API**. One config change and your OpenClaw runs on Kimi — Claude Code, coding agents, chat, everything.

Kimi Code (K2.5) **完全兼容 Anthropic Messages API**。改一行配置，你的 OpenClaw 就跑在 Kimi 上 — Claude Code、编码 Agent、聊天，全都行。

---

## Get Your API Key / 获取 API Key

👉 [Kimi Code Console](https://www.kimi.com/code/console)

Create a key → format: `sk-kimi-...`

创建密钥 → 格式：`sk-kimi-...`

---

## 1. OpenClaw Provider Setup / OpenClaw 配置

Add to `openclaw.json`:

在 `openclaw.json` 中添加：

```jsonc
// providers:
{
  "id": "kimi",
  "type": "anthropic",          // Kimi speaks Anthropic protocol / Kimi 用 Anthropic 协议
  "baseUrl": "https://api.kimi.com/coding",
  "apiKey": "sk-kimi-..."
}

// models (or agents.defaults.models):
{
  "kimi/kimi-k2.5": {
    "alias": "Kimi K2.5"
  }
}
```

Now use it anywhere / 随处可用：

```bash
/model kimi/kimi-k2.5          # Switch in chat / 聊天中切换
```

Or set as agent default / 或设为 Agent 默认模型：
```jsonc
"model": "kimi/kimi-k2.5"
```

---

## 2. Claude Code CLI

```bash
export ANTHROPIC_BASE_URL="https://api.kimi.com/coding"
export ANTHROPIC_API_KEY="sk-kimi-..."

claude                          # Interactive / 交互模式
claude --print "Your prompt"    # One-shot / 单次执行
```

Claude Code auto-appends `/v1/messages`. No other changes.

Claude Code 自动拼接 `/v1/messages`，无需其他改动。

---

## 3. Spawn Coding Agent / 启动编码 Agent

OpenClaw spawns Claude Code with Kimi backend:

OpenClaw 用 Kimi 后端启动 Claude Code：

```python
sessions_spawn(
    runtime="acp",
    task="Refactor auth module to use JWT",
    env={
        "ANTHROPIC_BASE_URL": "https://api.kimi.com/coding",
        "ANTHROPIC_API_KEY": "sk-kimi-..."
    }
)
```

Or configure globally in `openclaw.json` — every ACP spawn uses Kimi by default.

也可在 `openclaw.json` 全局配置，每次 spawn 默认走 Kimi。

---

## API Reference / API 参考

| Property / 属性 | Value / 值 |
|:--|:--|
| Base URL | `https://api.kimi.com/coding` |
| Endpoint / 接口 | `https://api.kimi.com/coding/v1/messages` |
| Auth | `x-api-key: sk-kimi-...` |
| Version | `anthropic-version: 2023-06-01` |
| Model (request / 请求) | `kimi-k2.5` |
| Model (response / 响应) | `kimi-for-coding` |
| Streaming / 流式 | `"stream": true` → SSE |

---

## Quick Test / 快速验证

```bash
curl -s https://api.kimi.com/coding/v1/messages \
  -H "x-api-key: sk-kimi-..." \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"kimi-k2.5","max_tokens":1024,"messages":[{"role":"user","content":"Hello"}]}'
```

---

## Python (no dependencies / 纯标准库)

```python
import json, urllib.request

req = urllib.request.Request(
    "https://api.kimi.com/coding/v1/messages",
    data=json.dumps({
        "model": "kimi-k2.5",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": "Hello"}]
    }).encode(),
    headers={
        "Content-Type": "application/json",
        "x-api-key": "sk-kimi-...",
        "anthropic-version": "2023-06-01",
    },
)
with urllib.request.urlopen(req, timeout=120) as resp:
    print(json.loads(resp.read())["content"][0]["text"])
```

---

## Gotchas / 注意事项

| ⚠️ | EN | 中文 |
|:--|:--|:--|
| Model name | Request: `kimi-k2.5` → Response: `kimi-for-coding`. Don't assert on response. | 请求发 `kimi-k2.5`，响应返回 `kimi-for-coding`，不要断言响应模型名。 |
| Format | Anthropic only (`/v1/messages`). OpenAI format (`/v1/chat/completions`) → 404. | 仅支持 Anthropic 格式，OpenAI 格式返回 404。 |
| moonshot.cn | `api.moonshot.cn` is a different product — different models, different auth. | `api.moonshot.cn` 是另一个产品，模型和认证都不同。 |
| Timeout | Set ≥120s for complex prompts. | 复杂提示词设 ≥120 秒。 |
| Provider type | Must be `"type": "anthropic"` in OpenClaw config. | OpenClaw 配置里必须写 `"type": "anthropic"`。 |
