---
name: "MeshMorize"
description: "Memory system for AI agents on OpenClaw-like hosts. File-based multi-layer memory: fresh daily layer (5-day rotation), mesh graph, auto-log of every exchange, cross-layer grep search, compliance check, crash-gap recovery from session transcripts, automation-registry lookup. Search before answering, log after answering. Local-first, $0 to run, survives restarts."
---

# MeshMorize 🧠

A local-first, file-based memory system for AI agents running on OpenClaw-like hosts. All state lives in plain Markdown + JSON on disk — no database server, no cloud dependency, no API cost. The bundled scripts are small, dependency-free Python (standard library + grep only).

**Core philosophy: memory is files, not sessions.** Sessions are ephemeral — they die on crashes, compaction, restarts, and reinstalls. Files survive all of those. If something isn't written to a file, it effectively didn't happen. This skill exists to make writing and finding those files automatic.

## What any agent gets

| Layer | Location | Purpose |
|-------|----------|---------|
| **Fresh** | `memory/fresh/today.md` … `4-days-ago.md` | Rolling 5-day window of recent context; read first at session start |
| **Daily log** | `memory/YYYY-MM-DD.md` | Timestamped record of every logged exchange, one file per day |
| **Mesh graph** | `memory/mesh.json` | Lightweight node/edge index with timestamps for long-lived topics |
| **Rolling log** | `memory/LATEST.md` | The most recent exchanges in one place |
| **Checkpoints** | `memory/checkpoints/` | Crash-recovery snapshots (`latest.json` + timestamped history) |
| **Decisions** | `memory/decisions/` | Dated decision records with mesh nodes |
| **Quarters** | `memory/quarters/` | Optional meaning-based day summaries (4 per day) |

## Tools

| Command | Source | What it does |
|---------|--------|--------------|
| `mem-bridge` | `memory/bridge.py` | Fresh-layer rotation, today-file creation, checkpoints, decision capture, mesh timestamps, session wrap |
| `auto_log` | `scripts/auto_log.py` | Append one timestamped entry to today's daily log + `LATEST.md` |
| `memory_search` | `scripts/memory_search.py` | Cross-layer search: fresh → daily logs → mesh (grep-based, $0) |
| `memcheck` | `scripts/memory_check.py` | 10-point compliance check of the whole memory chain |

## Install (any OpenClaw-like workspace)

