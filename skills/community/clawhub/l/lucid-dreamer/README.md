# Lucid 🧠

> *Your AI sleeps. Lucid dreams.*

Lucid keeps your AI's memory clean. Every night, it reads what happened, checks what your AI already knows, and tells you what's outdated, missing, or forgotten.

No database. No embeddings. No dependencies. Just a prompt, a cron job, and markdown files.

## The Problem

AI agents forget. Between sessions, context is lost. `MEMORY.md` gets stale. Todos slip through the cracks. Nobody notices until it's too late.

Lucid fixes this automatically. While you sleep, it:

- 🔍 Finds facts worth remembering that aren't saved yet
- ⏳ Spots todos and decisions that were never resolved
- 🚧 Flags problems that keep coming back
- 🔄 Tracks when your opinions or plans changed
- 🗑️ Catches outdated entries in your memory files
- 📈 Detects recurring issues, stale projects, and repeated mistakes over 14 days
- 🧹 Optionally removes resolved items automatically (v0.6.0+)

You wake up to a short report. Approve what's useful, reject what's not. Done.

## How It Works

```
Daily Notes (7 days)     MEMORY.md + USER.md
         \                    /
          \                  /
       ┌──────────────────────┐
       │   Nightly LLM Review │  ← runs at 3 AM
       └──────────────────────┘
                  │
          ┌───────┴───────┐
          │               │
    review file        state.json
   (for you to read)   (tracks suggestions)
          │
          ▼
    you approve/reject
          │
          ▼
    memory updated ✅
```

**Cost:** One LLM call per night (~$0.20 with Sonnet, less with Haiku).

## Quick Start

### With OpenClaw

```bash
mkdir -p memory/review

openclaw cron add \
  --name "lucid" \
  --cron "0 3 * * *" \
  --tz "Your/Timezone" \
  --model "anthropic/claude-sonnet-4-6" \
  --announce \
  --session isolated \
  --timeout-seconds 120 \
  --message "$(cat prompts/nightly-review.md)"
```

Check results in the morning:
```bash
cat memory/review/YYYY-MM-DD.md
```

Tell your agent what to accept or reject. It handles the rest.

### Optional: Pre-flight Flush (Recommended)

Add a cron at 02:45 Vienna time using `prompts/pre-flight-flush.md` as the message. This ensures your daily memory file is up-to-date before Lucid runs at 03:00, even if you forgot to manually flush your session.

Cron schedule: `45 2 * * *` tz: Europe/Vienna

### Optional: Session Debrief at ~18:00

Session debrief is a quick daily capture pass that runs before the full nightly review. It is meant for a fast end-of-day sweep: read today's daily note, pull out key decisions and durable facts, and write them directly into memory without generating a review report.

Recommended OpenClaw cron:

```bash
openclaw cron add \
  --name "lucid-debrief" \
  --cron "0 18 * * *" \
  --tz "Europe/Vienna" \
  --model "your-preferred-model" \  # e.g. anthropic/claude-haiku-4-5 or opencode-go/minimax-m2.7
  --session isolated \
  --wake-mode now \
  --message "$(cat prompts/session-debrief.md)"
```

Why use it:
- Faster and cheaper than the nightly review
- Reads today's daily note only
- Writes key decisions/facts directly to memory
- Keeps memory fresher before the 03:00 full review

### Without OpenClaw

Lucid is just a prompt. Copy `prompts/nightly-review.md`, give it to any LLM that can read and write files, and run it on a schedule.

## What You Need

```
your-workspace/
├── MEMORY.md              # Your AI's long-term memory
├── USER.md                # User profile (optional but helpful)
└── memory/
    ├── 2026-03-15.md      # Daily notes (Lucid reads last 7 days)
    ├── 2026-03-16.md
    └── review/            # Lucid writes here
        ├── 2026-03-17.md  # The review
        ├── state.json     # Suggestion tracker
        └── .last-success  # Health check timestamp
```

No vector database, no embeddings, no SQLite, no external APIs, no runtime dependencies.

## Features

### Suggestion Tracking

Every suggestion gets tracked in `state.json`:

- **pending** → Waiting for your review
- **accepted** → Applied to memory
- **rejected** → Won't come back
- **deferred** → Come back in 14 days

### Auto-Apply (opt-in)

Automatically apply high-confidence changes without review. Enable in `config/lucid.config.json`:

```json
"autoApply": { "enabled": true }
```

Configure categories in `config/auto-apply.md`:
- Version numbers, new project entries, infrastructure facts, lessons learned, closed open loops, stale project status, factual contradictions

Never auto-applied (hardcoded): belief updates, key decisions, family/personal facts, anything medium/low confidence.

All auto-applied changes are git-committed with a `dreamer: auto-apply —` prefix. Undo with `git revert`.

### Aggressive Cleanup (v0.6.0, opt-in)

Go beyond flagging — actually **remove** resolved entries from memory. Enable in `config/lucid.config.json`:

```json
"aggressiveCleanup": { "enabled": true }
```

Removes resolved Open Loops, closed Blockers, and confirmed-stale entries — but only with **high confidence** and explicit closure evidence from the last 7 days.

Each removal is a **separate git commit** listed in the review under `## 🗑️ Removed (Auto-Cleanup)` with the commit hash. Undo: `git revert <hash>`.

### Trend Detection (v0.5.0)

Analyzes patterns across the last 14 days:

- **🔁 Recurring Issues** — same problem on 3+ days
- **🕸️ Stale Projects** — in MEMORY.md but not mentioned for 30+ days
- **⚠️ Escalated Patterns** — same mistake in 3+ daily notes

Standalone usage:
```bash
python3 scripts/trend_detection.py \
  --workspace /path/to/workspace \
  --days 14 \
  --stale-days 30 \
  --state memory/review/state.json
```

## Safety

- Only suggests new facts if mentioned on **2+ separate days**
- Only flags stale entries with **clear** evidence
- Never suggests passwords, API keys, tokens, or temp debug info
- Auto-apply/cleanup only on **high confidence**
- Every change is git-committed and revertable
- ⚠️ Don't run on workspaces with unencrypted secrets in markdown files

## Inspiration

- [Honcho.dev](https://honcho.dev) — Background "dreaming" over conversations
- [Gigabrain](https://github.com/legendaryvibecoder/gigabrain) — World model with beliefs and suggestion ledger
- [Nuggets](https://github.com/NeoVertex1/nuggets) — Fact promotion to permanent memory

## Roadmap

- [x] Nightly review, state ledger, human approval
- [x] Automatic delivery via announce
- [x] Auto-apply with configurable categories (git-backed)
- [x] Trend Detection (recurring issues, stale projects, escalated patterns)
- [x] Aggressive Cleanup (opt-in, git-backed rollback)
- [ ] Sectioned memory (`memory/sections/*.md` with selective loading)
- [x] Session debrief (lightweight end-of-day capture)
- [x] Contradiction detection (memory vs daily notes)
- [ ] Embedding-based dedup
- [ ] Weekly consolidation

## License

MIT
