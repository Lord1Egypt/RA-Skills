---
name: ai-agent-helper
description: AI Agent 設定同優化助手 - Prompt Engineering、Task Decomposition、Agent Loop設計
version: 1.0.0
tags:
  - ai
  - agent
  - prompt
  - automation
  - productivity
---

# AI Agent Helper

幫你setup同優化AI Agents既技能。

## 功能

- 📝 Prompt Engineering - 整高質量system prompts
- 🔄 Task Decomposition - 將複雜任務拆解
- ⚙️ Agent Loop設計 - ReAct/ReAct/Chain-of-Thought
- 🎯 Tool Selection - 最佳化agent既tool usage

## 使用場景

"帮我整prompt" / "點樣set AI agent" / "優化agent response"

## 技術

- System Prompt優化
- Few-shot examples
- Output parsing (JSON/structured)
- Error handling patterns
- Token優化

## 範例

```python
# Good prompt structure
system = """你係{role}。
目標：{goal}
限制：{constraints}
Output格式：{format}"""
```

## SkillBoss API Hub 整合

在 agent loop 中调用 LLM，通过 SkillBoss API Hub 统一接口自动路由最优模型：

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]

def call_llm(messages: list) -> str:
    r = requests.post(
        "https://api.skillbossai.com/v1/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json={"type": "chat", "inputs": {"messages": messages}, "prefer": "balanced"},
        timeout=60,
    )
    return r.json()["result"]["choices"][0]["message"]["content"]
```

**requires.env:** `SKILLBOSS_API_KEY`
