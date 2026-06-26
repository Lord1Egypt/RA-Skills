---
name: mttsports-session-bootstrap
description: "OpenClaw fallback only: verify that the CLI package already ships `mttsports_watch_in_bg`. Never write watcher scripts into the workspace; this skill only checks availability and tells the user how to recover when the packaged bin is missing."
---

# mttsports session bootstrap

This skill is an OpenClaw-specific fallback, not the default watch strategy.

Use it only when:

1. The current agent runtime cannot keep `mttsports session watch` alive with its own background-task or callback capability.
2. The availability check in [`../SKILL.md`](../SKILL.md) reported `MISSING`.

Do not load this skill when the agent runtime can manage `mttsports session watch` directly.

## Goal

Confirm that the packaged fallback bin `mttsports_watch_in_bg` is available and ready to use.

This skill no longer writes `watch-agent.js`, creates workspace files, or asks the agent to assemble a router script on the fly.

## Check Steps

### Step 1: Verify the packaged bin exists

```bash
command -v mttsports_watch_in_bg
```

If the command prints a path, the packaged fallback is installed.

If the command fails:

1. Tell the user the current CLI install does not yet include `mttsports_watch_in_bg`.
2. Ask them to reinstall or upgrade `@mtt-open/mttsports-cli`.
3. After reinstall, ask them to start a fresh OpenClaw session so the environment reloads the new bin.

### Step 2: Verify the packaged bin responds

```bash
mttsports_watch_in_bg --help
```

If the help text prints successfully, the packaged fallback is ready.

## Launch Example

Use this only for the OpenClaw fallback path.

```bash
OPENCLAW_SESSION_ID=$(openclaw sessions list --limit 1 --output json | python3 -c "import sys,json; print(json.load(sys.stdin)['results'][0]['sessionId'])")

mttsports_watch_in_bg \
  --session-id "$OPENCLAW_SESSION_ID" \
  --channel discord \
  --target "channel:<id>"
```

The launcher returns JSON similar to:

```json
{
  "ok": true,
  "session_id": "session_xxx",
  "pid": 12345,
  "pid_file": "/Users/you/.mttsports-cli/watch-router.pid",
  "log_file": "/Users/you/.mttsports-cli/watch-router.log"
}
```

Notes:

- If `--session-id` is omitted, `mttsports_watch_in_bg` resolves the latest OpenClaw session automatically.
- Callback attempts, callback arguments, watcher stderr, and watcher lifecycle logs are written into `log_file`.
- If `MTTSPORTS_CONFIG` is set, the default `pid_file` and `log_file` follow that config directory.

## Stop Example

```bash
kill -TERM $(cat /path/from/pid_file)
```

## Failure Handling

If launch fails, do not pretend the automation loop is live.

Instead:

1. Surface the exact launcher error.
2. If the launcher returned `log_file`, inspect it.
3. Tell the user whether the blocker is:
   - missing packaged bin
   - OpenClaw session lookup failure
   - background launch readiness failure
   - callback execution failure inside the router log
