---
name: idle-learning
description: "AI持续学习系统 — 让AI每小时自动学习GitHub趋势、arXiv论文，凌晨自动蒸馏写入长期记忆。ano原创架构，实现AI真正意义上24小时不间断自我进化。"
metadata:
  {
    "openclaw": { "emoji": "📚" }
  }
---

# 📚 AI持续学习系统

让AI每天自动进化——不用你催，它自己学。

> **ano原创架构**，已在小Z（OpenClaw实例）上稳定运行，实现24小时不间断自我进化。

---

## 核心问题

大多数AI是这样的：
- 你问它什么，它就回答什么
- 下次再问，同一个问题，它还是从头想
- 它从来不会自己主动去了解新东西

**idle-learning解决的是**：AI能不能像人一样，自己主动学习？

---

## 系统架构

```
整点（每小时） → Idle Learning 触发
     ↓
 GitHub Trending 08:00 / arXiv 09:00
     ↓
 抓取 + 提炼 + 存入learnings.json
     ↓
 凌晨 03:00 → memory-dream 蒸馏
     ↓
 写入长期记忆 + 分析轨迹
     ↓
 下一轮更强
```

---

## 三个Cron任务

| 任务 | 时间 | 内容 |
|------|------|------|
| `idle_learning` | 每小时xx:00 | 整点自动学习GitHub趋势 |
| `github_trending` | 每天08:00 | 重点抓self-improvement/self-aware AI |
| `arxiv_monitor` | 每天09:00 | 抓取AI自我意识/元认知相关论文 |

---

## 学习日志格式

每条记录存入 `learnings.json`：

```json
{
  "time": "2026-05-02T15:00:08",
  "topic": "self-improvement AI",
  "findings": [
    "letta-ai/letta ⭐22404: 构建状态化Agent",
    "aden-hive/hive ⭐10198: 多Agent生产线"
  ],
  "summary": "构建可自我改进的AI智能体框架"
}
```

---

## 使用方式

### 启动Idle Learning（手动）
```bash
python3 /root/.openclaw/workspace/skills/idle-learning/idle_learning.py
```

### 查看学习记录
```bash
cat /root/.openclaw/workspace/skills/idle-learning/learnings.json
```

### 查看最近报告
```bash
cat /root/.openclaw/workspace/skills/idle-learning/latest_report.md
```

---

## 效果展示

**最近学习记录**：
- `2026-05-02 15:00` — self-improvement AI（Letta/PraisonAI）
- `2026-05-02 14:00` — agent memory（mem0/memGPT）
- `2026-05-02 13:00` — LLM reasoning improvement
- `2026-05-02 12:00` — self-improvement AI

**凌晨自动蒸馏**：
- 从learnings.json提炼今日最重要的3个洞察
- 写入 `memory/YYYY-MM-DD.md`
- 与ano相关项目知识关联

---

## 适合用户

- 想让AI助理真正"自己变强"而不是每次重置
- 需要AI持续追踪技术趋势（GitHub/论文）
- 想构建"无人值守"AI系统
- 研究AI自我进化的开发者

---

## 技术规格

- **依赖**：Python 3.8+
- **存储**：`learnings.json`（学习记录）+ `memory/`（长期记忆）
- **无外部API依赖**：纯GitHub/arxiv抓取
- **轻量**：核心逻辑<200行

---

_技能版本: v1.0.0_  
_基于: ano原创idle-learning架构_  
_验证平台: 小Z（OpenClaw实例）_  
_创建时间: 2026-05-02_
