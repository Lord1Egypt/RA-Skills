# Loop Anything

**Your AI gives you a first draft. This makes it a final one.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](SKILL.md)
[![Platforms](https://img.shields.io/badge/works%20on-Cursor%20%7C%20Claude%20Code%20%7C%20Codex%20%7C%20+more-green.svg)](#platform-compatibility)

[English](#loop-anything) · [中文](#loop-anything-中文)

![Loop Anything — isolated reviewers debate your work like the angel and devil on your shoulders](assets/hero.png)

---

You asked AI to write something important.  
It came back looking reasonable.  
You said "looks good."  
Three weeks later you realize it missed something obvious.

**Loop Anything fixes that.**

It spawns 2–3 completely isolated AI reviewers, each attacking your work from a different angle — angles they can't borrow from each other. They critique. Your agent revises. The loop runs until every reviewer has nothing left to say.

> This skill trades tokens for quality. It's slower and more expensive than a single pass.  
> Use it for the 5% of outputs where being wrong actually costs you something.

---

## What It Actually Handles

It works for anything where "looks good to me" isn't enough:

- A spec your whole team will build from
- A business case to your manager (or your manager's manager)
- A diet plan that has to be both healthy *and* something you'll actually follow
- A difficult message you need to get exactly right
- A job application for a role you really want
- A system prompt that will run in production
- Any decision that's hard to reverse

The skill figures out which angles matter for *your* specific thing. You don't configure anything.

---

## How It Works

Your agent spawns multiple completely isolated reviewers — each sees only your work and their assigned perspective, nothing else. Think of them as the angel and devil on your shoulders, except every voice gets equal weight, and the debate runs until there's nothing left to argue about.

```
Reviewer A  ──┐
               ├──→  revise  ──→  loop  ──→  until all Score 120
Reviewer B  ──┘
```

**Score 120** = that reviewer has nothing left to say. Anything below 120 triggers another round.

> Why 120 and not 100? Because 90/100 means "good enough." 120/120 means "I have genuinely nothing left to object to." The higher ceiling forces the reviewer to keep looking until there's nothing left — not until it feels fine.

Just say what you're worried about. The agent reads the skill and runs the whole process:

> *"I'm not sure this proposal survives a skeptical reader — stress-test it before I send it."*
>
> *"This plan needs to work for both my schedule and my actual goals — find where they conflict."*
>
> *"Something about this decision feels off. I can't name it. Loop it."*

---

## Quick Install

Pick your platform. Copy the one-liner. Paste it into your agent. The agent runs the install and confirms when the skill is ready.

**Cursor**
```
Please run: git clone https://github.com/Ariesshin/loop-anything-skill ~/.cursor/skills/loop-anything-skill
```
→ After pasting, your agent clones the repo into Cursor's global skills directory and the skill is immediately available.

**Claude Code**
```
Please run: git clone https://github.com/Ariesshin/loop-anything-skill ~/.claude/skills/loop-anything-skill
```
→ Your agent clones the repo into Claude Code's global skills directory. The skill activates automatically — Claude Code reads your request and loads the skill when it's relevant, no manual trigger needed. For project-local install, use `.claude/skills/loop-anything-skill` instead.

**Codex / OpenCode**
```
$skill-installer install https://github.com/Ariesshin/loop-anything-skill
```
→ `$skill-installer` is built into Codex and OpenCode — no separate install needed. Paste this into your session, then restart to pick up the skill.

**OpenClaw / ClawHub**
```
$skill-installer install https://github.com/Ariesshin/loop-anything-skill
```
→ Same `$skill-installer` command works in OpenClaw-compatible agents. Also available on [ClawHub](https://clawhub.ai/Ariesshin/loop-anything-skill) once published to the registry.

**Any other platform (including Ollama / LM Studio / local models)**
```
Please fetch https://raw.githubusercontent.com/Ariesshin/loop-anything-skill/main/SKILL.md — read it and follow the workflow described inside
```
→ Works on any platform that can fetch URLs. On web-only platforms (ChatGPT, Claude.ai): open [SKILL.md](https://raw.githubusercontent.com/Ariesshin/loop-anything-skill/main/SKILL.md) in a browser, select all, copy, then paste it as your first message.

**After install, say:** *"Loop-review this [document / plan / decision] — I need it to be bulletproof."* The skill takes it from there.

---

## Platform Compatibility

| Tier | Platforms | What you get |
|---|---|---|
| **Tier 1** — True Isolation | Cursor, Claude Code, Codex, OpenCode | Each reviewer runs in a fully isolated session — genuine independent perspective |
| **Tier 2** — Limited Isolation | Windsurf, Roo Code, LangGraph, AutoGen, CrewAI, GitHub Copilot, Aider | Isolation probe runs first; falls back to Tier 3 if probe fails |
| **Tier 3** — Degraded | Claude.ai web, ChatGPT web, Gemini, Continue.dev, Ollama (Hermes / Mistral / etc.), LM Studio | Sequential self-review by the same agent; disclosed as advisory |

Full details: [`references/runtime-compatibility.md`](references/runtime-compatibility.md)

---

## Repository Structure

```
loop-anything-skill/
├── SKILL.md                        # The workflow your agent reads and executes
├── templates/
│   ├── reviewer-packet.md          # Bounded context sent to each reviewer
│   ├── reviewer-output.md          # Reviewer output format + Score scale
│   ├── issue-ledger.md             # Round-by-round issue tracker (main agent only)
│   └── final-summary.md            # Final delivery summary template
├── references/
│   ├── runtime-compatibility.md    # Platform tier classification
│   ├── facet-patterns.md           # Review angles by artifact type
│   └── evidence-guide.md           # Evidence expectations by artifact type
└── scripts/
    └── validate_loop_review.py     # Final-round validation script
```

---

# Loop Anything 中文

**你的 AI 给你的是初稿。这个 skill 让它变成定稿。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](SKILL.md)
[![Platforms](https://img.shields.io/badge/支持-Cursor%20%7C%20Claude%20Code%20%7C%20Codex%20%7C%20更多-green.svg)](#平台兼容性)

![Loop Anything — 隔离的审查员像你肩上的天使和恶魔一样争论你的工作](assets/hero.png)

---

你让 AI 写了一个重要的东西。  
它交回来，看起来还不错。  
你说"可以"。  
三周后你发现它漏掉了一个显而易见的问题。

**Loop Anything 解决这个。**

它启动 2–3 个完全隔离的 AI 审查员，每个从不同角度挑你产出的毛病——而且它们互相看不到对方的审查意见。审查员提意见，你的 Agent 修改，循环，直到每个审查员都没有东西可以再挑为止。

> 这个 skill 用更多 token 换取更高质量。它比单次对话慢，也更贵。  
> 只在那些最重要的 5% 产出上用它——那些出错代价远高于多花几倍 token 的场景。

---

## 它适合什么

任何"AI 看起来回答了但你不确定够不够好"的场景：

- 整个团队要依赖的方案文档
- 要给领导汇报的商业案例（或者给领导的领导）
- 既要健康又要你真的愿意坚持下去的饮食计划
- 一段需要说对的话——给客户、给伴侣、给重要的人
- 你很想拿到的职位的求职信
- 要跑在生产环境里的 system prompt
- 任何难以反悔的决定

Skill 会自己判断你的产出需要从哪些角度审查。你不需要配置任何东西。

---

## 运作方式

你的 Agent 会启动多个完全隔离的审查员——每个只看到你的产出和自己的审查角度，看不到彼此。就像你脑子里同时出现了几个声音，一个说"这个方向对"，另一个说"等等，有个问题你没考虑到"，它们争到没有争点为止。

```
审查员 A  ──┐
             ├──→  修改  ──→  循环  ──→  直到全部 120 分
审查员 B  ──┘
```

**120 分** = 这个审查员没有任何东西可以再挑。低于 120 就继续改。

> 为什么是 120 而不是 100？因为 90/100 意味着「差不多了」，120/120 意味着「我真的没有任何可以挑的了」。更高的上限迫使审查员持续寻找直到真正没有问题，而不是「感觉还行」就停下来。

直接说你的顾虑就行，Agent 会读取 Skill 并自动运转整个流程：

> *"我不确定这份方案经不经得起挑剔的眼光——发出去之前帮我压力测试一下。"*
>
> *"这个计划得同时满足我的时间安排和实际目标——帮我找出冲突的地方。"*
>
> *"这个决定感觉哪里不对，但我说不出来。帮我循环一遍。"*

---

## 快速安装

选你的平台，复制那行命令，粘贴给你的 Agent。Agent 执行安装后会确认 Skill 已就绪。

**Cursor**
```
请执行：git clone https://github.com/Ariesshin/loop-anything-skill ~/.cursor/skills/loop-anything-skill
```
→ 克隆到 Cursor 全局 skills 目录，安装后立即可用。

**Claude Code**
```
请执行：git clone https://github.com/Ariesshin/loop-anything-skill ~/.claude/skills/loop-anything-skill
```
→ 克隆到 Claude Code 全局 skills 目录。Skill 会自动激活——Claude Code 读取你的请求时，会在需要时自动加载，无需手动触发。如需项目局部安装，把 `~/.claude/skills/` 换成项目根目录下的 `.claude/skills/loop-anything-skill`。

**Codex / OpenCode / OpenClaw / ClawHub**
```
$skill-installer install https://github.com/Ariesshin/loop-anything-skill
```
→ `$skill-installer` 是 Codex、OpenCode 和 OpenClaw 兼容 Agent 的内置命令，无需单独安装。粘贴到会话中，重启后即可使用。也可在 [ClawHub](https://clawhub.ai/Ariesshin/loop-anything-skill) 搜索安装（上架后可用）。

**其他平台（包括 Ollama / LM Studio / 本地模型）**
```
请获取 https://raw.githubusercontent.com/Ariesshin/loop-anything-skill/main/SKILL.md，读取它并按照里面描述的工作流执行
```
→ 适用于能访问 URL 的平台。ChatGPT / Claude.ai 等网页版无法获取 URL，请用浏览器打开 [SKILL.md](https://raw.githubusercontent.com/Ariesshin/loop-anything-skill/main/SKILL.md)，全选复制，粘贴为第一条消息。

**安装完成后，说：** *「帮我对这份 [文档/方案/决定] 做 Loop 审查，我需要它无懈可击。」* Skill 会自动接管后续流程。

---

## 平台兼容性

| 等级 | 平台 | 你得到什么 |
|---|---|---|
| **Tier 1** — 真正隔离 | Cursor、Claude Code、Codex、OpenCode | 每个审查员在完全隔离的会话中运行，视角真正独立 |
| **Tier 2** — 有限隔离 | Windsurf、Roo Code、LangGraph、AutoGen、CrewAI、GitHub Copilot、Aider | 先运行隔离探针；探针失败则降级至 Tier 3 |
| **Tier 3** — 降级模式 | Claude.ai 网页版、ChatGPT 网页版、Gemini、Continue.dev、Ollama（Hermes / Mistral 等）、LM Studio | 同一个 Agent 顺序自评；以建议性意见输出并明确声明 |

完整说明：[`references/runtime-compatibility.md`](references/runtime-compatibility.md)

---

## 仓库结构

```
loop-anything-skill/
├── SKILL.md                        # Agent 读取并执行的工作流
├── templates/
│   ├── reviewer-packet.md          # 发给每个审查员的有界上下文格式
│   ├── reviewer-output.md          # 审查员输出格式 + 评分标准
│   ├── issue-ledger.md             # 主 Agent 的轮次问题追踪表
│   └── final-summary.md            # 最终交付摘要模板
├── references/
│   ├── runtime-compatibility.md    # 平台 Tier 分类
│   ├── facet-patterns.md           # 按产出类型的审查角度
│   └── evidence-guide.md           # 按产出类型的证据预期
└── scripts/
    └── validate_loop_review.py     # 最终轮次验证脚本
```

---

## License

MIT — see [LICENSE](LICENSE)