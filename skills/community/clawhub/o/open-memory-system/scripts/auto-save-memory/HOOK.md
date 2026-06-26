---
name: auto-save-memory
description: "会话结束时自动保存学习要点"
metadata:
  {
    "openclaw": {
      "emoji": "💾",
      "events": ["session:end"],
      "requires": {}
    }
  }
---

# Auto Save Memory Hook

会话结束时自动保存 .learnings/ 目录中的学习要点到记忆系统。
