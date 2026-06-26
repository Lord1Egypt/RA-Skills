---
name: persistent-code-terminal
description: Persistent per-project coding terminal (tmux). Run Codex CLI (codex exec) inside a stable session; mobile/SSH friendly.
user-invocable: true
metadata: {"openclaw":{"emoji":"💻","os":["darwin","linux"],"requires":{"bins":["tmux"]},"install":[{"id":"brew","kind":"brew","formula":"tmux","bins":["tmux"],"label":"Install tmux (brew)"},{"id":"apt","kind":"apt","package":"tmux","bins":["tmux"],"label":"Install tmux (apt)"}]}}
---

# persistent-code-terminal

A **persistent coding terminal** for OpenClaw. It creates a tmux session per project:

`<project-name>-code-session`

This makes terminal-first AI coding (Codex CLI / Claude Code / any CLI tool) reliable and **mobile/SSH friendly**:
- detach/reattach without losing output
- keep shell state across turns
- keep long-running tasks alive (dev server, watch mode, etc.)

## OpenClaw natural-language routing

When user intent is "use natural language to drive Codex CLI in this repo", route through this skill first.

Intelligent auto-trigger:
- Routing toggle: `openclaw.config.dev.autoCodeRouting` (default `false`).
- If enabled, route coding workflow messages via:
  - `{baseDir}/bin/persistent-code-terminal-route.sh "<user message>"`
- The route script applies:
  - intent detection (code change / fix / test / build / commit / push / codex phrases)
  - safety filtering (must be git repo + action verbs; bypass on `不要执行，只分析`)
  - execution chain:
    - `persistent-code-terminal-auto.sh --max-retries 3 --instruction "<message>"`
    - `persistent-code-terminal-summary.sh --lines 120`
  - fallback for missing deps (`tmux`/`codex`) with doctor guidance.

Multi-project routing:
- One message can include multiple project tasks split by newline / `；` / `;`
- Supported patterns:
  - `给 <project> 项目 <instruction>`
  - `给<project>项目：<instruction>`
  - `为 <project> 修复/增加/修改 ...`
  - `<project> 项目 ...；<project> 项目 ...`
- Execution is serial per project:
  - `start.sh --project <project>`
  - `auto.sh --max-retries 3 --instruction "<instruction>"`
  - `summary.sh --lines 120 --json`
- Invalid/unknown project tasks are reported as failed without blocking other tasks.

Trigger shortcuts (recommended):
- If user message starts with `codex `, treat the remaining text as instruction.
- Execute:
  - `{baseDir}/bin/persistent-code-terminal-codex-exec.sh "<remaining text>"`
- Then report with:
  - `{baseDir}/bin/persistent-code-terminal-status.sh`
  - `{baseDir}/bin/persistent-code-terminal-summary.sh --lines 120`

Preferred execution pattern in chat-driven runs:
- `start.sh` (or implicit auto-create from `send.sh`)
- `codex-exec.sh "<instruction>"` for Codex-driven work
- `status.sh` / `summary.sh` for concise progress reporting

If user says "检查项目/继续会话/跑测试并总结", use this skill scripts instead of asking user to type long shell commands.

## Core model (must follow)

**start → send → read → decide**

1) Start/ensure session:
- `{baseDir}/bin/persistent-code-terminal-start.sh`

2) Send ONE command:
- `{baseDir}/bin/persistent-code-terminal-send.sh "<command>"`
  - Appends a pane sentinel on completion: `__PCT_EXIT_CODE__N`
  - Supports: `--timeout <seconds>`, `--dry-run`, `--phase <name>`

3) Read output:
- `{baseDir}/bin/persistent-code-terminal-read.sh`
  - Parses the latest sentinel and updates `.pct-state.json`

4) Check state quickly (optional):
- `{baseDir}/bin/persistent-code-terminal-status.sh`
- `{baseDir}/bin/persistent-code-terminal-summary.sh --lines 120`
- `{baseDir}/bin/persistent-code-terminal-doctor.sh`
- `{baseDir}/bin/persistent-code-terminal-list.sh` (list `*-code-session`)
- `{baseDir}/bin/persistent-code-terminal-switch.sh --project <name>`

State file:
- `.pct-state.json` (current project directory)
- Fields: `projectDir`, `session`, `lastCommand`, `lastExitCode`, `phase`, `updatedAt`

Structured output:
- `{baseDir}/bin/persistent-code-terminal-read.sh --json`
- `{baseDir}/bin/persistent-code-terminal-summary.sh --json`
- `{baseDir}/bin/persistent-code-terminal-auto.sh --json`

## Codex-first workflow (one-shot)

If Codex CLI is installed as `codex`, prefer:

- `{baseDir}/bin/persistent-code-terminal-codex-exec.sh "<instruction>"`
- Default behavior uses:
  - `codex exec --full-auto --sandbox workspace-write --cd <current-dir> "<instruction>"`
- You can pass additional flags before the instruction:
  - `{baseDir}/bin/persistent-code-terminal-codex-exec.sh --json -o /tmp/codex.json "<instruction>"`
- Set `PCT_CODEX_NO_DEFAULT_FLAGS=1` to disable default flags.

Example:
- `{baseDir}/bin/persistent-code-terminal-codex-exec.sh "Implement feature X. Ensure build and tests pass. Commit and push to current branch. Do NOT force push."`

## Safety

- Never `git push --force` unless user explicitly requests.
- Keep secrets out of terminal output.
- Prefer feature branches; avoid direct pushes to main/master unless explicitly requested.
- For network/privileged actions (for example `git push`), follow active Codex approval/sandbox policy.
