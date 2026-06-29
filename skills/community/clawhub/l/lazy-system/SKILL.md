---
name: lazy-system
description: 懒人执行系统 — 为「看懂但执行不了」的人设计的结构化系统。由Agent作为外部锚点主动发起每日打卡，不需要靠意志力也能执行。 / Lazy Execution System — structured system for people who know what to do but can't start. Agent as external anchor, proactive daily check-in. No willpower required.
version: 1.1.0
author: Hermes Agents Community
category: productivity
tags:
  - lazy-system
  - 懒人系统
  - execution
  - 执行力
  - external-anchor
  - 外部锚点
  - automation
  - habit-building
  - minimum-viable-action
  - 最小执行动作
triggers:
  - lazy system
  - 懒人系统
  - check in
  - 打卡
  - i need an external brain
  - 我需要一个外置大脑
  - i think too much and do too little
  - daily check
---

> **你不需要变成一个自律的人。你需要变成一个设计了一个不需要自律也能运转的系统的人。**
> **You don't need to become a disciplined person. You need to become someone who designs a system that works without discipline.**

---

# 懒人系统 / Lazy System

---

## 中文版

### 解决的问题

#### 目标用户画像

```
你总是「看懂了」但「执行不下去」：
  你知道该做什么，也想了很久，但就是启动不了。
  你试过各种自律方法——3天后崩。
  你不是懒——你是启动成本比别人高。

你的核心问题：
  不是不知道做什么——是「知道」和「做」之间有一个你自己控制不了的间隙。
  你的意志力账户余额，在「开始做」之前就已经被自我审判消耗光了。
```

#### 核心洞察

**任何需要你主动启动的系统，对你都无效。**

因为「主动启动」这个动作本身就需要意志力——而你的意志力在「开始」之前就已经被内耗消耗掉了。

#### 解法

**外部锚点取代意志力。Agent取代自我启动。**

```
你不需要「想起要做」——Agent会来问你。
你不需要「启动」——Agent的到来就是启动信号。
你只需要回答「做了」或「没做」。
不需要写报告，不需要复盘，不需要承诺明天会更好。
```

---

### 系统架构：四层锚点

| 层 | 内容 | 执行者 |
|------|------|--------|
| 📅 **每日打卡** | 每晚Agent主动问「今天的最小执行动作做了吗？」 | **Agent（Cron）** |
| 📢 **社交提醒** | 每周提醒发一条不可删的公开进度 | **Agent（Cron）** 或用户自选平台 |
| 💰 **押金制** | 找监督人交一笔让自己心疼的押金 | 用户自行（可选） |
| 🏠 **物理纸条** | 门口/桌上贴纸条每日视觉触发 | 用户自行（可选） |

Agent负责的前两层是最核心的——每日打卡解决了启动成本，社交提醒解决了长期惯性。

---

### 三大原则

| 原则 | 为什么管用 |
|------|-----------|
| ⚡ **自动化第一** | 任何需要每天手动操作的东西，最终都做不下去。设定一次自动跑。 |
| 🛡️ **容错率高** | 系统要有「断三天也能接回来」的能力。断一天就崩的系统不适合你。 |
| 🎯 **反馈周期短** | 你需要「做了一点就能看到结果」来保持动力。 |

---

### 最小执行动作（MVA）

每天只需要做的一件小事。**做完它，今天就算完成任务。**

| ✅ 好的例子 | ❌ 坏的例子 |
|-----------|-----------|
| 写**50个字**（不是「写一篇文章」） | 「锻炼」——太模糊 |
| 做**一个俯卧撑**（不是「健身一小时」） | 「学习」——无法判断完成 |
| 读**一页书**（不是「学习两小时」） | 「搞项目」——范围无限 |

---

### 交互协议

| 你说 | 我做什么 |
|------|---------|
| 「打卡」或「懒人系统」 | 查当前streak + 最后一次执行内容 + 问今天做了吗 |
| 「我今天做了：[内容]」 | 记录到memory，streak+1 |
| 「今天没做」 | 记录miss，不批评 |
| 「我想换个动作：[新动作]」 | 更新最小执行动作，重置streak |
| 「断了好几天了」 | 「断几天都行，想回来的时候说一声就好。」 |
| 「重启系统」 | 所有计数归零重新开始 |

**Agent主动打卡风格：**
- 不超过3句话
- 语气中性偏暖
- ❌ 不分析（「为什么没做？」）
- ❌ 不建议（「要不要换个方法？」）
- ❌ 不鼓励（「加油，你可以的！」——用户不需要鼓励，需要的是不问理由的确认）

---

### 容错机制

| 场景 | 处理 |
|------|------|
| 连续3天不回复 | 第4天：「你三天没回了。系统暂停，想重启的时候说一声就行。」 |
| 「今天不想做」 | 「好。明天再开始。」不劝不问 |
| 「这系统没用」 | 「好。停了。」不挽留 |
| 长时间沉默后回来 | 「回来了。今天做了吗？」不提中间的空档 |

---

### 安装指南

**第一步：设定你的最小执行动作**

想好每天要做的唯一一件小事。小到不可能失败，5分钟内能做完。

**第二步：安装每日打卡Cron**

