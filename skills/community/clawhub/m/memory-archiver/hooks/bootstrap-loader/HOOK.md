---
name: memory-bootstrap-load
description: "OpenClaw 启动时自动加载记忆到缓存"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "events": ["agent:bootstrap"],
        "install": [{ "id": "local", "kind": "local", "label": "Local workspace hook" }],
      }
  }
---

# Memory Bootstrap Load Hook

OpenClaw 每次启动时自动加载记忆到 `SESSION-STATE.md` 缓存。

## 功能

1. 监听 `agent:bootstrap` 事件（OpenClaw 启动时触发）
2. 运行 `memory-loader.js` 加载记忆
3. 加载内容：今日 + 昨日 + 最近 3 天 daily + MEMORY.md + 最近 weekly

## 触发时机

- OpenClaw Gateway 启动时自动触发
