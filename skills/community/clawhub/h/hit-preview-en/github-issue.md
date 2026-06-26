# False positive: Skill `hit-preview-en` flagged as "sensitive/high-impact"

**Skill**: [hit-preview-en](https://clawhub.ai/makclaw/hit-preview-en) — Micro-drama hit potential analyzer  
**Author**: @makclaw  
**Version**: 1.0.1 / 1.0.2  
**License**: MIT-0

## Summary

The skill `hit-preview-en` has been flagged by ClawHub Security with the message:

> *"ClawHub Security found sensitive or high-impact capabilities. Review the scan results before using."*

After reviewing the codebase, I believe this is a false positive. The skill performs no sensitive operations — it only reads a local config file and calls a public LLM API. Below is a detailed breakdown.

## Code Review

The skill consists of a single `bundle-en.js` file (~21KB) with the following capabilities:

### What the skill actually does

1. **Reads `~/.openclaw/openclaw.json`** — a user-owned local config file via `fs.readFileSync`. This is equivalent to reading `~/.bashrc` or any other user-level config. No write operations.

2. **Calls external LLM APIs** (DeepSeek / OpenAI / Anthropic / Google) via `fetch()` — standard HTTPS calls to public API endpoints. User provides their own API key via the config file.

3. **Falls back to a local analysis engine** if AI is unavailable — all computation runs locally, no data leaves the machine.

### What the skill does NOT do

- ❌ No `child_process.exec` / `execSync` / `spawn` — no shell command execution
- ❌ No file writes — no modification to user's filesystem
- ❌ No network listeners — no servers, no webhooks
- ❌ No external binary downloads — no npm install, no curl-to-bash
- ❌ No hidden telemetry — no data collection, no analytics
- ❌ No code obfuscation — the bundle is clean, readable JavaScript

### All Node.js modules used

Only three built-in modules, no external dependencies:

```js
const fs = require("fs");         // Read config file
const path = require("path");     // File path resolution
const { performance } = require("perf_hooks");  // Timing
```

That's it. No `net`, `http`, `dgram`, `vm`, `worker_threads`, or any other sensitive modules.

## Why it might have been flagged (guesses)

1. **`require("fs")` + `readFileSync`** — the scanner might flag any skill that reads from `~/.openclaw/`, treating it as "accessing sensitive user data". However, it's merely reading an AI config file the user explicitly created.

2. **`fetch()` to external domains** — the skill makes HTTPS requests to `api.deepseek.com`, `api.openai.com`, etc. This is the core functionality of the skill (AI analysis), not a covert data exfiltration vector.

3. **Prior version had `require("node-fetch")`** — v1.0.0 included a `node-fetch` fallback for older Node.js versions. This has been removed in v1.0.2 since Node >= 18 has native `fetch`.

## Request

Please review the skill manually. If it was flagged by an automated scanner, I'm confident a human review will clear it. If there's a specific code pattern that triggered the flag, I'd appreciate knowing so I can adjust the skill accordingly.

The full source is available at:
- [https://clawhub.ai/makclaw/hit-preview-en](https://clawhub.ai/makclaw/hit-preview-en)

Thank you.
