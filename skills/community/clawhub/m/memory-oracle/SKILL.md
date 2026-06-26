---
name: memory-oracle
description: >
  Persistent structured memory system for OpenClaw agents with SQLite storage,
  hybrid search (FTS5 + decay scoring), rule-based capture, LLM-powered daily
  reflection, and adaptive weekly trend analysis. Replaces fragile markdown-only
  memory with a three-tier architecture (hot/warm/cold) that survives compaction,
  session restarts, and long-running workflows. Use this skill whenever the agent
  needs to remember facts across sessions, recall relevant context before responding,
  protect critical rules from being lost, or maintain awareness of changing priorities.
  Triggers on: memory, remember, forget, context loss, compaction, "pick up where
  we left off", session continuity, long-term memory, recall, guardrails.
required_env_vars:
  - name: ANTHROPIC_API_KEY
    required: false
    description: >
      Required ONLY for the HEAVY process (consolidate.py, reflect.py).
      The LIGHT process (capture.py, recall.py) works fully without it.
compatibility:
  python: ">=3.8"
  sqlite_fts5: true
---

# Memory Oracle

A structured, self-maintaining memory system for OpenClaw agents.

## Why this exists

OpenClaw's built-in memory is markdown files + LLM discretion. This means:
- The agent decides whether to save (often doesn't)
- The agent decides whether to search (often doesn't)
- Compaction silently destroys chat-only instructions
- MEMORY.md becomes a dumping ground with no cleanup
- No structured search, no decay, no dedup

Memory Oracle fixes all of these with zero external dependencies (Python stdlib + SQLite).

## Architecture

Two processes, mirroring the HEAVY/LIGHT pattern:

### LIGHT process (every turn, zero tokens, zero API calls)

1. **capture.py** — Rule-based extraction runs AFTER each agent response.
   Parses the conversation turn for facts, decisions, preferences, tasks
   using bilingual (RU+EN) pattern matching. Writes to SQLite.
   If a fact's content hash already exists → bumps `access_count` instead.

2. **recall.py** — Three-slot retrieval runs BEFORE each agent response.
   Injects relevant context from SQLite using a budget of ~2000 tokens:
   - Slot 1 (10%): Guardrails — always present, immune to decay
   - Slot 2 (30%): Fresh facts from last 24h by importance
   - Slot 3 (60%): FTS5 search ranked by `score = importance × recency × access_boost`

3. **checkpoint.py** — Emergency save triggered by OpenClaw's pre-compaction hook.
   Dumps all hot-tier context to SQLite with `source = "checkpoint"` tag.

### HEAVY process (cron, uses Claude API)

Runs nightly at 03:00 agent-local time:

1. **consolidate.py** — Sends today's daily log to Claude API (~2K tokens).
   Extracts structured facts that rule-based capture missed.
   
2. **reflect.py** — Analyzes the day's facts against MEMORY.md and prior reflections.
   - Light mode (daily): contradictions, new topics, priorities, stale candidates
   - Deep mode (weekly, Mondays): 7-day trend analysis, pattern detection, strategic rebalancing
   Outputs `reflection.json` with score modifications + `YYYY-MM-DD-reflection.md` digest.

3. **maintenance.py** — Applies decay, prunes dead facts, archives cold tier,
   re-renders MEMORY.md from top SQLite facts, vacuums DB.

## Agent protocol

These rules go into your AGENTS.md or equivalent config:

```
## Memory Oracle Protocol

BEFORE responding to the user:
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/recall.py --query "<user message>"
  Inject the output into your context as relevant background.

AFTER responding to the user:
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/capture.py --turn "<full turn text>"

When the user says "remember this", "never forget", "this is critical":
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/capture.py --turn "<text>" --guardrail

When the user asks "what do you know about X":
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/recall.py --query "X" --verbose
  Show the facts with their scores, sources, and ages.

Every 10 turns (heartbeat):
  Run: python3 ~/.openclaw/skills/memory-oracle/scripts/capture.py --flush
  This forces extraction of any buffered context.
```

## Installation

```bash
cd ~/.openclaw/skills/
git clone <repo-url> memory-oracle
cd memory-oracle
bash install.sh
```

The installer will:
1. Initialize SQLite database with FTS5 index
2. Import existing MEMORY.md and daily logs (if present)
3. Prompt you to optionally set up cron jobs for the HEAVY process
4. Print a snippet to paste into your AGENTS.md
5. Print a snippet to paste into your OpenClaw compaction config

**Note:** The installer does NOT auto-edit your AGENTS.md or OpenClaw config.
You review and paste the snippets yourself.

## Configuration

All thresholds live in `config/settings.json`. Key tunables:

- `recall_budget_tokens`: Total injection budget (default: 2000)
- `decay_rate`: Daily score decay multiplier (default: 0.05)
- `archive_threshold`: Score below which facts move to cold (default: 0.2)
- `delete_threshold`: Score below which cold facts are purged (default: 0.05)
- `delete_min_age_days`: Minimum age before deletion (default: 90)
- `reflect_deep_day`: Day of week for deep reflection, 0=Mon (default: 0)
- `api_model`: Model for HEAVY process (default: claude-sonnet-4-20250514)
- `api_max_tokens`: Max response tokens for LLM calls (default: 1000)

## Uninstall / rollback

```bash
cd ~/.openclaw/skills/memory-oracle
bash uninstall.sh
```

The uninstaller will:
1. Export full memory state to JSON (for re-import if you reinstall)
2. Remove cron jobs (with confirmation)
3. Restore original MEMORY.md from the backup created during install
4. Optionally delete the SQLite database (asks with fact count shown)
5. Clean up reflection files and pending queue
6. Print remaining manual steps (AGENTS.md cleanup, compaction config)

Use `--force` to skip confirmations, `--keep-db` to keep the database while removing everything else.

## Known issues & limitations

**FTS5 not available on some systems.**
Minimal containers (Alpine) and old Debian/Ubuntu may lack FTS5. install.sh checks
for this and prints fix instructions. Most systems with Python 3.8+ include FTS5.

**Conflict with other memory skills.**
If you have memory-complete, continuity, or agent-brain installed, they may
compete for MEMORY.md writes. Disable other memory plugins before installing:
`plugins.slots.memory = "none"` in your OpenClaw config, or remove conflicting skills.

**Cron unavailable in containers.**
Docker, sandboxed VPS, and some hosting environments block crontab.
install.sh handles this gracefully — just run the HEAVY pipeline manually or
via your own scheduler (systemd timer, supervisor, etc.):
```bash
python3 scripts/consolidate.py && python3 scripts/reflect.py --auto && python3 scripts/maintenance.py
```

**Large existing MEMORY.md (>50KB).**
Import during init_db.py works but may create noisy low-confidence facts.
After install, run `python3 scripts/maintenance.py --stats` and check the
fact count. If too high, run `python3 scripts/maintenance.py` to let decay
and pruning clean up naturally over a few days.

**Rule-based capture misses implicit facts.**
Capture.py uses pattern matching — it catches ~70% of facts. The remaining 30%
are caught by consolidate.py (HEAVY process) with LLM extraction. Without
ANTHROPIC_API_KEY, only rule-based capture works.

## File structure

```
memory-oracle/
├── SKILL.md              ← You are here
├── README.md             ← GitHub-friendly docs
├── LICENSE               ← MIT
├── install.sh            ← Bootstrap + cron setup
├── uninstall.sh          ← Safe rollback + export
├── scripts/
│   ├── init_db.py        ← Schema + migration from existing .md
│   ├── capture.py        ← LIGHT: rule-based extraction
│   ├── recall.py         ← LIGHT: 3-slot hybrid search
│   ├── checkpoint.py     ← Pre-compaction emergency save
│   ├── consolidate.py    ← HEAVY: LLM fact extraction
│   ├── reflect.py        ← HEAVY: adaptive reflection
│   ├── maintenance.py    ← HEAVY: decay, prune, re-render
│   └── migrate.py        ← Schema version management
├── config/
│   ├── settings.json     ← All tunables
│   └── patterns.json     ← Bilingual extraction rules
├── prompts/
│   ├── consolidate.txt   ← LLM extraction prompt
│   ├── reflect_light.txt ← Daily reflection prompt
│   └── reflect_deep.txt  ← Weekly reflection prompt
└── tests/
    ├── test_capture.py   ← Pattern matching tests
    └── test_recall.py    ← Ranking + budget tests
```

## Graceful degradation

Every component is designed to fail safely:
- SQLite corrupted → recall falls back to grep over MEMORY.md
- API unreachable → consolidate/reflect queue to `pending_queue.json`, LIGHT continues
- Cron missed → next run processes all accumulated data
- Bad LLM output → stored in `failed_reflections/`, scores unchanged
- Low confidence reflection → stored but not applied, re-evaluated next cycle

## Privacy & data flow

**What stays local (always):**
- SQLite database with all facts, scores, and access logs
- MEMORY.md, daily logs, SESSION-STATE.md
- Rule-based capture and recall (LIGHT process) — zero network calls

**What is sent to Anthropic API (HEAVY process only):**
- `consolidate.py` sends the text of today's daily log to Claude API for fact extraction
- `reflect.py` sends extracted facts (not raw logs) and current memory state for analysis
- Both require `ANTHROPIC_API_KEY` env var to be set
- If the API key is not set, HEAVY process is skipped entirely — LIGHT works alone

**If you are not comfortable sending daily logs to an external LLM:**
- Set `api.model` to a local model endpoint in `config/settings.json`
- Or simply don't set `ANTHROPIC_API_KEY` — the skill runs in LIGHT-only mode
  with rule-based capture and full recall, just without LLM-powered consolidation
  and reflection

**Other privacy rules:**
- MEMORY.md and recall output are NEVER loaded in group contexts
- Guardrails table is private-session only
- `maintenance.py --export` dumps full state to JSON for backup/migration

## Author

* 🐙 [github.com/Oleglegegg](https://github.com/Oleglegegg)
* 💬 Telegram: [@oleglegegg](https://t.me/oleglegegg)
* 🪙 Tip (USDT TRC-20): `TMkk6SHacogyEtSepLPzh8qU12iPTsG8Y3`
