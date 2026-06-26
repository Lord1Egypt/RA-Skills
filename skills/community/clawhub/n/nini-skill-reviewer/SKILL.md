---
name: skill-reviewer
description: >-
  Use this skill to audit, review, or validate Claude Code skills (.md files in
  .claude/commands/). Invoke when user wants to check skill quality, cross-platform
  compatibility, cross-agent compatibility, prerequisite declarations, or description
  triggering accuracy. Triggers on: 审查 skill, review skill, 检查 skill 质量,
  skill 兼容性检查, validate skill, audit skill. This skill delegates structure
  validation to validate.sh, content quality to skill-creator, and handles
  compatibility auditing itself. Do NOT use for general code review, reviewing PRs,
  or reviewing CLAUDE.md.
metadata: {"openclaw":{"emoji":"🔍"}}
---

# Skill Reviewer

审计 Claude Code skills 的质量和兼容性。作为编排器，委托已有工具处理结构/质量检查，自身专注兼容性审计。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| skill-creator | skill | Yes | Built-in on most AI coding agents (Claude Code, Cursor, etc.) |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## 审计流程

### Step 1: 结构校验（委托）

运行 skill-reviewer 自带的校验脚本，汇总 YAML frontmatter、name 格式、description 格式等结果：

```bash
bash <skill-reviewer-dir>/scripts/validate.sh
```

> 若脚本不可用（如未通过 npx skills 安装），手动检查每个 SKILL.md 的 YAML frontmatter：name（hyphen-case，≤64 字符）、description（无尖括号，≤1024 字符）。

### Step 2: 内容质量（委托）

**MUST 执行**：调用 `skill-creator` skill 进行深度质量审查（token 效率、渐进式披露、反模式、description 基准测试等）。

若 `skill-creator` 不可用，**MUST 停下并引导用户确认**，不得跳过。大多数 AI 编码 agent 内置了 skill-creator：

- Claude Code: `document-skills:skill-creator` 或 `skill-creator:skill-creator`
- 其他 agent: 检查对应的 skill 管理功能

> 此步骤不可跳过。没有 skill-creator 的审计是不完整的。

### Step 3: 兼容性审计（自身核心）

按 `references/compatibility-checklist.md` 逐项检查目标 skill 的所有文件（SKILL.md + scripts/ + references/）：

**3a. 跨平台兼容性** — 扫描平台锁定模式（macOS-only 命令、Windows 不兼容项等）。

**3b. 跨 Agent 兼容性** — 检测 Claude Code 专属工具引用和 MCP 依赖。

**3c. npx skills 生态兼容性** — 校验 marketplace.json 注册、symlink 可用性、跨 skill 依赖。

**3d. 工具引用规范** — 检查是否保留了 Claude Code 工具术语并提供了其他环境的 fallback 备注。详见 checklist 的 "Tool Reference Best Practices" 部分。

**3e. Prerequisites 声明** — 检查 SKILL.md 是否声明了外部依赖：

- 如果 skill 使用了外部 CLI 工具（`git`, `gh`, `reminders-cli` 等）、MCP 服务器、或其他 skill，MUST 有 `## Prerequisites` 章节
- Prerequisites 必须是 body 中第一个 `##` 章节
- 章节内 MUST 包含 4 列表格：Tool / Type / Required / Install
- Type 列 MUST 使用标准值：`cli`, `mcp`, `skill`, `system`
- 表格后 MUST 有被动检查说明（blockquote），明确要求在执行失败时直接引导用户完成安装配置，而非指向外部文档
- 需要配置的工具（如 MCP 服务器、需要 auth 的 CLI）SHOULD 在 Install 列提供可执行的安装命令和配置步骤，或引用 skill 自带的 references/ 文档
- 无外部依赖的 skill 不需要此章节

详见 `references/compatibility-checklist.md`。

### Step 4: 输出报告

使用以下格式输出统一报告：

```markdown
## Skill Review: {skill-name}

### 总览
| 维度 | 状态 | 方式 |
|------|------|------|
| 结构与元数据 | PASS / FAIL | validate.sh |
| 内容质量 | PASS / FAIL (N issues) | skill-creator |
| 平台兼容性 | PASS / FAIL (N issues) | 自查 |
| Agent 兼容性 | PASS / FAIL (N issues) | 自查 |
| npx skills 生态 | PASS / FAIL (N issues) | 自查 |
| Prerequisites 声明 | PASS / WARN / N/A | 自查 |

### Critical
- **[维度]** 问题描述
  当前: ...
  建议: ...

### High
...

### Medium / Low
...
```

严重度分级：

- **Critical** — 功能不可用或分发失败，必须修复
- **High** — 显著影响可用范围，建议修复
- **Medium** — 可改进项，不影响核心功能
- **Low** — 建议性改进
