---
name: openclaw-session-grep
version: 0.1.0
description: Search local OpenClaw session and transcript history with the openclaw-session-grep CLI. Use when debugging prior conversations, tool usage, cron behavior, panel failures, historical errors, expensive runs, or when looking for where something was said before. Prefer this over ad hoc rg/jq sweeps for transcript discovery; use jq only after narrowing to specific files.
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["/root/.openclaw/workspace/tools/ocgrep"] }
    }
  }
---

# openclaw-session-grep

Use this skill for transcript and session-history spelunking.

Default command:

```bash
/root/.openclaw/workspace/tools/ocgrep "keyword" --last 7d --open
```

## Best uses

- prior conversation lookup
- debugging dashboard/system panel history
- finding tool usage or failure strings
- tracing cron/job behavior over time
- locating model/session/channel-specific history

## Preferred workflow

1. Start with `ocgrep` to narrow by keyword, time window, tool, channel, or session.
2. Use `--summary` when you need the hot sessions first.
3. Use `--open` when you want exact file:line references.
4. Only switch to `jq` after you know which transcript file(s) matter.

## Good queries

```bash
/root/.openclaw/workspace/tools/ocgrep "api/system" --last 7d --open
/root/.openclaw/workspace/tools/ocgrep "morning briefing" --last 14d --summary
/root/.openclaw/workspace/tools/ocgrep "timeout" --tool-only --last 7d
/root/.openclaw/workspace/tools/ocgrep "message tool" --channel telegram --last 7d --open
```

## Important caveat

The upstream CLI can search broadly enough to include non-transcript files if you aim it at overly broad paths. Use it for session/transcript discovery first, not repo-wide code search. If results look noisy, tighten with `--path`, `--session`, `--channel`, `--last`, or `--tool-only`.

## Local install path on this host

The CLI is installed in an isolated venv at:

```bash
/root/.openclaw/venvs/openclaw-session-grep
```

Wrapper used for daily work:

```bash
/root/.openclaw/workspace/tools/ocgrep
```
