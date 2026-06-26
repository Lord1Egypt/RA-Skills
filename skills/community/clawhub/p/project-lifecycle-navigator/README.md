# Project Lifecycle Navigator / 项目生命周期导航助手

**Project Lifecycle Navigator** is a bilingual English/Chinese instruction-only Skill for guiding non-technical users and AI Coding Agent workflows through the full project lifecycle.

**项目生命周期导航助手** 是一个中英双语、纯文本指令型 Skill，适合非技术用户、创业者、运营团队、产品负责人和 AI Coding Agent 用户使用。

It routes the conversation into one of three modes:

它会根据用户当前情况自动进入三种模式之一：

1. **New Project Intake / 新项目需求访谈**  
   Turn a vague idea into a scoped MVP, project plan, technical approach, and Coding Agent execution plan.

2. **Mid-Project Realignment / 项目中期方向校准**  
   When a project feels off-track, bloated, or confusing, use structured review questions, assumption-challenging, MVP boundary control, and stop-loss decision-making.

3. **Code Review & Upgrade Plan / 代码审查与升级优化**  
   Review an existing codebase for security, dead code, logic bugs, performance, architecture, testability, dependencies, and produce an executable upgrade plan.

---

## Why this Skill exists / 为什么需要这个 Skill

Many non-technical users do not know how to describe complete software requirements, evaluate whether a project is drifting, or ask an AI Coding Agent for a safe code review.

很多非技术用户不知道如何完整描述软件需求，也不容易判断项目是否跑偏，更不知道如何让 AI Coding Agent 做安全、可执行的代码审查。

This Skill solves that by asking the right questions at the right time.

本 Skill 的核心价值是：**在正确阶段问正确的问题**。

---

## File Structure / 文件结构

```text
project-lifecycle-navigator/
  SKILL.md
  README.md
  skill.json
  .clawhubignore
  prompts/
    zh/
      01-new-project-intake.zh.md
      02-midproject-realignment.zh.md
      03-code-review-upgrade.zh.md
    en/
      01-new-project-intake.en.md
      02-midproject-realignment.en.md
      03-code-review-upgrade.en.md
  examples/
    usage-examples.md
  publish/
    CLAWHUB_LISTING.zh.md
    CLAWHUB_LISTING.en.md
    PUBLISHING.md
```

---

## Trigger Examples / 触发示例

### New Project Intake / 新项目需求访谈

> I want to build a new AI tool, but I don't know how to describe the requirements. Ask me questions first.

> 我想做一个新的 AI 工具，但我不懂技术，你先问我问题。

### Mid-Project Realignment / 项目中期方向校准

> The project is halfway done, but it feels like the MVP is getting too big. Help me recalibrate.

> 项目做到一半感觉跑偏了，功能越来越多，帮我重新校准方向。

### Code Review & Upgrade Plan / 代码审查与升级优化

> I have a codebase. Review it for security issues, dead code, architecture problems, and give me an upgrade plan.

> 我已经有代码了，帮我检查漏洞、冗余代码、架构问题，并生成升级优化计划。

---

## Install / 安装

For local use, place the folder in your OpenClaw skills directory or install it through ClawHub after publishing.

本地使用时，把整个文件夹放入 OpenClaw 支持的 skills 目录；发布到 ClawHub 后，也可以通过 ClawHub 安装。

After publishing, typical commands may look like:

```bash
openclaw skills install project-lifecycle-navigator
```

or:

```bash
clawhub install project-lifecycle-navigator
```

Exact commands may vary by OpenClaw/ClawHub version.

---

## Publish to ClawHub / 发布到 ClawHub

See:

```text
publish/PUBLISHING.md
```

This Skill is instruction-only and declares no required environment variables, binaries, network permissions, or install scripts.

本 Skill 是纯文本指令型 Skill，不声明任何必需环境变量、命令行工具、网络权限或安装脚本。
