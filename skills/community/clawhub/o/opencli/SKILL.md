---
name: opencli
description: Use the local OpenCLI source install at `/Users/ShiXin/Documents/Workspace/github-project/opencli` as the primary `opencli` skill. Load this when the user explicitly asks to use OpenCLI or `skill opencli`, or when a task maps well to OpenCLI adapters/external-CLI passthrough instead of generic browser automation. Covers capability discovery, browser-bridge health checks, Twitter/X routing, and stable command invocation.
---

# opencli

This is the canonical OpenCLI skill for this workspace.

Use it when the user says any of:

- `opencli`
- `skill opencli`
- `use OpenCLI`
- `用 opencli`

Also use it when a request is better handled by an existing OpenCLI adapter than by ad-hoc browser driving.

## Canonical entrypoint

Always invoke OpenCLI through this wrapper first:

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh <args...>
```

Wrapper behavior:

- prefers the source build at `/Users/ShiXin/Documents/Workspace/github-project/opencli/dist/main.js`
- falls back to the global `opencli` binary only if the source build is unavailable

This avoids old global installs and keeps behavior aligned with the source repo.

## Current source of truth

**Version:** local source build 1.7.7 (source repo) | global npm 1.7.8 (fallback).

**自动同步：** 本地 source repo 由 cron job `每周二技能升级检查`（每周二 09:00）自动同步 origin/main。无需手动更新。

Do not hard-code site command lists from memory.

At the start of a task, prefer:

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh list -f json
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh <site> --help
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh <site> <command> --help
```

Important top-level commands currently available from the local source build include:

- `list`
- `validate`
- `verify`
- `explore|probe`
- `synthesize`
- `generate`
- `record`
- `cascade`
- `doctor`
- `plugin`
- `install`
- `register`
- external CLI passthrough such as `gh`, `docker`, `lark-cli`, `vercel`

## Health model

Run this when checking the browser bridge:

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh doctor --no-live
```

Interpretation:

- `doctor` only diagnoses the browser bridge
- `PUBLIC` or non-browser discovery commands can still work when doctor is not green
- browser-backed adapters usually need the Browser Bridge extension and/or a logged-in browser session

## Output rules

- Prefer `-f json` for agent use
- Use `--help` before assuming argument shapes
- Return the exact command used when that helps future reuse

## Twitter / X routing

Use the correct command for the job:

```bash
# Search uses a positional query, not --query
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter search "OpenAI" --limit 10 -f json

# Single tweet / thread by tweet ID or status URL
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter thread 2047128854389465296 -f json

# Long-form article / note-tweet-like article content
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh twitter article 2047128854389465296 -f json
```

Important routing notes:

- `twitter search` is `opencli twitter search <query>`
- there is no `opencli twitter id ...` subcommand
- when the user gives a tweet ID or status URL, prefer `twitter thread` over `twitter search`
- `twitter search` depends on search results and indexing; it is not the right primitive for direct-ID retrieval

## Prefer OpenCLI when

- the user explicitly asks for OpenCLI
- the target site already has a stable OpenCLI adapter
- structured deterministic output is better than ad-hoc browser extraction
- you need OpenCLI external-CLI passthrough like `opencli gh ...`

## Prefer OpenClaw native browser when

- the task is generic UI automation
- the task depends on the current OpenClaw-managed browser session
- no clear OpenCLI adapter advantage exists

## References

- `scripts/opencli.sh` — canonical wrapper
- `references/commands.md` — validated command cookbook
- upstream source skill: `/Users/ShiXin/Documents/Workspace/github-project/opencli/skills/opencli-usage/SKILL.md`
