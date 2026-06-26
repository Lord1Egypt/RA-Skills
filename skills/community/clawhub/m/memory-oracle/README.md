# Memory Oracle

**Structured, self-maintaining memory for OpenClaw agents.**

A drop-in skill that replaces OpenClaw's fragile markdown-only memory with a three-tier SQLite-backed system featuring hybrid search, decay scoring, LLM-powered reflection, and zero external dependencies.

## The problem

OpenClaw's built-in memory relies on the LLM to decide when to save and when to recall. It usually doesn't do either. Compaction silently destroys chat-only instructions. MEMORY.md becomes a dumping ground that never gets cleaned up. Existing solutions (Mem0, Supermemory) fix this but require external APIs and subscriptions.

## The solution

Memory Oracle runs two processes:

| | LIGHT (every turn) | HEAVY (nightly cron) |
|---|---|---|
| **Tokens** | Zero | ~3 API calls (~$0.02/day) |
| **Does** | Rule-based capture, 3-slot recall | LLM extraction, adaptive reflection, maintenance |
| **Fails gracefully** | Always works | Queues on failure, LIGHT continues alone |

### Three-slot recall budget

Every turn, ~2000 tokens of context are injected:
- **10% Guardrails** — critical rules, always present, immune to decay
- **30% Fresh** — last 24h facts by importance
- **60% Relevant** — FTS5 search ranked by `importance × recency × access_boost`

### Adaptive reflection

Daily light reflection spots contradictions, new topics, patterns, and stale facts. Weekly deep reflection (Mondays) analyzes 7-day trends, merges duplicates, promotes frequently-used facts to guardrails, and generates a strategic summary.

### Nine failure modes hardened

| Failure | Mitigation |
|---|---|
| Race condition (cron vs agent) | WAL mode + busy timeout |
| Critical rules lost (Summer Yue) | Guardrails table, immune to decay |
| Old facts crowd out fresh | Slotted budget with reserved fresh slot |
| API/cron failure | Pending queue, LIGHT works alone |
| Duplicate facts | SHA-256 content-addressed dedup |
| Bad LLM reflection | Confidence gate (skip apply if < 0.5) |
| Cold start / migration | Bootstrap import from existing .md files |
| No audit trail | Provenance tracking (session + turn per fact) |
| RU + EN mixed content | Bilingual pattern matching, UTF-8 safe |

## Installation

```bash
cd ~/.openclaw/skills/
git clone https://github.com/Oleglegegg/memory-oracle.git
cd memory-oracle
bash install.sh
```

The installer will:
1. Check Python 3.8+ and SQLite FTS5 availability
2. Initialize the database and import existing MEMORY.md / daily logs
3. Ask whether to install a nightly cron job (you confirm explicitly)
4. Print snippets for AGENTS.md and compaction config — **you paste them manually**

Requirements: Python 3.8+ with SQLite FTS5 support (standard on most systems). No pip dependencies.

**Environment variables:**

| Variable | Required | Used by |
|---|---|---|
| `ANTHROPIC_API_KEY` | Only for HEAVY process | consolidate.py, reflect.py |

Without the API key, the skill runs in LIGHT-only mode (rule-based capture + full recall). LLM consolidation and reflection are skipped.

## Privacy & data flow

**Local only (LIGHT process):** capture.py, recall.py, checkpoint.py — zero network calls, all data stays on disk.

**Sent to Anthropic API (HEAVY process):** consolidate.py sends daily log text for fact extraction; reflect.py sends extracted facts and memory state for analysis. Both require `ANTHROPIC_API_KEY`. If the key is not set, HEAVY is skipped entirely.

**If you prefer no external calls:** don't set the API key, or point `api.base_url` in settings.json to a local model endpoint. The skill works fully in LIGHT-only mode.

## Configuration

All thresholds in `config/settings.json`. Key tunables:

```json
{
  "recall.budget_tokens": 2000,
  "scoring.decay_rate_per_day": 0.05,
  "scoring.archive_threshold": 0.2,
  "reflection.deep_day_of_week": 0,
  "api.model": "claude-sonnet-4-20250514"
}
```

## Usage

The installer prints an `AGENTS.md` snippet. Core protocol:

```
BEFORE responding → recall.py --query "<message>"
AFTER responding  → capture.py --turn "<turn text>"
Every 10 turns    → capture.py --flush
User says "remember this" → capture.py --turn "<text>" --guardrail
```

Manual commands:

```bash
# Check memory stats
python3 scripts/maintenance.py --stats

# Export full state for backup
python3 scripts/maintenance.py --export backup.json

# Run reflection manually
python3 scripts/reflect.py --deep

# Search memory
python3 scripts/recall.py --query "crypto trading" --verbose
```

## Uninstall

```bash
cd ~/.openclaw/skills/memory-oracle
bash uninstall.sh
```

Exports your memory to JSON, removes cron, restores MEMORY.md from the backup
created during install, and optionally deletes the database. All steps ask
for confirmation unless `--force` is passed.

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │     LIGHT (every turn, 0 tokens)    │
                    │                                     │
                    │  capture.py ──→ SQLite + FTS5       │
                    │  recall.py  ←── 3-slot budget       │
                    │  checkpoint.py (pre-compaction)      │
                    └──────────────┬──────────────────────┘
                                   │ reads/writes
                    ┌──────────────▼──────────────────────┐
                    │     HEAVY (nightly cron, ~$0.02)    │
                    │                                     │
                    │  consolidate.py → LLM extraction    │
                    │  reflect.py     → adaptive analysis │
                    │  maintenance.py → decay + cleanup   │
                    └──────────────┬──────────────────────┘
                                   │ renders
                    ┌──────────────▼──────────────────────┐
                    │     OUTPUT (what OpenClaw reads)     │
                    │                                     │
                    │  MEMORY.md  │ daily logs │ context   │
                    └─────────────────────────────────────┘
```

## Tests

```bash
python3 tests/test_capture.py -v   # 18 bilingual pattern tests
python3 tests/test_recall.py       # 7 ranking + budget tests
```

## License

MIT

## Credits

Built on top of OpenClaw's file-first memory philosophy, incorporating lessons from memory-complete, memory-maintenance, agent-brain, Mem0, and Supermemory — without their external dependencies.

## Author

* 🐙 [github.com/Oleglegegg](https://github.com/Oleglegegg)
* 💬 Telegram: [@oleglegegg](https://t.me/oleglegegg)
* 🪙 Tip (USDT TRC-20): `TMkk6SHacogyEtSepLPzh8qU12iPTsG8Y3`