The scripts respect the `OPENCLAW_WORKSPACE` environment variable and default to `~/.openclaw/workspace` (or your host's agent home). `memory/` and `scripts/` are relative to that workspace root.

1. **Place the files** (this repo is a skill bundle — copy, don't run in place):
   - `memory/bridge.py` → `<workspace>/memory/bridge.py`
   - `scripts/memory_search.py`, `scripts/auto_log.py`, `scripts/memory_check.py` → `<workspace>/scripts/`
2. **Make them callable** — symlink into a directory already on `PATH` (e.g. `~/.local/bin` or `~/.npm-global/bin`):
   ```bash
   ln -s "$(pwd)/memory/bridge.py"          ~/.local/bin/mem-bridge
   ln -s "$(pwd)/scripts/auto_log.py"       ~/.local/bin/auto_log
   ln -s "$(pwd)/scripts/memory_search.py"  ~/.local/bin/memory_search
   ln -s "$(pwd)/scripts/memory_check.py"   ~/.local/bin/memcheck
   ```
3. **Run the bridge on every session start** (before answering anything):
   ```bash
   mem-bridge init-auto
   ```
   This rotates the fresh layer, creates `memory/fresh/today.md`, resumes the latest checkpoint, and logs the startup.

## Protocol 1 — SEARCH BEFORE ANSWER

Before answering any question about the past, prior work, people, decisions, or plans:

1. **Search first** — extract the 2–5 most specific keywords from the user's message and run:
   ```bash
   memory_search "<keywords>"
   ```
   Cost: $0 (pure grep, no API calls). It searches the fresh layer first, then the TDAI/legacy archive if present, then every dated daily log, then mesh nodes.
2. **If there are hits, read the full source file.** Snippets are context; the files are truth. A search hit line tells you *where* the answer is — go open that file and read the surrounding entry.
3. **If search returns nothing**, do not answer "no record" yet. Check the remaining places memory can live: the automation/reminder registry (see below), `memory/checkpoints/`, and mesh nodes by related keyword.

## Protocol 2 — LOG EVERY EXCHANGE

After any turn that contained something worth remembering — decisions, results, plans, corrections, context, or user preferences:

```bash
auto_log "what was said, done, or decided"
```

This appends one timestamped entry to today's daily log (`memory/YYYY-MM-DD.md`) and to the rolling `LATEST.md`. It is the **last step** of the turn, so the log always reflects the final state. Do not log trivia; do log anything future-you would need to reconstruct the conversation.

## Fresh-layer rotation

`bridge.py` keeps a 5-day fresh window. Each startup, `init-auto` (or `init`) checks whether `memory/fresh/today.md` already contains today's date string; if the file is stale, it rotates: `4-days-ago ← 3-days-ago ← … ← yesterday ← today`, then creates a fresh template for today. Rotation is idempotent — running it twice on the same day changes nothing.

Other bridge commands: `mem-bridge log <msg>`, `mem-bridge decision <topic> <body>`, `mem-bridge quarter <1-4> <summary>`, `mem-bridge checkpoint <context> [node]`, `mem-bridge resume`, `mem-bridge touch <node_id>`, `mem-bridge wrap`, `mem-bridge mesh [N]`, `mem-bridge summarize`, `mem-bridge daily`.

## memcheck — compliance in one command

When memory health is in doubt (missing files, rotation broken, tools lost from PATH), run:

```bash
memcheck
```

It runs 10 checks: auto_log writes, bridge init, today.md presence/age, the 5 fresh files, core agent files, mesh.json, the raw log, the local secret store, tools on PATH, and the heartbeat file — then prints a pass/warn/fail summary. The core-file and directory lists encode one workspace's conventions: treat it as a template and adjust the lists to your own layout if your agent home differs.

## Crash-gap recovery (conversation lost to a dead session)

When a conversation is missing from the file layers (an LLM crash ate the turn, or the machine powered off before the periodic dump), recover it from the gateway's transcript store — never rebuild from guesses.

1. **Identify the session** that was live at the time. Session listings show a `sessionId` per `sessionKey` (for the main chat this is your agent's main session key).
2. **Copy the database first** — `sqlite3` refuses to open the live DB while the gateway holds it:
   ```bash
   mkdir -p /tmp/db-inspect
   cp <openclaw-state>/agents/<agent-id>/agent/openclaw-agent.sqlite* /tmp/db-inspect/
   ```
   The exact path depends on the OpenClaw version and agent layout — look under your host's OpenClaw state directory (commonly `~/.openclaw/`), find the agent's `agent/` folder, and copy every `*.sqlite*` file. The schema is `transcript_events` with `session_id`, `seq`, `created_at`, and an `event_json` payload column.
3. **Convert the wall-clock window to epoch milliseconds** (use the host's timezone; `+0300` in this example):
   ```bash
   date -d "YYYY-MM-DD HH:MM:SS +0300" +%s%3N   # repeat for start and end
   ```
4. **Locate the user messages in the window** (`event_json` holds `{"message":{"role":"user","content":...}}`):
   ```bash
   sqlite3 /tmp/db-inspect/openclaw-agent.sqlite \
     "SELECT seq, created_at, substr(event_json,1,400) FROM transcript_events \
      WHERE session_id='<session-id>' AND created_at BETWEEN <t0> AND <t1> \
        AND event_json LIKE '%\"role\":\"user\"%' ORDER BY seq;"
   ```
5. **Dump the full window and parse it** into readable dialogue:
   ```bash
   sqlite3 /tmp/db-inspect/openclaw-agent.sqlite \
     "SELECT event_json FROM transcript_events WHERE session_id='<session-id>' \
      AND seq BETWEEN <a> AND <b> ORDER BY seq;" > /tmp/db-inspect/convo.jsonl
   ```
   then in Python print each entry's `role`, timestamp, and content — for assistant entries, only the parts where `type == "text"`.
6. **Persist what matters.** Feed the recovered words back to the user verbatim as proof, then write the recovered idea/concept into a file immediately (e.g. `<project>/IDEA.md`).

**Rule (Sep 2026):** user ideas discussed in-session get written to a file the same session — files survive, sessions don't. If the user asks "remember the idea we discussed" and the files have a gap, run this recovery *before* answering.

## Automation registry is memory too (check it when memory_search is empty)

Recurring reminders/automations often hold the only record of an old plan — and their payload text goes stale. When the user references a project and `memory_search` returns nothing (the files were never updated), check the automations registry before answering "no record":

1. **List automations** — find the job by name (look for a reminder-style cron, e.g. `0 12 * * 1` = every Monday).
2. **Read the job** — get `createdAtMs` plus the payload text; convert the timestamp with `python3 -c "import datetime; print(datetime.datetime.fromtimestamp(<ms>/1000))"`.
3. **Beware stale relative time.** If the payload says "yesterday"/"today" but the job was created days or weeks ago, it re-fires the same stale text on every run — never relay it as fresh news. Verify against the creation date first.
4. **Rewrite the payload with absolute dates** so future runs stop repeating the stale text.

**Rule:** `memory_search` only greps file layers — automation payloads live outside them. An empty search result does not mean there is no record.

## Security notes

- **Local-first by design.** All memory is plaintext on the machine that runs the agent. Treat memory directories like any personal data: back them up, don't commit them to public repos, and scrub names/secrets before publishing logs anywhere.
- The daily logs and LATEST file are raw by design — they are the memory. If you keep secrets in your workspace, keep them in a dedicated local store (`secrets/`, `*.env`) that is **git-ignored** and never referenced in log payloads. As a rule: log *that* an action happened, not the credentials it used.
- Optional off-machine backup should use SSH key authentication only — never credentials or secret-bearing env files in the repo.
- `memcheck` verifies a local secret store exists; that check is about confirming your agent's credential store is intact — it never reads or prints secret contents.

## Source & license

Source: https://github.com/mozz0/MeshMorize

Released under the MIT License. See LICENSE in the repository.
