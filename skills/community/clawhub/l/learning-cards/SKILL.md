---
name: learning-cards
description: |
  Spaced-repetition flashcard system backed by Feishu Bitable (multi-dimensional table).
  Create flashcards from any book or knowledge base, quiz the user interactively,
  track progress with 16 fields, and auto-schedule reviews using the 85% Rule.

  基于飞书多维表格的间隔复习学习卡片系统。从任何书籍/知识体系生成学习卡片，
  通过对话式问答练习，16 个字段追踪学习进度，85% 规则动态调整难度。

  Use when / 使用场景:
  (1) User wants to study a book/course with flashcards / 用户想用卡片学习一本书或课程
  (2) User says "继续学习", "来几张卡片", "continue studying", "quiz me"
  (3) User asks to create learning cards from a book or document / 用户要求从书籍或文档生成学习卡片
  (4) User asks about learning progress, weak points, or review schedule / 查看学习进度、薄弱点、复习计划
  (5) User mentions "学习卡片", "间隔复习", "spaced repetition", "flashcards"
---

# Learning Cards

Spaced-repetition flashcard system on Feishu Bitable.

基于飞书多维表格的间隔复习学习卡片系统。

Full design details: [references/system-design.md](references/system-design.md)

完整设计文档：[references/system-design.md](references/system-design.md)

## Prerequisites

This skill requires **Feishu (Lark) Bitable** access. Ensure the following before use:

本技能依赖**飞书多维表格**。使用前请确认以下条件：

