---
name: project-memory-workflow
description: Maintain AI-readable project memory for software repositories. Use when onboarding to a codebase, initializing project context, detecting missing project guidance or progress documents, preserving repository conventions and user changes, or recording implementation, verification, decisions, and risks. Trigger on requests such as "初始化项目", "初始化项目记忆", "init", "init project", "set up project memory", and "建立项目记忆". Support OpenAI/Codex AGENTS.md and Claude CLAUDE.md conventions.
---

# Project Memory Workflow

建立并维护一套轻量、可迁移的项目记忆，使不同 AI 工具接手同一仓库时能快速获得可靠上下文，并在每次工作后留下可验证记录。

## 1. Detect the project and conventions

- Identify the repository root from the current directory, Git metadata, workspace markers, or user-specified path. Do not scan or modify unrelated parent directories.
- Check for instruction files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, and other tool-specific files. Read all applicable instructions before editing.
- Treat `AGENTS.md` as the OpenAI/Codex convention and `CLAUDE.md` as the Claude convention. If both exist, preserve both and keep shared rules consistent; never replace one with the other.
- Check for `docs/README.md`, `docs/PROJECT.md`, `docs/DEVELOPMENT.md`, `docs/PROGRESS.md`, and `docs/DECISIONS.md`.
- Inspect Git status before editing. Preserve existing user changes and avoid destructive Git commands.

## 2. Decide whether to initialize

Use user intent, not missing files alone, to decide whether to write.

- During an ordinary development task, if canonical files are missing, report the missing files and ask whether the user wants project memory initialized. Continue only with read-only analysis until the user agrees; do not expand the requested task implicitly.
- When the user explicitly asks with `初始化项目`, `初始化项目记忆`, `init`, `init project`, `set up project memory`, `建立项目记忆`, or equivalent language, execute initialization without asking again.
- If only some files are missing, create only those files unless the user asks to restructure documentation.
- If another established documentation layout exists, adapt to it and record the mapping; do not create competing sources of truth.
- Never overwrite an existing instruction or project document merely to make it conform to this skill.

## 3. Initialize project memory

Gather facts from source, tests, routes, migrations, manifests, configuration, CI, and deployment files before writing. Separate confirmed facts from assumptions.

Create the missing minimal documents:

- `docs/PROJECT.md`: current product purpose, boundaries, modules, flows, interfaces, data rules, configuration boundaries, and known limitations.
- `docs/DEVELOPMENT.md`: prerequisites, local commands, test/typecheck/build commands, migration/deployment procedures, and start/finish workflow.
- `docs/PROGRESS.md`: dated, append-only timeline using `references/progress-entry-template.md`.
- `docs/DECISIONS.md`: durable technical or product decisions and reasons, not a duplicate timeline.
- `docs/README.md`: short map stating which document owns each kind of fact.

When no applicable instruction file exists, create a concise `AGENTS.md` by default. If the user primarily uses Claude or requests Claude compatibility, also create a small `CLAUDE.md` compatibility file pointing to shared rules instead of duplicating them. Follow `references/agent-file-compatibility.md`.

Require agents to read project memory before work, inspect existing changes, follow repository conventions, define success criteria and verification commands, protect secrets, and record results after work. Keep rules project-specific only when repository evidence supports them.

## 4. Use project memory during work

At task start, read the applicable instruction files, `docs/README.md`, `docs/PROJECT.md`, `docs/PROGRESS.md`, and relevant sections of `docs/DEVELOPMENT.md` and `docs/DECISIONS.md`. Then inspect source, tests, and configuration in scope.

Before editing, establish:

1. requested outcome;
2. affected modules and boundaries;
3. success criteria and verification commands;
4. risks or facts needing confirmation.

After editing, run checks proportional to risk, update current-state documentation when behavior changed, and append one progress entry containing goal, completed work, verification, and remaining items. Never claim a service, browser, device, database, or production deployment was verified when it was not.

## 5. Keep memory trustworthy

- Prefer code, tests, routes, migrations, configuration, and command output over old prose.
- Mark stale, unverified, and environment-dependent behavior explicitly.
- Keep current state in `PROJECT.md`, history in `PROGRESS.md`, and durable rationale in `DECISIONS.md`.
- Never write credentials, tokens, private URLs, or local secret values.
- Keep documents concise and avoid duplicating the same fact.

## References

- Read [agent-file-compatibility.md](references/agent-file-compatibility.md) when creating or reconciling agent instruction files.
- Read [memory-file-design.md](references/memory-file-design.md) when initializing or restructuring project memory.
- Read [progress-entry-template.md](references/progress-entry-template.md) when recording completed work.
