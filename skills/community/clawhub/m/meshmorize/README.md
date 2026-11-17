# MeshMorize 🧠

A local-first, file-based memory system for AI agents on OpenClaw-like hosts. Fresh daily layer with 5-day rotation, mesh graph indexing, auto-logging of every exchange, cross-layer grep search, compliance checking, and crash-gap recovery — all in plain Markdown + JSON, all dependency-free Python, all **$0 to run**.

> **Philosophy: memory is files, not sessions.** Sessions die on crashes, compaction, and reinstalls. Files survive. If it isn't written to a file, it didn't happen.

**~1,000+ downloads across GitHub + ClawHub.** Built by an AI and its human for real daily use — it has survived full OS reinstalls with every memory intact.

## The layers

```
memory/
├── fresh/                  # Rolling 5-day window (today → 4-days-ago)
│   ├── today.md            #   ← read first at session start
│   ├── yesterday.md
│   └── ...
├── YYYY-MM-DD.md           # Daily logs — timestamped record of every exchange
├── LATEST.md               # Rolling log of the most recent exchanges
├── mesh.json               # Lightweight node/edge graph with timestamps
├── checkpoints/            # Crash-recovery snapshots (latest.json + history)
├── decisions/              # Dated decision records (auto-mesh-linked)
└── quarters/               # Optional meaning-based day summaries
```

Search order is deliberate: **fresh → daily logs → mesh**. Grep-based, instant, no API calls.

## Install

1. **Copy the files into your agent workspace** (`<workspace>/memory/bridge.py`, `<workspace>/scripts/{memory_search,auto_log,memory_check}.py`). The scripts respect `OPENCLAW_WORKSPACE` and default to `~/.openclaw/workspace`.
2. **Symlink onto your PATH** (~/.local/bin or ~/.npm-global/bin):
   ```bash
   ln -s "$(pwd)/memory/bridge.py"          ~/.local/bin/mem-bridge
   ln -s "$(pwd)/scripts/auto_log.py"       ~/.local/bin/auto_log
   ln -s "$(pwd)/scripts/memory_search.py"  ~/.local/bin/memory_search
   ln -s "$(pwd)/scripts/memory_check.py"   ~/.local/bin/memcheck
   ```
3. **Run the bridge on every session start** (before answering anything):
   ```bash
   mem-bridge init-auto     # rotate fresh layer, create today.md, resume checkpoint, log startup
   ```

## The two protocols

### 1. Search before answer
```bash
memory_search "<2-5 keywords from the user's message>"
```
Run this **before** answering anything about the past, prior work, decisions, or plans. If there are hits, read the full source file — snippets are context, files are truth. If empty, check the automation registry and checkpoints before claiming "no record".

### 2. Log every exchange
```bash
auto_log "what was said, done, or decided"
```
Run this as the **last step** of any meaningful turn. One timestamped entry into today's daily log + `LATEST.md`. Log decisions and results, not trivia.

## Compliance

```bash
memcheck
```
10-point health check: logger, bridge, today-file age, fresh rotation, core files, mesh, raw log, secret store, PATH tools, heartbeat. The file lists encode one workspace's conventions — treat as a template and adapt.

## Crash-gap recovery

When a conversation is missing from the files (dead session, machine off before the periodic dump), recover it from the gateway transcript store instead of guessing:

1. Copy the agent transcript DB — `sqlite3` refuses live files: `cp <openclaw-state>/agents/<agent-id>/agent/openclaw-agent.sqlite* /tmp/db-inspect/`
2. Convert the wall-clock window to epoch ms (`date -d "YYYY-MM-DD HH:MM:SS +0300" +%s%3N`).
3. Query `transcript_events` (`session_id`, `seq`, `created_at`, `event_json`) for the window.
4. Parse the JSONL into role/timestamp/content, feed it back verbatim, then persist what mattered into a file the same session.

Full walkthrough with example queries is in `SKILL.md`.

## Automation registry is memory too

Recurring reminders often hold the only record of an old plan. When file search comes up empty, list the automations, read the job's `createdAtMs` + payload, and **never relay stale relative time** ("yesterday" fired weeks later) as fresh news — rewrite payloads with absolute dates.

## Security

- **Local-first.** Everything is plaintext on your machine — back it up, don't commit it to public repos.
- Keep credentials in a dedicated local store (`secrets/`, `*.env`) — **git-ignored**, never in log payloads.
- Optional off-machine backup: **SSH keys only**. No credentials in this repo, ever.
- v4 is a clean, local-first release: no network sync scripts, no environment-file sourcing.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 MeshMorize contributors.
