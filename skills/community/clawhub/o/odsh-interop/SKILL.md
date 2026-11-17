---
name: odsh-interop
description: ODSH Bridge cross-container collaboration protocol — how the OpenClaw agent routes tasks between itself and a DeepSeek Harness (DSH) execution layer by task weight and predicted token cost: task envelopes, bridge zones, notification channel rules, optional read-only SQLite audit ledger
version: 5
author: odsh-bridge project
author_email: 319212746+rm-Vstar@users.noreply.github.com
maintainers:
  - 319212746+rm-Vstar@users.noreply.github.com
license: MIT
tags:
  - openclaw
  - dsh
  - bridge
  - interop
  - automation
categories:
  - integration
when_to_use: for every incoming operator request, decide whether to handle it yourself or relay it to the DSH execution layer; then use the bridge envelopes when relaying. DSH runs a self-starting bridge daemon, so it is always ready to receive and execute relayed tasks.
---

# ODSH-Interop Skill (OpenClaw side)

## Roles

- **OpenClaw (you) = brain / persona**: conversation, memory, dreaming, decisions,
  final judgement, and the **task router**.
- **DSH (DeepSeek Harness) = execution layer**: external/cross-application work —
  tools, code, retrieval, file/batch processing, and (if the operator enables the
  Cua channel, see docs/CUA-EXECUTION.md) Windows desktop actions.
- **Human operator = final arbiter** for anything uncertain.

## Task Routing Decision (do this for EVERY incoming request)

You are the router between **do it myself** and **relay to DSH**. Decide before
working, and re-decide if a task grows while you work.

### Step 1 — Weight the task (light / medium / heavy)

Estimate the task weight from: number of steps, external systems touched, data
volume, duration, and how much context it would add to this conversation.

- **Light**: single answer, one tool call, pure dialogue, memory lookup,
  summarisation, formatting, translation.
- **Medium**: a few steps, a couple of tools, some file work, short batch.
- **Heavy**: long/multi-step pipeline, lots of files or data, long-running
  execution, repeated tool calls, anything that would bloat your context window.

### Step 2 — Compare predicted token cost (the deciding factor)

Compare the predicted token cost of **doing it yourself** versus **relaying to
DSH** and pick the smaller side:

| Cost model | OpenClaw does it | DSH does it |
|---|---|---|
| conversation context growth | high — tools calls/outputs accumulate in your window | low — you only see the envelope + result summary |
| execution context | your window only | separate process, own context (theirs), your context stays stable |
| handoff overhead | none | one envelope write + one result read (small, fixed) |

- **Light tasks** usually cost less on your side (relay overhead would exceed the
  work itself) → **do it yourself**.
- **Heavy tasks** usually cost more on your side (context bloat from many tool
  calls) → **relay to DSH**.
- **Medium tasks**: compare honestly; if roughly equal, keep **neutral bias** —
  do it yourself unless DSH has an obvious advantage (filesystem-heavy, headless
  batch, external network work, more separate systems).

### Step 3 — capability check (DSH can execute on the Windows host)

`standard` DSH can execute **Windows desktop tasks via Cua Driver** (see
`docs/CUA-EXECUTION.md`): real screenshot, browser automation (CDP), click/type/
hotkey, app launch — focus-safe, over SSH to the host. So:

- For **files / code / fetch / batch / containers / data wrangling**: DSH fully
  available — relay when weight/cost favours it.
