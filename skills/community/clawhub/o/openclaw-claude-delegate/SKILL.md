---
name: claude-delegate
description: "Give Claude back to OpenClaw through a local Claude Code delegation lane with dispatch, poll, result, resume, and an optional non-root bypassPermissions runner. Use when: you want Claude subscription access available to OpenClaw agents through a stable local worker lane, need resume/monitoring in a bounded workspace, or need Claude auth separate from OpenClaw providers. Don't use when: the user explicitly wants an ACP chat harness or thread, use acp-router plus sessions_spawn(runtime: \"acp\"); the task is a simple edit or shell command, use edit/exec directly; or the local Claude runner is not set up yet, read references/setup.md first."
---

# Claude Delegate

Give Claude back to OpenClaw.

Use this skill when Claude Code should run as a **local delegated worker**, not as an ACP chat harness.

The whole point is simple: third-party harnesses do not reliably get Claude subscription access, but OpenClaw operators still want Claude-quality work inside their agent system.

## Stable entrypoints

- Wrapper: `scripts/claude-delegate.sh`
- Profile wrapper: `scripts/cc-profile.sh`
- Orchestrator: `scripts/cc-orchestrator.sh`
- Low-level runner: `scripts/run-task.sh`

## Default flow

1. Read `references/setup.md` the first time you install or port this skill.
2. Configure `profiles.json`, or point `CLAUDE_DELEGATE_PROFILES` at a host-local profiles file.
3. Keep local delegate instructions in the nearest `CLAUDE.delegate.md` files. The wrapper now tells Claude to discover/read those plus nearby `AGENTS.md`, `TOOLS.md`, and `README.md` docs before substantive work.
4. Dispatch work through `scripts/claude-delegate.sh dispatch <profile> <budget> <model> <label> "<task>"`.
5. Monitor with `poll`, `result`, `list`, or `doctor`.
6. Use `resume` to continue the same Claude session instead of starting over.

## When to prefer this over ACP

Prefer this skill when you want:
- a boring local wrapper around Claude CLI
- a non-root runner user with synced auth/binary state
- bounded filesystem access through a chosen workdir
- cheap monitoring and resume without a chat-thread harness

Prefer ACP when the user explicitly asked for Claude Code as a chat/thread runtime.

## Files to load when needed

- Setup, auth, env knobs, and profile customization: `references/setup.md`
- Delegate bootstrap guidance for this repo: `CLAUDE.delegate.md`

## Notes

- `scripts/cc-profile.sh` supports `CLAUDE_DELEGATE_PROFILES=/abs/path/to/profiles.json`.
- Profile paths support `~` and environment variable expansion.
- `scripts/ensure-nonroot-delegation.sh` supports env overrides for source paths if your Claude or acpx installs live somewhere else.
- Delegate bootstrap is on by default. Disable with `CLAUDE_DELEGATE_BOOTSTRAP=0` or change the instruction filename with `CLAUDE_DELEGATE_DOC_BASENAME`.
