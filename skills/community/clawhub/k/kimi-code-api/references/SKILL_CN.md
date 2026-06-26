# Kimi Code API — OpenClaw + Claude Code 集成指南

Kimi Code (K2.5) **完全兼容 Anthropic Messages API**。改一行配置，你的 OpenClaw 就能用 Kimi 跑 Claude Code。

## 快速开始：获取 API Key

1. 打开 [Kimi Code 控制台](https://www.kimi.com/code/console)
2. 创建 API Key → 格式：`sk-kimi-...`

## 配置 1：OpenClaw — 添加 Kimi 为 Provider + Model

在 `openclaw.json` 中添加：

```jsonc
// providers 里加：
{
  "id": "kimi",
  "type": "anthropic",          // Kimi 用的是 Anthropic 协议
  "baseUrl": "https://api.kimi.com/coding",
  "apiKey": "sk-kimi-..."
}

// models 里加（或 agents.defaults.models）：
{
  "kimi/kimi-k2.5": {
    "alias": "Kimi K2.5",
    "params": {}
  }
}
```

然后在 OpenClaw 里随处可用：
- Agent 模型：`"model": "kimi/kimi-k2.5"`
- 聊天切换：`/model kimi/kimi-k2.5`
- 设为某个 Agent 的默认模型

## 配置 2：Claude Code CLI — 直接使用

```bash
export ANTHROPIC_BASE_URL="https://api.kimi.com/coding"
export ANTHROPIC_API_KEY="sk-kimi-..."

# 交互模式
claude

# 单次执行
claude --print "把这个函数改成 async/await"
```

Claude Code 会自动在 Base URL 后拼 `/v1/messages`，无需其他改动。

## 配置 3：OpenClaw 启动 Claude Code 用 Kimi 后端

在 OpenClaw 中 spawn Claude Code (ACP) 会话，自动使用 Kimi 后端：

```bash
# 通过 sessions_spawn：
sessions_spawn(
    runtime="acp",
    task="你的编码任务",
    env={
        "ANTHROPIC_BASE_URL": "https://api.kimi.com/coding",
        "ANTHROPIC_API_KEY": "sk-kimi-..."
    }
)
```

也可以在 `openclaw.json` 全局配置，每次 ACP spawn 默认都走 Kimi。

## API 参考

| 属性 | 值 |
|------|-----|
| Base URL | `https://api.kimi.com/coding` |
| 消息接口 | `https://api.kimi.com/coding/v1/messages` |
| 认证头 | `x-api-key: sk-kimi-...` |
| 版本头 | `anthropic-version: 2023-06-01` |
| 模型名（请求） | `kimi-k2.5` |
| 模型名（响应） | `kimi-for-coding` |
| 协议 | Anthropic Messages API |
| 流式输出 | `"stream": true` → SSE |

## 原始调用示例

### curl

```bash
curl -s https://api.kimi.com/coding/v1/messages \
  -H "x-api-key: sk-kimi-..." \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"kimi-k2.5","max_tokens":1024,"messages":[{"role":"user","content":"你好"}]}'
```

### Python（纯标准库）

```python
import json, urllib.request

req = urllib.request.Request(
    "https://api.kimi.com/coding/v1/messages",
    data=json.dumps({
        "model": "kimi-k2.5",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": "你好"}]
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

## 注意事项

- **模型名不一致**：请求发 `kimi-k2.5`，响应返回 `kimi-for-coding`。不要断言响应中的模型名。
- **仅 Anthropic 格式**：`/v1/messages` 可用；`/v1/chat/completions`（OpenAI 格式）返回 404。
- **`api.moonshot.cn` ≠ Kimi Code**：那是 Moonshot 通用 API，不同产品、不同认证。
- **超时**：复杂提示词设 ≥120 秒。
- **Provider 类型**：OpenClaw 配置里必须写 `"type": "anthropic"` — Kimi 走 Anthropic 协议。
