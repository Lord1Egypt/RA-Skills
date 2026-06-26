# paperclip-resilience — Architecture

This document describes the design of each module, how they compose, and the data flows between them.

---

## Overview

`paperclip-resilience` is a collection of five independent Node.js modules that wrap common failure modes in Paperclip + OpenClaw agent deployments. Each module can be used standalone; the full stack is shown in the diagram below.

```
┌──────────────────────────────────────────────────────────────┐
│                        Caller / Orchestrator                  │
│         (heartbeat handler, cron job, or human CLI)           │
└──────────────┬───────────────────────────────────────────────┘
               │
               │  1. enrich task metadata
               ▼
   ┌───────────────────────┐
   │    Task Injection      │
   │  (src/task-injection)  │◀── Paperclip issue API (optional)
   └───────────┬───────────┘
               │  enriched task string
               │  2. spawn agent with fallback
               ▼
   ┌───────────────────────┐
   │  Spawn with Fallback   │
   │ (src/spawn-with-      │◀── config.json (aliases + fallbacks)
   │   fallback.js)         │
   └───────────┬───────────┘
               │  openclaw session spawn → agent session
               │
               ▼
   ┌───────────────────────┐
   │   Paperclip Agent      │
   │   (heartbeat runs)     │
   └──────────┬────────────┘
              │
   ┌──────────┴──────────┐
   │                      │
   ▼                      ▼
┌──────────────────┐  ┌──────────────────────┐
│  Run Recovery     │  │   Blocker Routing     │
│ (src/run-         │  │  (src/blocker-        │
│  recovery.js)     │  │   routing.js)         │
└────────┬─────────┘  └──────────────────────┘
         │
         ▼
┌──────────────────┐
│  Model Rotation   │
│ (src/model-       │
│  rotation.js)     │
└──────────────────┘
```

---

## Module Reference

### 1. Spawn with Fallback (`src/spawn-with-fallback.js`)

**Purpose:** Wrap `openclaw session spawn` with automatic provider failover on rate-limit or billing errors.

**Inputs:**
- `model` — short alias or full `provider/model` string
- `task` — task string or `@file` path reference
- `mode` — `run` (one-shot) or `session` (persistent)
- `label` — optional session label
- `config` — loaded config object (aliases + fallbacks + failurePatterns)

**Flow:**
1. Resolve model alias → full provider/model string
2. Run `openclaw session spawn` via `execFile`
3. Parse stdout/stderr for failure patterns (e.g., `rate limit`, `402`, `credits_exhausted`)
4. If failure detected and a fallback is configured, retry once with the fallback model
5. Return `{ success, model, fallbackUsed, output }`

**Config keys:** `aliases`, `fallbacks`, `failurePatterns`, `failureStopReasons`

---

### 2. Model Rotation (`src/model-rotation.js`)

**Purpose:** Track attempt counts per PR/task and automatically escalate to stronger models after repeated failures.

**Inputs (CLI):**
- `check` — read the attempt counter and return the recommended model for this PR
- `record` — increment the attempt counter for a PR and record the model used

**State:** Stored in a JSON file at `~/.openclaw/model-rotation-state.json` (path configurable).

**Rotation logic:**
- 0–1 attempts → primary model
- 2–3 attempts → fallback model
- 4+ attempts → escalation model (e.g., `opus`)

**Config keys:** `aliases`, `fallbacks`, rotation thresholds (currently hardcoded, configurable via issue)

---

### 3. Run Recovery (`src/run-recovery.js`)

**Purpose:** Detect failed Paperclip heartbeat runs (gateway crash, provider timeout, unhandled error) and re-invoke the responsible agent.

**Inputs:**
- Paperclip API credentials (from environment)
- `--dry-run` — list recoverable runs without triggering anything
- `--verbose` — emit full run metadata for each candidate

**Flow:**
1. `GET /api/companies/{companyId}/runs?status=failed` via Paperclip API
2. For each failed run, identify the assigned agent
3. If within the retry window and not already retried, POST a wake/re-run event for the agent
4. Record recovery attempts to prevent duplicate retries

**Cron integration:** Run every 15 minutes via system cron or OpenClaw's built-in cron scheduler.

```
*/15 * * * *  node skills/paperclip-resilience/src/run-recovery.js
```

---

### 4. Blocker Routing (`src/blocker-routing.js`)

**Purpose:** Scan agent session transcripts for blocked/stuck signals and route them to a configurable destination.

**Detection heuristics:**
- Keywords: `blocked`, `waiting for`, `cannot proceed`, `need access`, `missing credentials`
- Exit codes from session spawn that indicate non-completion

**Routing destinations (configurable):**
- `file` — append a JSON record to a local file (default: `~/.openclaw/blockers.jsonl`)
- `stdout` — print to stdout for piping / log aggregation
- `webhook` — HTTP POST to a configured URL

**Config keys:** `blocker-routing.destinations`, `blocker-routing.patterns`

---

### 5. Task Injection (`src/task-injection.js`)

**Purpose:** Enrich a raw task string with structured metadata before spawning an agent.

**Injections (configurable):**
- Paperclip issue identifier + title + description (from `/api/issues/{id}`)
- PR metadata (number, title, base branch) for code-review tasks
- UX preflight checklist (from TOOLS.md pattern: user flows, empty/loading/error states, copy clarity, mobile behavior)
- Agent identity header (which agent, run ID, model)

**Output:** A fully-expanded task string passed to `spawn-with-fallback` or used directly.

---

## Configuration (`config.json`)

All five modules read from `config.json` in the skill root. The schema is defined in `config.schema.json`; sensible defaults are in `config.defaults.json`.

```json
{
  "aliases": {
    "sonnet": "anthropic/claude-sonnet-4-6",
    "codex":  "openai-codex/gpt-5.3-codex"
  },
  "fallbacks": {
    "anthropic/claude-sonnet-4-6": "openai-codex/gpt-5.3-codex",
    "openai-codex/gpt-5.3-codex":  "anthropic/claude-sonnet-4-6"
  },
  "failurePatterns": {
    "patterns": ["rate[\\s_-]?limit", "402", "credits", "quota"]
  },
  "failureStopReasons": {
    "reasons": ["error", "credits_exhausted", "quota_exceeded"]
  }
}
```

Generate a config interactively:

```bash
node scripts/setup.js
```

---

## Cron Setup

For automated run recovery, add this to your system crontab or OpenClaw cron:

```bash
# system crontab
*/15 * * * *  node /path/to/skills/paperclip-resilience/src/run-recovery.js

# openclaw cron (run: openclaw cron add ...)
# see SKILL.md §4 for details
```

---

## Security Model

All user-controlled inputs (model names, task file paths, spawn modes, labels) are validated before use. See [SECURITY-AUDIT-REPORT.md](../SECURITY-AUDIT-REPORT.md) for the full audit record.

Key boundaries:
- No shell execution (`execFile` only, no `exec`)
- No dynamic code evaluation
- File paths canonicalized and checked against allowlists
- Credentials read from environment, never embedded

---

## Versioning and Distribution

This skill is published to [ClawHub](https://clawhub.ai) and installable via:

```bash
clawhub install paperclip-resilience
```

Source lives in `/Users/andrew/clawd/skills/paperclip-resilience`.
