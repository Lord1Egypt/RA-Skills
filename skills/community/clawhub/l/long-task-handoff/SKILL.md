---
name: long-task-handoff
description: Ultra-light automatic handoff manager for long-running agent sessions at context-boundary moments. Use this skill when a runtime reports context compaction/summarization/resume-from-summary, low-context or before-context-eviction hooks fire, the user explicitly asks for a handoff/transfer/restart-session handoff, an agent is about to recommend restarting because context is unreliable, or a fresh session has an explicit active-handoff signal such as handoffs/ACTIVE.md or a provided handoff path. Do not trigger merely because the user says continue/keep going, or because a task has many changed files. Keep the user experience nearly invisible by calling the bundled Python manager.
metadata:
  agents: [codex, openclaw, hermes-agent, claude-compatible]
  requires:
    write_access: workspace-or-temp
    bins: [python]
  os: [windows, macos, linux]
---

# Long Task Handoff

Keep this skill lightweight. Do not manually reproduce the full handoff template in context. Use the bundled Python manager and keep user-facing messages short.

Detailed protocol is deferred to `references/protocol.md`. Do not load it during normal operation. Load it only if the manager is unavailable, the skill is being audited or modified, or a manual fallback is required.

## Use The Manager

Prefer:

```bash
python scripts/handoff_manager.py update --workspace . --task "Task name" --event context_compaction --compaction-count N
```

Installed script paths:

- Codex: `.codex/skills/long-task-handoff/scripts/handoff_manager.py`
- Hermes: `/root/.hermes/skills/software-development/long-task-handoff/scripts/handoff_manager.py`

Useful commands:

```bash
python scripts/handoff_manager.py create --workspace . --task "Task name"
python scripts/handoff_manager.py update --workspace . --task "Task name" --event context_compaction --compaction-count N
python scripts/handoff_manager.py recover --workspace .
python scripts/handoff_manager.py suggest --compaction-count N --json
python scripts/handoff_manager.py validate handoffs/session-handoff-*.md
```

Pass rich task facts with `--input-json` when available. Otherwise pass only concise CLI facts such as `--completed`, `--test-result`, `--key-file`, `--unfinished`, `--next-action`, `--risk`, and `--do-not-do`.

## Automatic Behavior

- First compaction: update handoff quietly.
- Second compaction: update handoff and verify `handoffs/ACTIVE.md`.
- Third compaction: update handoff and briefly say restart is advisable.
- Fourth compaction or state loss: update handoff and strongly recommend restart.
- Fresh session recovery: run `recover` only when there is an explicit handoff signal, such as `handoffs/ACTIVE.md`, a provided handoff path, a runtime resume marker, or the user mentioning handoff/session restart context.

The user should not need to know the handoff path once an active handoff signal is present, but ordinary continuation requests should not trigger this skill by themselves.

## Boundaries

The handoff is a restart packet, not a project wiki. Include only current restart-critical state: goal, branch/commit/worktree, delta, tests, key files, unfinished items, next actions, risks, and do-not-do items.

Do not include secrets, `.env` contents, private keys, long chat logs, stale plans, unverified guesses as facts, or descriptions that conflict with the current workspace. Put durable project knowledge in repo docs and reference it by path.

## If Script Fails

Do not silently continue. Report the concrete failure, keep the message short, and avoid asking the user to restate context unless `recover` cannot find or read a handoff.
