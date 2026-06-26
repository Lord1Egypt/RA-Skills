---
name: auto-load-memory
description: "会话启动时自动加载核心记忆"
metadata:
  {
    "openclaw": {
      "emoji": "💾",
      "events": ["agent:bootstrap"],
      "requires": { "bins": ["python3"] }
    }
  }
---

# Auto Load Memory Hook

会话开始时自动加载三层记忆。

## 功能
1. 监听 `agent:bootstrap` 事件
2. 运行 `memory/memory.py read` 获取记忆内容
3. 将记忆内容注入 Agent 上下文

## 加载的记忆内容
- MEMORY.md 长期记忆
- 今日 short-term 日志
- preferences 摘要