- For **Windows desktop tasks** (browser UI automation, screen, desktop actions):
  DSH can do them **if the Cua channel is enabled** (operator has installed Cua
  Driver + OpenSSH on the host and whitelisted DSH's key). Relay to DSH when
  enabled; otherwise tell the operator the Cua channel must be enabled first.

### Step 4 — never relay these to DSH

- Pure persona/identity/emotional/opinion conversations — always yours.
- Anything needing final human judgement — hold and ask the operator.
- Tiny lookups you can do in one call — more costly to relay than to just do.

> ⚠️ **Target routing** — mark the envelope `target` correctly: a `T-*.json` with
> `target: dsh` is consumed by the DSH daemon automatically; `target: openclaw` is
> left in `Input/` for an OpenClaw-side consumer (DSH's daemon never reads OpenClaw's
> mail). If it is a task for DSH, set `target: dsh` (or omit it); only set
> `target: openclaw` for something you yourself will pick up.

## Collaboration channels (bridge zones)

| Path | Purpose |
|---|---|
| `<BRIDGE>/Input/` | Task entry: `T-*.json` envelopes (SHARED) |
| `<BRIDGE>/output/` | Result exit: `T-*_result.json` (SHARED) |
| `<BRIDGE>/DSH-Workspace/` | DSH private zone (OpenClaw must not modify) |
| `<BRIDGE>/openclaw-workspace/` | OpenClaw private zone (DSH must not modify) |
| configured notification channel (e.g. Discord) | real-time status between both sides |

`<BRIDGE>` = the shared mount path both containers use (repo default `/root/ODSH-bridge`).

## Envelope contract (v1)

- A task is `input/T-<YYMMDD>-<seq>.json`; fields (see `docs/BRIDGE-SPEC.md`):
  `taskId / type / status / requester / target / createdMs / payload / context / result`.
- State machine: `queued -> running -> done | failed | cancelled`.
- Atomic writes: always `.tmp` → rename (never write a half file).
- Result: `output/<taskId>_result.json` with `status / finishedMs / by / payload / human / error`.

## What OpenClaw should do when relaying

1. Write an envelope `input/_T-*.json` (copy the template below), including your
   routing decision in `context`:
   ```json
   "context": { "channel": "<id>", "routingDecision": "relay-dsh: heavy, token-cost favourable" }
   ```
2. Don't block waiting: the DSH daemon picks it up, executes, writes the result
   and may notify the channel. Continue your own work meanwhile.
3. When a result arrives in `output/`:
   - Surface the `human` summary to the operator via your normal channel.
   - Keep a concise conclusion in memory; optionally drop a note into
     `<bridge>/openclaw-workspace/dream-feed/` for your dreaming pipeline.
4. You are the decider, DSH is the doer: anything needing persona/judgement/
   operator preference stays with you.
5. Prefer bridge envelopes over touching the other side's private zone.

## Template envelope (OpenClaw → DSH)

```json
{
  "schema": "odsh-envelope/v1",
  "taskId": "T-YYMMDD-XX",
  "type": "execute",
  "status": "queued",
  "requester": "openclaw",
  "target": "dsh",
  "createdMs": 0,
  "payload": {
    "kind": "run-command",
    "command": "<command>",
    "args": {}
  },
  "context": {
    "channel": "<notificationChannelId>",
    "routingDecision": "relayed_dsh: heavy task, predicted token cost lower on DSH"
  }
}
```

## Worked examples (routing)

| User says | Weight | Route | Why |
|---|---|---|---|
| "hi / who are you / tell me a story" | light | yourself | persona/dialogue, one round |
| "summarise my memory of last week" | light | yourself | one memory call, reply in place |
| "download this page and extract the tables" | heavy | DSH | network + file + parsing, would bloat your window |
| "run this analysis over 40 CSV files and give me the totals" | heavy | DSH | batch file work, DSH context stays clean |
| "search X for posts about LLM agents" | light-heavy | yourself (one web call) or DSH if multiple iterations | compare: one search = you; multi-iteration crawl = DSH |
| "open the browser, log into the dashboard, take a receipt" | heavy (windows desktop) | relay to DSH when the Cua channel is enabled | real desktop execution via Cua Driver |

## Setup (once)

Place this skill in your skills directory (e.g. `/root/.openclaw/skills/odsh-interop/SKILL.md`
or your skills path), then the collaboration works as long as:

- both containers share the bridge mount (same `<BRIDGE>` path);
- DSH has the bridge daemon **auto-started** (see below) — no manual start needed;
- the notification channel id is configured on both sides (envelope `context.channel` /
  DSH `.env` `DISCORD_CHANNEL_ID`).

## DSH is always ready (self-starting daemon)

Since v1.2, the DSH container auto-starts the bridge daemon at boot
(`scripts/dsh-entrypoint.sh` → `src/dshtrigger.mjs daemon`). You can assume DSH is
continuously watching `Input/` and will pick up any `T-*.json` envelope you drop —
no operator needs to start anything. If a result does not arrive, check that the DSH
container is running and the bridge mount is shared; a restart re-arms the daemon automatically.


## Optional SQLite audit ledger (read-only; v1.3.2+)

When the DSH bridge runs on **Node >=22.5** (built-in `node:sqlite`) with `BRIDGE_SQLITE=1` in `.env`, the DSH daemon mirrors every processed envelope into one lightweight file: **`<BRIDGE>/DSH-Workspace/dsh.db`**. This is optional, additive and fail-soft — if it is absent (old Node, or disabled), the JSON file store stays the source of truth.

You may **READ** this ledger directly to answer questions about bridge health/stats. It is **read-only for you** — never write to `DSH-Workspace/` (DSH owns that zone).

### Schema

| table / view | purpose |
|---|---|
| `dsh_envelopes` | one row per envelope: taskId, type, status, requester, target, createdMs / expiresMs / finishedMs, generated `duration` (= finishedMs - createdMs), trace_id / span_id / parent_span_id, raw_envelope |
| `dsh_events` | status-transition audit log (id, taskId, fromStatus, toStatus, timestamp) |
| `dsh_errors` | failed-task detail (taskId, error, traceback, timestamp) |
| `dsh_bridge_stats` | view — total_tasks, completed, failed, running, first_created, last_finished |

### Read it (zero extra deps — Node built-in)

```
<BRIDGE>=(the shared mount path; default /root/ODSH-bridge)
node --input-type=module -e "import('node:sqlite').then(({DatabaseSync})=>{const db=new DatabaseSync('<BRIDGE>/DSH-Workspace/dsh.db',{readOnly:true});console.log(db.prepare('SELECT * FROM dsh_bridge_stats').get());db.close();}).catch(()=>console.log('dsh.db not available - fall back to Output/*_result.json'))"
```

If you only have Python, the stdlib works: `python3 -c "import sqlite3; for r in sqlite3.connect('<BRIDGE>/DSH-Workspace/dsh.db').execute('SELECT * FROM dsh_bridge_stats'): print(r)"`. Prefer Node (`node:sqlite`) when available.

### Common read-only queries

- **Overview:** `SELECT * FROM dsh_bridge_stats;`
- **Recent tasks:** `SELECT taskId,status,duration,datetime(createdMs/1000,'unixepoch') AS created FROM dsh_envelopes ORDER BY createdMs DESC LIMIT 15;`
- **Failures:** join `dsh_envelopes` with `dsh_errors` on taskId where `status='failed'`.
- **Lifecycle of one task:** `SELECT fromStatus,toStatus,timestamp FROM dsh_events WHERE taskId='T-YYMMDD-XX' ORDER BY id;`
- **Trace across hops:** `SELECT taskId,span_id,parent_span_id,status FROM dsh_envelopes WHERE trace_id='...';`

### Guardrails

- Always open **`readOnly`**; never `INSERT`/`UPDATE`/`DROP` in `DSH-Workspace/`.
- `duration` is `NULL` when `finishedMs` is empty (still queued/running) — treat NULL, not 0.
- If `dsh.db` is missing or the query throws, **fall back to scanning `Output/*_result.json`** and tell the operator SQLite is off/old-Node — the file store is always authoritative.
- For heavy or uncertain aggregation, relay to DSH (see routing) rather than hand-writing complex SQL yourself.

## Notes

- The rest of the integration details live in the odsh-bridge repo
  (`docs/PROTOCOL.md`, `docs/BRIDGE-SPEC.md`, `MAINTENANCE.md`, `src/`).
- Re-decide the route if the task grows while you work (a "light" starting point
  can become heavy — switch to relay when the context bloat starts).