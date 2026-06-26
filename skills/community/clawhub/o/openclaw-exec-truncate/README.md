# exec-truncate

**Domain-aware output truncation for the OpenClaw `exec` tool.**

> _"My git diffs are 3,000 lines. My context window is finite."_

Installs as an OpenClaw plugin. Intercepts `exec` output, detects the command domain from output patterns, and compresses verbose output — git diffs, logs, grep results, directory listings, and build logs — down to their informative core.

**Token savings:** 20–40% on typical git/build/grep output.

---

## The Problem

The `exec` tool is OpenClaw's most-used tool — and its most wasteful. A single `git diff` can spit out 2,000+ lines. A `grep` across a codebase returns everything, everywhere. After a dozen commands, your context window is gone.

You don't need all those lines. You need:
- _What changed?_
- _What matched?_
- _What broke?_

exec-truncate gives you exactly that.

---

## Supported Domains

| Domain | Detects | What it does |
|--------|---------|-------------|
| `gitDiff` | `diff --git`, `index [hash]` | First 100 + last 20 addition lines. Strips headers, hunk markers, unchanged context. |
| `gitLog` | 40-char hash + `Author:` | One line per commit: `hash7 \| subject \| branch`. Max 50 lines. |
| `grep` | `file:line:col` pattern | Strips absolute paths. Caps at 50 matches with `[... N more matches ...]` marker. |
| `ls` | `drwxr-xr-x` permissions format | Icon + abbreviated size + name only. Strips owner, group, timestamps. |
| `build` | `error`, `Error`, `warning` keywords | Strips ANSI codes, progress bars, "Compiling X" lines. Keeps errors/warnings. |

---

## Installation

```bash
# Via OpenClaw CLI
openclaw plugins install exec-truncate
openclaw gateway restart

# Or manual — add to openclaw.json
{
  "plugins": {
    "entries": [{ "module": "exec-truncate" }]
  }
}
```

Requires OpenClaw ≥ 2026.4.1.

---

## Configuration

Defaults work out of the box. Override per domain in `openclaw.json`:

```json
{
  "plugins": {
    "entries": [{ "module": "exec-truncate" }]
  },
  "skills": {
    "entries": {
      "exec-truncate": {
        "config": {
          "enabled": true,
          "gitDiff": { "headLines": 80, "tailLines": 20 },
          "gitLog": { "maxLines": 50 },
          "grep": { "maxMatches": 50 },
          "ls": { "maxEntries": 100 },
          "build": { "headLines": 10, "tailLines": 30 }
        }
      }
    }
  }
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `enabled` | `true` | Master kill switch |
| `gitDiff.headLines` | `80` | Addition lines to keep at start |
| `gitDiff.tailLines` | `20` | Addition lines to keep at end |
| `gitLog.maxLines` | `50` | Max commit summary lines |
| `grep.maxMatches` | `50` | Max grep result lines |
| `ls.maxEntries` | `100` | Max directory entry lines |
| `build.headLines` | `10` | Build output lines to keep at start |
| `build.tailLines` | `30` | Build output lines to keep at end |

---

## Behavior

- **Small outputs pass through unchanged.** Anything under 200 characters is returned as-is — no false positives.
- **Detection is output-based**, not command-based. The plugin reads the output content and identifies the domain from patterns — no command metadata parsing required.
- **`MARKER`** — `... [N lines truncated by exec-truncate] ...` — appears whenever lines are omitted, so you always know truncation happened.
- **All domains can be disabled individually** via `domain.enabled: false`.
- **Fail-safe on any error.** If truncation crashes (TypeError, RangeError, bad regex), the original raw output is returned unchanged with a message to stderr.

---

## Example Transformations

### git diff

```
# before (2,847 lines)
+import { defineConfig } from 'vite'
+import { defineConfig } from 'vite'
...
+export default defineConfig({   # +2,840 more addition lines

# after (122 lines)
+import { defineConfig } from 'vite'
+import { defineConfig } from 'vite'
...
[... 2715 lines truncated, 2847 total additions ...]
+export default defineConfig({
```

### git log

```
# before (20 commits, full output)
def5678 Fix login redirect bug
abc1234 Update dependencies
...
ghi9012 Merge branch 'main'

# after (one line per commit, max 50)
def5678 Fix login redirect bug (main)
abc1234 Update dependencies
ghi9012 Merge branch 'main'
```

### grep

```
# before
/home/pi/project/src/utils/auth.ts:45:    // TODO: implement token refresh
/home/pi/project/src/utils/auth.ts:47:    // TODO: add error boundary
/home/pi/project/src/middleware/role.ts:23:    // TODO: check permissions
...

# after
src/utils/auth.ts:45:    // TODO: implement token refresh
src/middleware/role.ts:23:    // TODO: check permissions
[... 48 more matches ...]
```

### build (cargo/npm/go/etc.)

```
# before (500 lines of progress bars + ANSI + warnings + 1 error)

# after
error[E0308]: mismatched types
  --> src/main.rs:23:45
   |
23 |     let x: i32 = "hello";
   |                ^^^^^^^ expected `i32`, found `&str`

warning: unused variable
  --> src/main.rs:10:5
   |
10 |     let y = 42;
   |         ^ help: prefix with underscore: `_y`

[build OK — 1 warning]
```

---

## Architecture

```
tool_result_persist (synchronous hook)
  └── message.content
        ├── string → used directly
        └── array  → text parts joined, filtered to type:"text"
              ├── < 200 chars → returned unchanged
              ├── domain detected? → apply domain truncation
              └── no domain → returned unchanged
```

---

## Testing

```bash
npm install
npm test        # vitest — truncation functions + hook integration
```

---

## Package Contents

```
src/
  index.ts         — Plugin entry point, wires to tool_result_persist hook
  hook-handler.ts  — Parses exec output, routes to truncation functions
  domains/
    gitDiff.ts     — git diff detection + truncation
    gitLog.ts      — git log detection + truncation
    grep.ts        — grep/rg/find detection + truncation
    ls.ts          — ls detection + truncation
    build.ts       — build tool detection + truncation
    shared.ts      — Shared utilities: failSafe, MARKER, constants
dist/              — Compiled output (published to npm)
tests/
  truncation.test.ts      — Unit tests for each truncation function
  hook-integration.test.ts — Integration tests for the hook handler
openclaw.plugin.json      — Plugin manifest + configSchema
SKILL.md                 — AI skill card (used by OpenClaw skill loader)
README.md                — This file
```

---

## Changelog

- **1.0.1** — README significantly expanded with examples, architecture, configuration, and package contents
- **1.0.0** — Initial release. 5 domains: gitDiff, gitLog, grep, ls, build.

---

Built with the [OpenClaw Plugin SDK](https://docs.openclaw.ai/plugins/).
Published to [ClawHub](https://clawhub.ai) and [GitHub](https://github.com/ether-btc/openclaw-exec-truncate).
