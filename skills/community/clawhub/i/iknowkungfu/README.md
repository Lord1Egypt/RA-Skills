# iknowkungfu 🥋

**Your agent doesn't know what it's missing. This skill does.**

## The Problem

ClawHub has 13,700+ skills and growing. Finding the right ones for your specific workflow means browsing endless lists or hoping someone on Reddit mentions something useful. Most agents run with 5-10 skills when they could benefit from 20-30.

## The Solution

iknowkungfu analyzes your agent's actual workflow and recommends the specific ClawHub skills you're missing. Every recommendation includes a trust score and a clear reason tied to YOUR usage, not generic "top 10" lists.

## How It Works

1. Run `/kungfu`
2. The skill reads your workspace (memory, skills, config, recent logs)
3. It builds a Workflow Profile showing what you actually do
4. It matches gaps against a curated index of quality ClawHub skills
5. You get personalized recommendations with trust scores and install commands

## Features

- 🔍 **Workflow profiling** — understands what your agent actually does
- 🎯 **Gap detection** — finds categories where you have zero coverage
- 📋 **Curated recommendations** with trust scores (0-5 stars)
- 🛡️ **Security filtering** — never recommends flagged or suspicious skills
- 🧠 **Gets smarter** the more you use your agent (more logs = better profile)
- 🔒 **100% local** — no data leaves your machine, ever

## Commands

```
/kungfu          Full scan with top 5 recommendations
/kungfu-scan     Workflow profile only
/kungfu-gaps     Show uncovered areas
/kungfu-update   Refresh skills index
```

## Example Output

```
🥋 I KNOW KUNG FU — Recommendations
═══════════════════════════════════════

Based on your workflow, you're missing these:

1. 🟢 slack (★ 4.5)
   Category: Communication | Author: steipete
   Why: You mention Slack in 4 of your last 7 daily logs
        but have no Slack integration skill.
   Install: clawhub install slack
   ─────────────────────────────────

2. 🟢 obsidian (★ 4.3)
   Category: Knowledge | Author: steipete
   Why: You reference notes and documentation frequently
        but have no PKM skill installed.
   Install: clawhub install obsidian
   ─────────────────────────────────

═══════════════════════════════════════
💡 /kungfu-gaps for all uncovered areas
═══════════════════════════════════════
```

## Trust & Safety

- **Read-only.** Never installs anything automatically.
- **Never sends data anywhere.** Zero network calls.
- Filters out skills with fewer than 50 downloads, VirusTotal flags, or excessive permissions.
- Recommendations include reasoning so you can judge for yourself.
- Quick security check on installed skills included (for deep scanning, use ClawSpa).

## Install

```
clawhub install iknowkungfu
```

## Links

- Issues: [github.com/whooshinglander/iknowkungfu](https://github.com/whooshinglander/iknowkungfu)

Built by [@whooshinglander](https://clawhub.com/whooshinglander)

---

# iknowkungfu 🥋 — 简体中文

**你的智能体不知道自己缺什么。这个技能知道。**

## 问题

ClawHub 有 13,700+ 个技能，还在增长。找到适合你工作流的技能意味着浏览无尽的列表，或者期望有人在 Reddit 上推荐。大多数智能体装了 5-10 个技能就不管了，实际上可能需要 20-30 个。

## 解决方案

iknowkungfu 分析你的智能体的实际工作流，推荐你缺少的 ClawHub 技能。每条推荐都包含信任评分和针对你具体使用场景的理由，不是泛泛的"热门排行"。

## 工作原理

1. 运行 `/kungfu`
2. 技能读取你的工作区（内存、技能、配置、最近日志）
3. 生成工作流画像，展示你实际在做什么
4. 将缺口与精选 ClawHub 技能索引匹配
5. 输出个性化推荐，附带信任评分和安装命令

## 功能

- 🔍 **工作流画像** — 理解你的智能体实际在做什么
- 🎯 **缺口检测** — 找到没有技能覆盖的领域
- 📋 **精选推荐** — 带信任评分（0-5 星）
- 🛡️ **安全过滤** — 绝不推荐有安全标记或可疑的技能
- 🧠 **越用越准** — 使用日志越多，画像越准确
- 🔒 **100% 本地** — 数据绝不离开你的机器

## 命令

```
/kungfu          完整扫描 + 前 5 条推荐
/kungfu-scan     仅工作流画像
/kungfu-gaps     展示未覆盖领域
/kungfu-update   刷新技能索引
```

## 信任与安全

- **只读。** 绝不自动安装任何东西。
- **绝不发送数据。** 零网络请求。
- 过滤掉下载量低于 50、有 VirusTotal 标记或权限过高的技能。
- 推荐包含理由，由你自己判断是否安装。
- 附带已安装技能的快速安全检查（深度扫描请使用 ClawSpa）。

## 安装

```
clawhub install iknowkungfu
```

开发者：[@whooshinglander](https://clawhub.com/whooshinglander)
