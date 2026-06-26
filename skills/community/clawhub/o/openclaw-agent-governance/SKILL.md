---
name: openclaw-agent-governance
description: |
  Set up or audit an OpenClaw agent workspace with standardized governance files.
  
  Use when: (1) creating a new agent workspace, (2) auditing existing agent files for compliance with governance standards, (3) onboarding a new agent, (4) user asks to set up or audit agent files.
  
  Creates/verifies: MEMORY.md (4-layer index), AGENTS.md (standard sections + agent-specific), memory/projects.md (Projects.md template), memory/lessons.md (Lessons template), memory/YYYY-MM-DD.md (daily log).
---

# agent-governance

为 OpenClaw agent workspace 建立标准化的治理文件体系。

## 使用场景

1. **新建 agent workspace** — 运行 `agent-governance apply <workspace-path>` 建立全套文件
2. **审计现有 agent** — 运行 `agent-governance audit <workspace-path>` 检查缺失和违规
3. **用户要求设置/审计** — 执行上述流程

## 标准文件体系

| 文件 | 作用 | 模板 |
|------|------|------|
| `MEMORY.md` | 长期记忆索引（Who + Index + Notes） | `references/MEMORY.md.template` |
| `AGENTS.md` | 职责说明 + 标准章节 | `references/AGENTS.md.template` |
| `memory/projects.md` | 项目状态（Projects.md 模板） | `references/projects.md.template` |
| `memory/lessons.md` | 经验教训（Lessons 模板） | `references/lessons.md.template` |
| `memory/YYYY-MM-DD.md` | 每日结论日志 | `references/daily-log.md.template` |

## MEMORY.md 标准结构

```markdown
## Who / Identity (stable)
- Name / Role / Timezone / Vibe / Emoji / Purpose

## Memory Index
- projects: memory/projects.md — 每个项目按 Projects.md 模板记录
- lessons: memory/lessons.md
- daily logs: memory/YYYY-MM-DD.md

## Notes
- 🚫 禁止执行 `gateway stop` 命令
- ⚠️ 执行 `gateway restart` 前必须征得用户同意
```

## AGENTS.md 标准章节

必须包含：
1. Every Session（启动顺序）
2. Responsiveness & Delegation Policy（>120秒 spawn sub-agent）
3. Red Lines（含 gateway stop/restart 两条禁止规则）
4. 4-Layer Memory System（标注按 Projects.md 模板记录）
5. Group Chats

## apply 命令（创建/更新）

对指定 workspace 执行以下操作：

### 1. 检查目录结构
```bash
WS="$1"
mkdir -p "$WS/memory"
```

### 2. 从模板生成/更新文件
- `MEMORY.md`：用 `references/MEMORY.md.template` 生成，替换 `[...]` 占位符
- `memory/projects.md`：不存在则从 `references/projects.md.template` 创建
- `memory/lessons.md`：不存在则从 `references/lessons.md.template` 创建
- `memory/YYYY-MM-DD.md`：不存在则从 `references/daily-log.md.template` 创建，日期为当天
- `AGENTS.md`：不存在则从 `references/AGENTS.md.template` 创建；已存在则**追加**标准章节（不覆盖 agent 专属内容）

### 3. 追加而非覆盖原则
- 如果 `AGENTS.md` 已存在且有 agent 专属内容（Mission Control API / 任务流程等），**不要覆盖**
- 只需确保包含标准章节（Responsiveness / Red Lines / 4-Layer Memory）
- 如果缺少标准章节，插入到 "## Group Chats" 之前

## audit 命令（检查合规）

对指定 workspace 执行：

1. 检查 `MEMORY.md` 是否存在且包含 Who/Identity + Memory Index + Notes（含 gateway 规则）
2. 检查 `AGENTS.md` 是否包含 Responsiveness + Red Lines（含 gateway 规则）+ 4-Layer Memory
3. 检查 `memory/projects.md` 是否存在
4. 检查 `memory/lessons.md` 是否存在
5. 检查 `memory/` 目录是否有当日 `YYYY-MM-DD.md`

输出格式：
```
=== Audit: <workspace> ===
✅ MEMORY.md
❌ AGENTS.md — 缺少 Red Lines
✅ memory/projects.md
✅ memory/lessons.md
✅ memory/2026-03-26.md
```

## 新建 agent 完整流程

```bash
# 1. 创建 workspace 目录
mkdir -p ~/.openclaw/workspace-<agent-name>

# 2. 应用治理文件
agent-governance apply ~/.openclaw/workspace-<agent-name>

# 3. 填充 agent 专属内容（手动或通过对话）
# - 编辑 MEMORY.md：填入 Who / Identity
# - 编辑 AGENTS.md：在 "## [Agent 专属职责]" 下添加专属内容
```

## 模板文件

所有模板位于 `references/` 目录：
- `references/MEMORY.md.template`
- `references/AGENTS.md.template`
- `references/projects.md.template`
- `references/lessons.md.template`
- `references/daily-log.md.template`

如需修改标准模板，编辑对应文件后重新 apply 即可。
