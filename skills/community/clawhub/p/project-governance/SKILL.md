---
name: project-governance
description: Set up and maintain a project governance workspace for AI-assisted long-running projects — project protocol (AGENTS.md), directory index (index.md), error log (LESSONS.md), session handoff, changelog, stable version index (VERSIONS.md), whitelist/blacklist parameter registries. 为 AI 长期项目建立「项目记忆 + 文件索引 + 工作规则 + 版本记录」的治理系统，让 AI 在长期项目里「不忘事、不乱改、不重复犯错」，换会话后仍能接着做。Use when the user complains the project is messy, files are scattered or misplaced, the AI repeats mistakes or uses wrong versions, the user expects the AI to find files itself instead of asking for paths, when starting a new AI-assisted project, onboarding an AI agent into an existing project, or when a project lacks structured rules/versioning. 触发场景：项目太乱、文件乱、找不到文件、乱放文件、又用错版本、项目太多怎么管理、上次做到哪、你不是应该记得吗、哪个才是最终版、建立规则、版本索引、黑白名单。
---

# Project Governance

> 中文：给 AI 长期项目建立一套「项目记忆 + 文件索引 + 工作规则 + 版本记录」的管理系统，让 AI 换会话、换模型后仍能正确接着项目做，而不是重新猜项目。

## 30-second overview

这个 Skill 给项目增加 8 个东西：

1. 项目规则 —— AI 应该怎么做
2. 文件地图 —— 文件在哪里
3. 项目状态 —— 现在做到哪里
4. 错误记录 —— 以前踩过什么坑
5. 版本索引 —— 哪个版本才是真的
6. 黑白名单 —— 什么能用、什么不能用
7. 会话交接 —— 上一个 AI 做到哪里
8. 变更记录 —— 为什么这么改

核心目标：**让 AI 换会话、换模型、甚至换 Agent 后，仍然能正确接着项目做，而不是重新猜项目。**

## When to Use

Use this skill when:

- The user complains the project is messy, files are scattered, or the AI keeps misplacing files ("你怎么又乱放文件").
- The user expects the AI to find files itself instead of asking for paths ("你自己找").
- The AI keeps repeating mistakes or using wrong versions.
- The user says "你不是应该记得吗？" / "上次不是已经验证过了吗？" / "哪个才是最终版？" / "别重新做，之前已经跑通了" — Memory + Governance boundary scenarios where memory alone is not a reliable authority.
- Starting a new AI-assisted project and you want the agent to follow a stable protocol from day one.
- Onboarding an AI agent into an existing project that has no rules, error log, or parameter registry.
- A project has grown messy: files scattered, parameters changed without record, past mistakes repeated.
- You want to enforce durable rules such as "index-first file lookup", "plan before execute", "file existence ≠ file validity", or "registry-driven parameter selection".

Do NOT use this skill when:

- The task is a one-off question or small edit that does not need project-wide conventions.
- The project already has a mature governance system and you only need a small rule tweak — edit the existing files directly instead.

## Memory & Governance Boundary

Platform memory (e.g. Trae user profile / project memory) is a **context source,
not an authoritative fact store**. Governance files are the **project execution
protocol**. The two complement each other:

| Layer | What it answers |
|---|---|
| Platform memory | "What happened before / how does this user usually work" |
| Governance files | "How this project must work now, where files are, which version is authoritative" |

Authority priority when they conflict:

1. Current project files / frozen versions
2. Project governance files (`AGENTS.md`, `index.md`, `VERSIONS.md`, registries)
3. Project memory
4. User long-term memory
5. AI inference

When memory and governance files disagree, **governance wins**. Durable
conventions learned from memory must be settled into the governance files after
human confirmation — memory alone never becomes the project's authority.

## Instructions

### Step 1 — Scaffold

```bash
python scripts/governance.py init --project-dir /path/to/project --project-name "My Project"
```

Creates 11 governance files from `templates/` (never overwrites existing files unless `--force`).

### Step 2 — Customize

Edit the generated `AGENTS.md`: directory permission zones, autonomy levels, artifact placement rules, and project-specific rules under "Project Customization". Keep the universal Core Governance Rules as-is.

### Step 3 — Maintain (every session)

1. **Session start**: read `index.md` → `session_handoff.md` → `LESSONS.md`; before generating parameters, read `blacklist.json` / `whitelist.json`.
2. **During work**: find files via the index (never blind search); inherit whitelist entries with `score > 0.85`; never use `permanent_ban: true`; record new mistakes in `LESSONS.md`.
3. **Session end**: update `session_handoff.md`, `index.md` (file changes), `CHANGELOG.md` (decisions).

### Step 4 — Validate, index, check

```bash
python scripts/governance.py validate --project-dir /path/to/project   # registries conform to schema
python scripts/governance.py index --project-dir /path/to/project      # rebuild index.md map (links + notes)
python scripts/governance.py check --project-dir /path/to/project      # health gate: files + registries + fresh index
```

### Input / Output

- **Input**: a project directory (with or without existing governance files), a project name, and the user's governance pain points (messy files, wrong versions, repeated mistakes, "你自己找").
- **Output**: a governance workspace (`AGENTS.md`, `index.md`, `VERSIONS.md`, `LESSONS.md`, `session_handoff.md`, `CHANGELOG.md`, `whitelist.json` / `blacklist.json`) plus a validated, up-to-date index.

### On Failure

- `init` fails (invalid path, permission): report the exact failing command and reason; do not partially scaffold or guess.
- `validate` reports schema errors: fix the registry entries; never bypass validation.
- `check` fails (missing files / stale index): run `index`, then re-run `check`; if still failing, report to the human.
- Never fabricate a "passed" result — report what was verified and what was not.

## What It Produces

| File | Purpose |
|---|---|
| `AGENTS.md` | Project protocol: core governance rules, authority levels, first-run protocol, permission zones, trust boundary |
| `index.md` + `index_notes.json` | Authoritative directory map with clickable links and short notes |
| `VERSIONS.md` | Stable version index with human judgments |
| `LESSONS.md` | AI error & correction log |
| `session_handoff.md` | End-of-session handoff |
| `CHANGELOG.md` | Decision & version history |
| `whitelist.json` / `blacklist.json` | Verified / failed parameter registries |
| `ARCHITECTURE.md` / `PROJECT.md` | Architecture & project card |

## Details

- `README.md` — full package overview: Core / CLI / Skill-adapter structure, subcommands, limitations, Trae cold-start acceptance test
- `templates/` — governance file templates
- `scripts/governance.py` — init / validate / index / check CLI

## Limitations

This package is currently designed and tested primarily for Trae Skills. Other agents may use the generated governance files, but automatic Skill discovery/loading is not guaranteed outside Trae. The governance files and CLI are kept agent-neutral for future adapters.