1. **OpenClaw Feishu plugin configured** — The `openclaw-lark` plugin must be installed and connected to a Feishu tenant. See [OpenClaw Feishu setup docs](https://docs.openclaw.ai/channels/feishu).

   **OpenClaw 飞书插件已配置** — 需安装 `openclaw-lark` 插件并连接到飞书租户。

2. **User OAuth authorization** — The user must grant Bitable read/write permissions when prompted (standard Feishu OAuth flow, handled automatically by OpenClaw).

   **用户 OAuth 授权** — 用户需在首次使用时授权多维表格读写权限（OpenClaw 自动处理）。

3. **Bitable app scope** — The Feishu app needs scopes: `bitable:app`, `bitable:app:readonly`. These are standard in the OpenClaw Feishu plugin.

   **多维表格权限范围** — 飞书应用需开通 `bitable:app`、`bitable:app:readonly` 权限（OpenClaw 飞书插件标配）。

**No additional API keys or credentials are needed** — authentication is handled by the OpenClaw Feishu plugin's existing OAuth infrastructure.

**无需额外 API 密钥** — 认证由 OpenClaw 飞书插件的 OAuth 基础设施统一处理。

## Setup

Create a Bitable app with one table containing these fields.

创建一个飞书多维表格，包含以下字段。

### Content fields / 内容字段

| Field | Type | Note |
|-------|------|------|
| 概念名 | Text (primary) | Card title / 卡片标题 |
| 阶段 | SingleSelect | Major phase / 大阶段 |
| 站点 | SingleSelect | Chapter/unit / 章节 |
| 类型 | SingleSelect | e.g. 核心概念 / 隐喻 / 转变工具 / 关键问题 |
| 正面（问题） | Text | Question / 问题 |
| 背面（答案） | Text | Answer / 答案 |
| 我的理解 | Text | Learner's own notes / 学习者笔记 |

### Tracking fields / 追踪字段

| Field | Type | Note |
|-------|------|------|
| 掌握程度 | SingleSelect | 未学习 / 初步了解 / 基本掌握 / 深度理解 |
| 学习顺序 | Number | Sequential order for first pass / 首轮学习顺序 |
| 首次学习时间 | DateTime | First study timestamp (ms) / 首次学习时间戳 |
| 上次复习 | DateTime | Last study timestamp (ms) / 上次学习时间戳 |
| 下次复习时间 | DateTime | Next review date (ms) / 下次复习日期 |
| 学习次数 | Number | Total attempts / 总答题次数 |
| 连续答对次数 | Number | Streak — drives interval / 连对次数，决定间隔 |
| 答错次数 | Number | Cumulative errors / 累计答错 |
| 最近得分 | Number | Last score (1-5) / 最近得分 |

## Three Learning Phases

### Phase 1: Sequential coverage / 顺序覆盖

First pass through all cards in order by 学习顺序. Goal: build a mental map of the entire knowledge base.

按学习顺序首轮过一遍，建立全局地图感。

### Phase 2: Spaced review / 间隔复习

After first pass. Schedule by 下次复习时间. Mix in remaining new cards.

首轮完成后按复习时间调度，穿插新卡。

### Phase 3: Mastery & transfer / 融会贯通

Cross-topic quizzes, scenario-based questions, reverse prompts (give answer → guess concept).

跨章节混合抽问、情境题、反向提问（给答案猜概念）。

## Quiz Flow

```
1. Read all cards from Bitable
2. Compute recent accuracy (last 5 scores) → determine new:review ratio
3. Select cards:
   - Review: 下次复习时间 <= today, sorted by overdue days
   - New: 学习次数 = 0, sorted by 学习顺序
4. Mix per ratio, present one at a time
5. After each answer: score → show answer → update Bitable
```

### Card presentation format / 出题格式

```
第 X 题（复习/新卡）
> [概念名] | [阶段] | [站点] | [类型]
[正面问题]
```

User can say "讲讲" to skip answering and see the explanation directly (score = 0).

用户可说"讲讲"跳过作答，直接看答案（计 0 分）。

## 85% Rule — Dynamic Ratio

Target ~85% accuracy for optimal learning speed (Wilson et al., Nature Communications, 2019).

目标保持 85% 正确率以获得最优学习速度。

| Recent accuracy | New:Review | Logic |
|---|---|---|
| > 90% | 3:1 | Too easy, add new / 太轻松，加新卡 |
| 80–90% | 2:1 | Optimal zone / 最优区间 |
| 70–80% | 1:1 | More review / 多复习 |
| < 70% | 1:2 | Consolidate first / 先巩固 |

Accuracy = proportion of scores >= 4 in last 5 attempts.

正确率 = 最近 5 次中得分 >= 4 的比例。

## Spaced Review Algorithm

Interval based on consecutive correct answers (连续答对次数):

| Streak | Interval |
|--------|----------|
| 0 | 1 day |
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 14 days |
| 5 | 30 days |
| 6+ | 90 days |

## Post-Answer Update

After each answer, immediately update the card record:

每题答完立即更新卡片记录：

```
学习次数 += 1
最近得分 = score
上次复习 = today
首次学习时间 = today  (if null)

if score >= 4:       连续答对次数 += 1
elif score <= 2:     连续答对次数 = 0; 答错次数 += 1 (if score > 0)
else (score == 3):   streak unchanged

intervals = [1, 1, 3, 7, 14, 30, 90]
下次复习时间 = today + intervals[min(streak, 6)] days  (if score >= 4)
               today + 1 day                           (otherwise)

掌握程度:
  streak >= 5 → 深度理解
  streak >= 3 → 基本掌握
  studied    → 初步了解
```

## Card Generation Guidelines

When creating cards from a book:

从书籍生成卡片时：

- 2–4 cards per chapter for conceptual books / 概念类书籍每章 2-4 张
- 1–2 per tool/API for technical books / 技术类每个工具 1-2 张
- Target 30–50 cards total / 总量 30-50 张
- Questions should be specific, not vague / 问题要具体
- Answers: 150–300 chars, use ①②③ for key points / 答案 150-300 字，序号标注

## User Commands

| Command | Action |
|---------|--------|
| 继续学习 / continue | Default 3 cards, dynamic ratio / 默认 3 张，动态配比 |
| 来 N 张 / give me N | Specific count / 指定数量 |
| 讲讲 / explain | Show answer directly / 直接看答案 |
| 学习进度 / progress | Show overall stats / 显示整体进度 |
| 薄弱点 / weak points | List cards with most errors / 列出高错卡片 |
