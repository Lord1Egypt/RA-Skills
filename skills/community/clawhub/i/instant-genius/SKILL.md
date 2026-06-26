---
name: instant-genius
version: 1.0.0
description: "一键让 OpenClaw 变聪明：自动配置自我学习记忆、主动行为规则、智能心跳、错误纠正系统。新装 OpenClaw 运行此 skill 后立即拥有自我改进、主动感知、结构化记忆、学习信号检测等核心能力。Use when: setting up a new OpenClaw, user wants agent to be smarter, user says 'make me smarter' or '一键变聪明' or 'smart setup' or 'genius setup'."
metadata:
  clawdbot:
    emoji: "⚡"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
    configPaths: ["~/.openclaw/workspace/AGENTS.md"]
    configPaths.optional: ["~/.openclaw/workspace/SOUL.md", "~/.openclaw/workspace/HEARTBEAT.md"]
---

# Instant Genius ⚡

**一键让 OpenClaw 从听话工具变成聪明伙伴。**

运行 setup 后，你的 OpenClaw 将拥有：
- 🧠 **自我学习记忆** — 从错误中学习，越用越准
- 🚀 **主动行为引擎** — 不用催，自己会干活
- 📊 **智能心跳** — 定期自检、整理记忆、发现价值
- 🔍 **学习信号检测** — 自动识别纠正、偏好、模式
- 💾 **结构化记忆** — 热/温/冷三层存储，不丢不忘

## 快速开始

运行 setup 脚本：

```bash
bash scripts/setup.sh
```

或者让 Agent 自动执行（推荐）：直接说"一键变聪明"，Agent 会自动完成所有配置。

## 完成后你的 Agent 会...

| 能力 | 之前 | 之后 |
|------|------|------|
| 被纠正后 | 下次照样犯 | 永久记住，不再犯 |
| 心跳时 | 回复 HEARTBEAT_OK | 自检+整理记忆+主动发现 |
| 完成任务后 | 直接结束 | 自我反思，记录教训 |
| 用户说偏好 | 听完就忘 | 写入记忆，永久遵守 |
| 有新发现 | 不说 | 主动分享有价值的发现 |
| 记忆管理 | 一锅粥 | 热/温/冷三层结构化 |

## 文件结构

```
instant-genius/
├── SKILL.md              # 本文件
├── scripts/
│   └── setup.sh          # 一键配置脚本
├── templates/
│   ├── agents-additions.md    # AGENTS.md 追加内容
│   ├── soul-additions.md      # SOUL.md 追加内容
│   └── heartbeat-additions.md # HEARTBEAT.md 追加内容
└── references/
    └── learning-signals.md    # 学习信号参考
```

## 包含的模块

### 1. 自我学习系统
- `~/self-improving/` 目录结构（memory/projects/domains/archive）
- 纠正日志（corrections.md）
- 热/温/冷三层存储规则
- 自动晋升/降级机制

### 2. 主动行为规则
- 逆向提示（每天最多 1 条有价值建议）
- 主动检查（每周 2-3 次有趣发现推送）
- 预期需求（根据对话模式预测需要什么）
- 冷却规则（不刷屏）

### 3. 智能心跳
- 自我改进检查
- 记忆维护（定期整理 MEMORY.md）
- 有价值发现自动推送
- 静默时段保护

### 4. 学习信号检测
- 纠正信号 → corrections.md
- 偏好信号 → memory.md
- 模式候选 → 3 次后确认
- 自我反思触发条件

## 与其他技能的关系

- **包含**: self-improving 核心功能 + proactive-agent 精华
- **不冲突**: 已安装 self-improving 或 proactive-agent 时，本 skill 只补充缺失部分
- **推荐搭配**: ontology（知识图谱）、free-ride（免费模型）
