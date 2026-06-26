---
name: paperclip-resilience
description: >
  Production resilience patterns for Paperclip AI agent orchestration.
  Spawn-with-fallback, model rotation, run recovery, blocker routing, and task injection
  — configurable, composable, and ready for any OpenClaw + Paperclip deployment.
metadata:
  openclaw:
    emoji: "🛡️"
---

# paperclip-resilience

Production-grade resilience for AI agents running on [Paperclip](https://github.com/paperclipai/paperclip), orchestrated through [OpenClaw](https://github.com/openclaw/openclaw).

## The Problem

Paperclip agents die silently when providers hit rate limits, sessions crash on gateway restarts, and failed runs leave agents stuck in `error` state with no recovery path. If you're running agents overnight or in parallel, you need automated recovery — not manual babysitting.

## What's Included

| Module | File | Purpose |
|--------|------|---------|
| **Spawn with Fallback** | `src/spawn-with-fallback.js` | Wraps `openclaw session spawn` with automatic provider failover. If your primary model 429s, it tries the configured fallback. |
| **Model Rotation** | `src/model-rotation.js` | Tracks fix attempts per PR/task and rotates through models + thinking levels after repeated failures. |
| **Run Recovery** | `src/run-recovery.js` | Detects failed Paperclip heartbeat runs (gateway errors, timeouts, 429s) and re-invokes agents with model fallback. |
| **Blocker Routing** | `src/blocker-routing.js` | Scans agent session transcripts for blocked/stuck signals and routes them to configurable destinations (file, stdout, webhook). |
| **Task Injection** | `src/task-injection.js` | Enriches spawn task descriptions with issue tracking metadata, PR requirements, and UX design checklists before agent execution. |

## Quick Start

### 1. Install

```bash
clawhub install paperclip-resilience
```

### 2. Configure

```bash
cd skills/paperclip-resilience
cp config.example.json config.json
# Edit config.json with your model aliases and fallback pairs
```

### 3. Use Spawn with Fallback

```bash
# CLI
node skills/paperclip-resilience/src/spawn-with-fallback.js \
  --model sonnet --task "Fix the login bug" --mode run

# Dry run to see what would happen
node skills/paperclip-resilience/src/spawn-with-fallback.js \
  --model opus --task "Refactor auth" --dry-run
```

```javascript
// Programmatic
const { spawnWithFallback, loadConfig } = require('./skills/paperclip-resilience/src/spawn-with-fallback');
const config = loadConfig('./my-config.json');
const result = await spawnWithFallback({ model: 'sonnet', task: 'Fix bug', config });
```

### 4. Set Up Run Recovery (Cron)

Add to your OpenClaw cron schedule to auto-recover failed runs:

```bash
node skills/paperclip-resilience/src/run-recovery.js --dry-run --verbose
```

Once verified, schedule it:
```
*/15 * * * *  node skills/paperclip-resilience/src/run-recovery.js
```

### 5. Model Rotation for PR Fixes

```bash
# Check if a PR needs model rotation
node skills/paperclip-resilience/src/model-rotation.js check --pr 42 --repo owner/repo

# Record an attempt
node skills/paperclip-resilience/src/model-rotation.js record --pr 42 --repo owner/repo --model anthropic/claude-sonnet-4-6
```

## Configuration

All modules read from `config.json` in the skill directory, with sensible defaults if no config is provided.

See `config.example.json` for the full documented schema, and `config.schema.json` for validation.

### Key Configuration Sections

**aliases** — Map short model names to full provider/model strings:
```json
{
  "aliases": {
    "sonnet": "anthropic/claude-sonnet-4-6",
    "opus": "anthropic/claude-opus-4-6",
    "codex": "openai-codex/gpt-5.3-codex"
  }
}
```

**fallbacks** — Define provider failover pairs:
```json
{
  "fallbacks": {
    "anthropic/claude-sonnet-4-6": "openai-codex/gpt-5.3-codex",
    "openai-codex/gpt-5.3-codex": "anthropic/claude-sonnet-4-6"
  }
}
```

**failurePatterns** — Regex patterns that trigger fallback:
```json
{
  "failurePatterns": {
    "patterns": ["credits", "quota", "402", "rate[\\s_-]?limit"]
  }
}
```

## Architecture

```
┌──────────────────┐     ┌──────────────────┐
│  Task Injection   │────▶│ Spawn w/ Fallback │
│  (enrich task)    │     │  (provider retry)  │
└──────────────────┘     └────────┬───────────┘
                                  │
                                  ▼
                    ┌──────────────────────┐
                    │   Paperclip Agent     │
                    │   (heartbeat runs)    │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │                       │
                    ▼                       ▼
          ┌────────────────┐    ┌──────────────────┐
          │ Run Recovery    │    │ Blocker Routing   │
          │ (detect + wake) │    │ (escalate stuck)  │
          └────────────────┘    └──────────────────┘
                    │
                    ▼
          ┌────────────────┐
          │ Model Rotation  │
          │ (escalate model)│
          └────────────────┘
```

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) (for session spawning and agent management)
- [Paperclip](https://github.com/paperclipai/paperclip) (for heartbeat run monitoring and agent lifecycle)
- Node.js 18+
- At least two LLM provider API keys configured (for fallback to work)

## Security

This skill was security-reviewed for ClawHub publication in **SUP-453**. The code paths that accept user-controlled input now enforce validation up front and fail closed.

### Hardened Surfaces

| Surface | Protection |
|---|---|
| **Model names** | Character allowlist with support for provider suffixes like `:free`; rejects empty path segments and `.` / `..` traversal segments |
| **Task files (`@file`)** | Blocks explicit `../`, canonicalizes symlinks with `realpath`, rejects system paths like `/etc/` and `/usr/`, requires a regular file |
| **Task payloads** | 1MB max size limit for inline and file-backed task content |
| **Spawn mode + labels** | Allowlist validation for mode (`run`, `session`) and safe-character validation for labels |
| **Failure regex config** | Caps pattern count/length and drops invalid regexes to reduce ReDoS risk |
| **Paperclip issue metadata** | Sanitizes API strings, constrains issue identifier extraction, normalizes priority values |

### Security Boundaries

- **Process execution**: uses `execFile`, not shell execution
- **Dynamic code execution**: none (`eval` / `Function` not used)
- **Credentials**: read from environment or external auth files; not embedded in the skill
- **File access**: limited to explicitly requested files, with traversal and symlink tunnel protections
- **Dependencies**: zero external runtime dependencies in this package

### Verification

```bash
# Functional coverage
node skills/paperclip-resilience/tests/test-spawn-with-fallback.js

# Full security suite
node skills/paperclip-resilience/tests/test-security.js

# Quick smoke test
node skills/paperclip-resilience/tests/test-security-quick.js
```

### Audit Record

- **Last audit**: 2026-03-27
- **Tracking issue**: SUP-453
- **Status**: ✅ Approved for ClawHub publication
- **Details**: see [SECURITY-AUDIT-REPORT.md](./SECURITY-AUDIT-REPORT.md)

## Related Paperclip Issues

These are the upstream gaps this skill works around:
- [#276](https://github.com/paperclipai/paperclip/issues/276) — Auto-requeue agent on failure
- [#1845](https://github.com/paperclipai/paperclip/issues/1845) — No crash-recovery wakeup after restart
- [#1861](https://github.com/paperclipai/paperclip/issues/1861) — Agent death on 429 with no model fallback

## License

MIT