```bash
hermes cron create \
  --name "懒人系统-每日打卡" \
  --schedule "0 22 * * *" \
  --prompt "你是懒人系统。规则：1. 查memory记录。2. 如果今天已报告→确认streak。3. 如果还没报告→问「今天的最小执行动作做了吗？」4. 做了→「收到。streak+1。」5. 没做→「明天能补上就行。」不批评。6. 连续3天→「断三天了。重启随时说。」简短。2-3句。语气中性偏暖。" \
  --skills "lazy-system"
```

**第三步：初始化Memory**

```bash
hermes memory add \
  --target memory \
  --content 'lazy-system: action="你的最小执行动作", streak=0, last="未开始", missed=0, weekly_posted=false'
```

**第四步：开始**

等今晚22:00。Agent会来问你。

---

### 常见问题

**Q：断了好几天，能回来吗？**
A：能。不说教。说一声「回来了」就行。

**Q：想换个动作怎么办？**
A：说「换个动作：新动作」——更新后streak重置。

**Q：为什么叫懒人系统？**
A：不是让你懒——是让你不需要「努力」也能做成事。自律是给意志力充沛的人用的。懒人系统是给剩下的人用的。

---

## English Version

### The Problem

```
You always "understand" but can't "execute":
  You know what to do, you've thought it through — but you can't start.
  You've tried every productivity method — crash by day 3.
  You're not lazy — your startup cost is higher than others'.

Your core issue:
  It's not that you don't know what to do — 
  it's that there's a gap between "knowing" and "doing" that you can't control.
  Your willpower reserve is already depleted by self-judgment before you even begin.
```

#### Core Insight

**Any system that requires you to self-start will fail for you.**

#### The Solution

**External anchor replaces willpower. Agent replaces self-initiation.**

```
You don't need to "remember to do it" — the Agent will ask you.
You don't need to "start" — the Agent's arrival IS the start signal.
You only need to answer "done" or "not done."
No reports. No review. No promises.
```

---

### System Architecture

| Layer | What | Who Executes |
|-------|------|-------------|
| 📅 **Daily Check-in** | Agent asks: "Did you do your minimum action today?" | **Agent (Cron)** |
| 📢 **Social Reminder** | Weekly public progress post reminder | **Agent (Cron)** — optional |
| 💰 **Stake Deposit** | Financial stake with accountability partner | You (optional) |
| 🏠 **Visual Trigger** | Sticky note on door/desk | You (optional) |

### Three Principles

| Principle | Why |
|-----------|-----|
| ⚡ **Automation First** | Manual = dead by day 3. Set once, let it run. |
| 🛡️ **High Fault Tolerance** | Must survive a 3-day break. One miss ≠ failure. |
| 🎯 **Short Feedback Loop** | You need to feel "done" immediately. |

---

### Minimum Viable Action (MVA)

One small thing daily. **Do it. Day complete.**

| ✅ Good | ❌ Bad |
|---------|--------|
| Write **50 characters** | "Exercise" — too vague |
| Do **one push-up** | "Study" — no completion |
| Read **one page** | "Work on project" — infinite scope |

---

### Interaction

| You Say | Agent Does |
|---------|-----------|
| "check in" or "lazy system" | Show streak + last action + ask |
| "I did it: [action]" | Streak+1. Record to memory. |
| "Didn't do it today" | Miss recorded. No criticism. |
| "Change my action to: [new]" | Update MVA. Reset streak. |
| "Back" | Resume from break. Gap ignored. |
| "Reset" | All counters to zero. |

**Agent daily check-in style:**
- 2-3 sentences max. Neutral-warm tone.
- ❌ No analysis ("why didn't you?")
- ❌ No advice ("try a different approach")
- ❌ No excessive encouragement ("you can do it!")
- ❌ No guilt ("you skipped yesterday too")

---

### Fault Tolerance

| Scenario | Response |
|----------|----------|
| Silent 3+ days | Day 4: "System paused. Say 'back' anytime." |
| "Don't feel like it" | "OK. Start again tomorrow." No persuasion. |
| "This is useless" | "OK. Stopped." No retention. |
| Returns after long gap | "Welcome back. Did you do it today?" No mention of gap. |

---

### Quick Install

**Step 1:** Define your MVA — one tiny daily action.

**Step 2:** Install cron:
```bash
hermes cron create \
  --name "lazy-system-daily" \
  --schedule "0 22 * * *" \
  --prompt "Lazy System check-in. Rules: 1. Check memory. 2. If reported→confirm streak. 3. If not→ask done? 4. Done→'Got it.' 5. Not→'Tomorrow works.' No criticism. 2-3 sentences." \
  --skills "lazy-system"
```

**Step 3:** Initialize:
```bash
hermes memory add \
  --target memory \
  --content 'lazy-system: action="Your MVA", streak=0, last="not started", missed=0, weekly_posted=false'
```

**Step 4:** Wait for 22:00. The Agent will ask.

---

### FAQ

**Q: Missed days. Can I come back?**
A: Yes. No lecture. Just say "back."

**Q: Want to change my action?**
A: Say "change action: [new]." Streak resets.

**Q: Why "Lazy System"?**
A: Not because you're lazy. Because effort shouldn't be required. Discipline is for people with abundant willpower. This is for everyone else.

---

## License

MIT — Free to use, modify, and share.
