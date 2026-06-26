---
name: my_skill_management_skill
description: 管理和发布用户自定义技能的统一接口。强制执行“my_”前缀、统一存放目录（~/.openclaw/skills）、基于配置文件（skills.json）的智能体绑定规则，并要求本地技能变更后必须立即通过clawhub上传备份。
---

# my_skill_management_skill

## Purpose (目的)
A wrapper for `clawhub` to standardize the publishing, installation, and governance workflow for custom user-created agent skills.

## Core Rules (核心规则与约束)
1. **范围限制 (Scope Limit)**：本技能仅适用于用户自己创建的专属技能。所有用户自定义的技能名称**必须以 `my_` 开头**（例如 `my_stock_report_skill`）。
2. **统一目录 (Directory Standard)**：用户自己创建或修改的专属技能，**必须统一放置在全局目录 `~/.openclaw/skills/` 下**，不允许存放在各智能体单独的工作区目录中。
3. **智能体绑定规则 (Agent Binding)**：如果要把某个技能绑定给指定的 Agent，**必须去修改对应 Agent 的配置文件**（即 `~/.openclaw/agents/{agent_name}/skills.json`），将技能名加入到 `"enabled_skills"` 列表中。禁止在 `SKILL.md` 中硬编码“仅限 xxx 使用”等文字描述来实现绑定。
4. **实时备份要求 (Auto-Backup/Publish)**：我本地的自定义技能（`my_` 开头）发生任何变更（新增或修改）后，**应当立即使用 clawhub 命令（或 helper 脚本）将最新版本上传备份**，确保云端与本地实时同步。

## Commands (命令)

### 1. Publish (上传与备份)
Standardize publishing with mandatory versions and changelogs.
```bash
bash scripts/clawhub_helper.sh publish <path> <version> "<changelog>"
```
或者直接使用原生的 clawhub 命令进行发布（推荐）：
```bash
clawhub publish ~/.openclaw/skills/<my_skill_name> --slug <my_skill_name> --name "<My Skill Name>" --version <version> --changelog "<changelog>"
```

### 2. Install (下载与搜索)
Search and install with optional version specification.
```bash
bash scripts/clawhub_helper.sh install <slug> [version]
```

## Features (特性)
- **Auto-versioning**: Ensures every publish has a version.
- **Verification**: Searches for skills before attempting to install.
- **Structure**: Enforces standard ClawHub formatting.
- **Strict Governance**: 强制执行前缀命名、全局路径和规范的 Agent 绑定流程。