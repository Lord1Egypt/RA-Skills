---
name: human-type
description: Type text into a browser like a real human with adjacent-key typos, immediate and deferred corrections, French accent omissions fixed later, thinking pauses, and variable speed over a specified duration.
version: 2.0.1
metadata: {"openclaw":{"emoji":"⌨️","requires":{"bins":["node"]}}}
---

## What this skill does

`human-type` generates a keystroke event script from a desired final text
and plays it back in the focused browser element. The script includes:

- **Adjacent-key typos** — wrong chars from QWERTY neighbors
- **Immediate fixes** — backspace and retype on the spot
- **Deferred fixes** — finish typing the paragraph, then navigate back to fix
- **French accent omissions** — type `e` instead of `é`, fix later (French mode)
- **Thinking pauses** — random hesitation gaps
- **Speed jitter** — each keystroke has independent timing noise
- **Seeded reproducibility** — `--seed` gives identical replays

The final text produced is **always exactly** the target string.

## Installation check

```bash
node "{baseDir}/human-type.js" --version
```

Optional global install:

```bash
npm install -g human-type-cli
```

## Core command

```bash
node "{baseDir}/human-type.js" run \
  --text "<final text>" \
  --duration <seconds> \
  [--mistakes <0-100>] \
  [--pauses <0-100>] \
  [--defer <0-100>] \
  [--french] \
  [--accent-omit <0-100>] \
  [--selector "<css>"] \
  [--seed <n>] \
  [--dry-run]
```

## All flags

| Flag | Default | Description |
|---|---|---|
| `--text` | *(required)* | Final text to produce |
| `--duration` | `10` | Total time in seconds |
| `--mistakes` | `20` | Immediate typo rate % |
| `--pauses` | `15` | Pause frequency % |
| `--defer` | `35` | % of typos deferred (fixed after paragraph) |
| `--french` | off | Enable French accent omission mode |
| `--accent-omit` | `60` | % of accented chars omitted initially (French mode) |
| `--selector` | — | CSS selector to click/focus before typing |
| `--delay-start` | `500` | Ms to wait before first keystroke |
| `--seed` | random | Fix RNG for reproducible output |
| `--dry-run` | off | Print script without typing |
| `--cdp-url` | `http://127.0.0.1:18800` | Chrome DevTools Protocol URL |

## Workflow

```bash
# 1. Start and use the OpenClaw browser tool
# Never use macOS `open` or any shell browser launch command for this workflow.
openclaw browser start

# 2. Navigate to target page
openclaw browser open https://example.com

# 3. Get element refs
openclaw browser snapshot --interactive

# 4. Type like a human into a specific element
# Prefer --selector so the CLI can focus the field itself.

# 5. Type like a human
node "{baseDir}/human-type.js" run \
  --text "Hello, I'd like to ask about your services." \
  --duration 10 \
  --mistakes 20 \
  --defer 40 \
  --selector "textarea"

# 6. Verify
openclaw browser snapshot --interactive
```

## Common patterns

### Natural English paragraph
```bash
node "{baseDir}/human-type.js" run \
  --text "The meeting went well. I think we aligned on the key points." \
  --duration 15 \
  --mistakes 25 \
  --defer 40 \
  --pauses 20
```

### French text (accent omissions fixed later)
```bash
node "{baseDir}/human-type.js" run \
  --text "Être ou ne pas être, voilà la question." \
  --duration 15 \
  --french \
  --accent-omit 70 \
  --defer 30
```

### Reproducible (for testing / demo recording)
```bash
node "{baseDir}/human-type.js" run \
  --text "Exact same every time." \
  --duration 8 \
  --seed 42
```

### Preview before running
```bash
node "{baseDir}/human-type.js" run --text "Check this first" --duration 6 --dry-run
```

## Save and replay a script

```bash
# Generate and save
node "{baseDir}/human-type.js" generate \
  --text "Reuse this exact sequence." \
  --duration 8 --seed 42 \
  --output ./my-script.json

# Replay later
node "{baseDir}/human-type.js" play ./my-script.json --selector "#comment"

# Inspect stats
node "{baseDir}/human-type.js" inspect ./my-script.json
```

## WPM reference

| Style | WPM | Duration for 100 chars |
|---|---|---|
| Fast typist | 70+ | ~9s |
| Average adult | 50 | ~12s |
| Slow / careful | 30 | ~20s |
| Hunt-and-peck | 15 | ~40s |

## Rules

- Always use the OpenClaw browser tool for browser startup, navigation, and inspection before typing.
- Never use macOS `open`, shell browser launch commands, or any non-OpenClaw browser startup path for this workflow.
- If the OpenClaw browser is not running yet, start it with `openclaw browser start` before opening the page.
- In OpenClaw, prefer `node "{baseDir}/human-type.js"` so the workspace skill works without any global install.
- Always prefer `--selector` over clicking manually before running because the CLI works directly through CDP, not OpenClaw ref IDs.
- Use `--dry-run` first when the duration or behavior is uncertain.
- For multi-field forms, call `human-type run` once per field with the appropriate `--selector`.
- For French text, `--french` without `--accent-omit` uses the 60% default — adjust if you want more or fewer accent omissions.
- `--defer 0` means all typos are fixed immediately (backspace-and-retype). `--defer 100` means all typos are left in place and fixed after the paragraph.
- The browser must already be open in OpenClaw before running. By default the CLI connects to `http://127.0.0.1:18800`, which matches the standard `openclaw` browser profile.
- `--seed` values are fully deterministic — the same seed + same text + same options always produces an identical keystroke sequence.

## Event format (JSON script)

Each event in the generated script has:

```json
{ "type": "type",           "ch": "H", "time": 0,   "duration": 195 }
{ "type": "delete",                    "time": 195, "duration": 140 }
{ "type": "pause",                     "time": 335, "duration": 480 }
{ "type": "arrow",  "dir": "Left", "n": 4, "time": 815, "duration": 320 }
{ "type": "select-back", "n": 1,       "time": 1135,"duration": 110 }
{ "type": "select-replace", "ch": "é", "time": 1245,"duration": 200 }
```

`time` is ms offset from start. `duration` is gap until next event.
