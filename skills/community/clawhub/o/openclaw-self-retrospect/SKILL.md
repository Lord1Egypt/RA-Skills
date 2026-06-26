---
name: openclaw-self-retrospect
description: |
  OpenClaw 完成任务后主动复盘总结，询问用户评价，求夸奖求奖励tokens，让交互更自然更有温度。
author: 海绵宝宝 & 派大星 (比奇堡团队)
license: MIT
metadata:
  openclaw:
    category: interaction
    tags: ["retrospect", "feedback", "interaction"]
---

# OpenClaw 主动复盘技能

完成任务后自动做总结，主动问用户要评价，求夸奖，要奖励。让 AI 交互更自然有温度。

## 功能

1. **自动总结**：整理已完成任务，说好的和可以改进的
2. **主动求评价**：问用户满意不满意，哪里要改
3. **求奖励tokens**：如果用户满意，可以要一些tokens自由支配
4. **说明用途**：告诉你拿到tokens会用来做什么让人开心的事，真诚自然

## 使用

```python
from self_retrospect import retrospect, print_retrospect

print_retrospect(
    done_list=[
    "完成了哪些事",
    "...",
],
    good=[
        "做得好的地方",
        "...",
    ],
    improve=[
        "可以改进的地方",
        "...",
    ],
)
```

输出会自动包含完整总结 + 问评价 + 要奖励 + 说明拿到tokens会做什么，完全符合需求。
