# HermesSkill 🤖

> Self-Evolution Skill Package — Give your AI Agent the ability to learn, improve, and create skills autonomously

[English](#english) · [中文](#中文) · [日本語](#日本語) · [한국어](#한국어)

---

## English

### Overview

HermesSkill is a self-evolution skill package inspired by Hermes Agent. It provides AI agents with capabilities for **self-learning**, **automatic skill creation**, **memory management**, and **continuous improvement**.

### Features

| Feature | Description |
|---------|-------------|
| 🚀 **Auto Skill Creator** | Automatically creates reusable skills from complex tasks (5+ tool calls) |
| 💡 **Smart Nudge System** | Intelligent reminders based on task complexity and time |
| 🔍 **Memory Management** | HOT/WARM/COLD three-tier memory system |
| 📊 **Skill Evaluator** | 1-5 star rating with improvement suggestions |
| ⏰ **Scheduled Self-Check** | Hourly automatic health checks |

### Installation

```bash
# Install via npx (recommended)
npx skills add devrobbin/hermes-skill@hermes-skill

# Or clone directly
git clone https://github.com/devrobbin/hermes-skill.git
```

### Quick Start

```bash
# Check all nudges
python3 scripts/evo_main.py nudge

# Add a memory
python3 scripts/evo_main.py remember "Important knowledge to remember"

# Search memories
python3 scripts/evo_main.py search "keyword"

# Evaluate a skill
python3 scripts/evo_main.py eval "skill-name,4"

# Run full self-check
python3 scripts/evo_main.py check
```

### Directory Structure

```
hermes-skill/
├── SKILL.md              # Skill definition
└── scripts/
    ├── evo_main.py           # Unified command entry
    ├── auto_skill_creator.py  # Auto skill creation
    ├── memory_tool.py         # Memory management
    ├── nudge_system.py        # Smart reminders
    ├── skill_evaluator.py     # Skill evaluation
    └── self_check_cron.sh     # Scheduled checks
```

### Comparison with Hermes Agent

| Feature | Hermes Agent | HermesSkill |
|---------|-------------|-------------|
| Memory Capacity | ~2200 tokens | ~2000 tokens (HOT) |
| Skill Creation | LLM generation | Template + Key Points |
| Evaluation | Implicit scoring | Explicit 1-5 rating |
| Scheduled Tasks | Fixed 30 min | OpenClaw cron |
| Cross-session Search | HermesDB (SQLite) | OpenClaw LCM built-in |

### Supported Agents

![OpenClaw](https://img.shields.io/badge/OpenClaw-✅-4FC3F7?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude_Code-✅-FF6B6B?style=flat-square)
![Cursor](https://img.shields.io/badge/Cursor-✅-7C3AED?style=flat-square)
![VSCode](https://img.shields.io/badge/VSCode-✅-007ACC?style=flat-square)
![Windsurf](https://img.shields.io/badge/Windsurf-✅-20B2AA?style=flat-square)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-✅-F59E0B?style=flat-square)

---

## 中文

### 简介

HermesSkill 是一个自进化技能包，灵感来自 Hermes Agent。它为 AI 智能体提供**自我学习**、**自动创建技能**、**记忆管理**和**持续改进**的能力。

### 功能特性

| 功能 | 说明 |
|------|------|
| 🚀 **自动技能创建** | 从复杂任务 (5+ 工具调用) 自动生成可复用技能 |
| 💡 **智能 Nudge 提醒** | 基于任务复杂度和时间的智能提醒 |
| 🔍 **记忆管理** | HOT/WARM/COLD 三层记忆系统 |
| 📊 **技能评估** | 1-5 星评分 + 改进建议 |
| ⏰ **定时自检** | 每小时自动健康检查 |

### 安装方式

```bash
# 通过 npx 安装（推荐）
npx skills add devrobbin/hermes-skill@hermes-skill

# 或者直接克隆
git clone https://github.com/devrobbin/hermes-skill.git
```

### 快速开始

```bash
# 检查所有 nudges
python3 scripts/evo_main.py nudge

# 添加记忆
python3 scripts/evo_main.py remember "要记住的重要知识"

# 搜索记忆
python3 scripts/evo_main.py search "关键词"

# 评估技能
python3 scripts/evo_main.py eval "技能名,4"

# 运行完整自检
python3 scripts/evo_main.py check
```

### 目录结构

```
hermes-skill/
├── SKILL.md              # 技能定义文件
└── scripts/
    ├── evo_main.py           # 统一命令入口
    ├── auto_skill_creator.py  # 自动技能创建
    ├── memory_tool.py         # 记忆管理
    ├── nudge_system.py        # 智能提醒
    ├── skill_evaluator.py     # 技能评估
    └── self_check_cron.sh     # 定时自检
```

### 与 Hermes Agent 对比

| 功能 | Hermes Agent | HermesSkill |
|------|-------------|-------------|
| 记忆容量 | ~2200 tokens | ~2000 tokens (HOT) |
| 技能创建 | LLM 生成 | 模板 + 关键点 |
| 评估方式 | 隐式评分 | 显式 1-5 分 |
| 定时任务 | 固定 30 分钟 | OpenClaw cron |
| 跨会话搜索 | HermesDB (SQLite) | OpenClaw LCM 内置 |

---

## 日本語

### 概要

HermesSkillは、Hermes Agentからインスピレーションを得た自己進化スキルパッケージです。AIエージェントに**自己学習**、**自動スキル作成**、**メモリ管理**、**継続的改善**の能力を提供します。

### 機能

| 機能 | 説明 |
|------|------|
| 🚀 **自動スキル作成** | 複雑なタスク (5+ ツール呼び出し) から再利用可能なスキルを自動生成 |
| 💡 **スマートNudgeシステム** | タスクの複雑さと時間に基づくインテリジェントなリマインダー |
| 🔍 **メモリ管理** | HOT/WARM/COLD 三層メモリシステム |
| 📊 **スキル評価** | 1-5段階評価 + 改善提案 |
| ⏰ **定期的自己チェック** | 毎時の自動ヘルスチェック |

### インストール

```bash
npx skills add devrobbin/hermes-skill@hermes-skill
```

---

## 한국어

### 개요

HermesSkill은 Hermes Agent에서 영감을 받은 자기 진화 스킬 패키지입니다. AI 에이전트에게 **자기 학습**, **자동 스킬 생성**, **메모리 관리**, **지속적인 개선** 능력을 제공합니다.

### 기능

| 기능 | 설명 |
|------|------|
| 🚀 **자동 스킬 생성** | 복잡한 작업 (5+ 도구 호출)에서 재사용 가능한 스킬 자동 생성 |
| 💡 **스마트 Nudge 시스템** | 작업 복잡성과 시간 기반 지능형 알림 |
| 🔍 **메모리 관리** | HOT/WARM/COLD 3계층 메모리 시스템 |
| 📊 **스킬 평가** | 1-5점 평가 + 개선 제안 |
| ⏰ **예약 자체 검사** | 매시간 자동 상태 확인 |

### 설치

```bash
npx skills add devrobbin/hermes-skill@hermes-skill
```

---

## Contributing & Development Guidelines

This skill package is itself a self-evolving system. Any improvements to modules must follow these rules:

### GitHub Sync Rule
> **Every self-evolution must be pushed to the GitHub repo.**

Workflow:
1. Make improvements in `~/.qclaw/skills/hermes-skill/`
2. `git add` + `git commit -m "description"`
3. `git push` to origin/main
4. Sync update `SKILL.md` / `README.md` if features changed

### Changelog Rule
> New modules, breaking changes, or API changes → append entry to `upstream-tracker/changelog.md`

Format:
```
## YYYY-MM-DD — vX.X.X
- [Change description]
- [File changes]
```

### What NOT to do
- ❌ Local-only changes, no push
- ❌ Update code without updating docs
- ❌ Overwrite existing upstream-tracker state files

## License

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Made with ❤️ by the OpenClaw Community</strong>
  <br>
  <a href="https://github.com/devrobbin/hermes-skill">GitHub</a> ·
  <a href="https://skills.sh/devrobbin/hermes-skill">skills.sh</a>
</p>
