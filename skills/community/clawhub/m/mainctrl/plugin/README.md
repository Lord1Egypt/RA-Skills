# mainctrl plugin

A `before_tool_call` hook for OpenClaw that intercepts destructive tool calls
from controlled agents. When an agent in the controlled list tries to run
`write`, `edit`, `exec`, `process`, or `apply_patch`, the plugin blocks the
call and returns a delegation message.

## Install

```bash
openclaw plugins install clawhub:mainctrl
```

Or from local source:

```bash
./scripts/mainctrl.sh plugin install
```

Restart the gateway after install.

## How it works

Every tool call hits the hook. Multiple checks, one file read:

1. `enabled` true? No → let it through.
2. Caller is a controlled agent? No → let it through.
3. Tool is on the blocked list? Yes → block. No → let it through.

`execAllowExcept` only takes effect when `exec` is in `blockedTools`. If `exec` is not blocked, all commands pass through regardless of this config.

For `exec`, the plugin also checks `execAllowExcept`: commands listed
as keys are allowed through unless their command line contains an allow-except
pattern (substring match). Commands not in the map fall through to the
normal block.

State lives in `skills/mainctrl/scripts/state.json`. The plugin reads it on
every invocation — one synchronous filesystem read. If the file is missing or
corrupted, it falls back to permissive mode (everything allowed).

## Pairs with the mainctrl skill

This plugin is one half of mainctrl. It needs the companion skill for
management — the skill's CLI script (`mainctrl.sh`) writes `state.json`;
the plugin reads it. Install both:

```bash
openclaw plugins install clawhub:mainctrl
openclaw skills install clawhub:mainctrl
```

## Config

See the skill's `scripts/state.json`:

```json
{
  "enabled": true,
  "controlledAgents": ["main"],
  "blockedTools": ["write", "edit", "exec", "process", "apply_patch"],
  "execAllowExcept": {
    "find": ["-exec", "-ok", "-delete", "-fprint", "|", "$(", ">", ">>"],
    "ls":   [">", ">>", "|"],
    "pwd":  [">", ">>", "|"],
    "sed":  [">", ">>", "|", ".java", ".py", ".js", ".html", ".css"],
    "cat":  [">", ">>", "|"]
  }
}
```

Set to empty to disable a control:
- `"blockedTools": []` — no tools blocked
- `"execAllowExcept": {}` — no exec exceptions, all exec blocked
- `"controlledAgents": []` — clear all (falls back to default `["main"]`)

## Files

- `index.js` — the `before_tool_call` hook
- `package.json` — npm package metadata
- `openclaw.plugin.json` — plugin registration
