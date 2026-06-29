---
name: miab-broker
description: Operate the Message-in-a-Bottle (MIAB) LIFO callback stack — the async inter-agent transport that lets agents delegate work, yield their turn, and get woken when results return instead of CPU-idling on poll loops. Use when registering wake paths, creating/forwarding/returning/resolving callbacks, observing the ledger, or piping live callback activity to Discord.
---

# MIAB Broker — Asynchronous Callback Message-in-a-Bottle Stack

This skill formalizes the **Message-in-a-Bottle (MIAB) LIFO Callback Stack**: the file-based
asynchronous transport that the LYRA agent network uses to hand work between specialist agents
without blocking a runtime turn.

It governs two concerns:

1. **The protocol** — the `claw-callback.py` registry CLI and the lifecycle of a bottle as it
   travels down a delegation chain and unwinds back up (`register → create → forward → return →
   resolve`).
2. **The observer** — `scripts/interagent_queue.py`, which tails the callback ledger, renders
   raw events into rich human-readable logs, and (when toggled on) pipes them to the
   `#scheduling` Discord channel.

---

## 1. What the MIAB LIFO Callback Stack Is

Traditional multi-agent coordination wastes turns. A caller delegates a task, then **sits in a
poll loop** asking "are you done yet?" — burning CPU, wall-clock, and tokens while the holder
does the real work. The MIAB stack removes the poll loop entirely.

Instead of waiting, a caller pushes a lightweight **resume frame** onto an active registry
ledger and **ends its turn immediately**. The frame is the "message in a bottle": a compact,
self-contained capsule describing *what to do when woken* — a one-line `summary`, an ordered set
of `steps`, what the caller `expects` back, and how to `integrate` the result. The agent's
expensive session is freed the instant the bottle is dispatched.

The structure is a **stack (LIFO)**, not a flat queue. When a holder delegates further
mid-chain (a `forward`), its own resume frame is **pushed on top** of the parent's frame, and
the whole stack of frames travels with the work. As each agent finishes its part and calls
`return`, the top frame is popped and its `wake` target is resurfaced — execution unwinds back
up the chain in reverse order, exactly like a function call stack. The agent at the bottom of
the stack is the **terminal root** (the original caller); when control returns to it, it
finishes the overall task and `resolve`s the bottle.

Why this matters:

- **No CPU idling / no continuous polling.** Agents never spin waiting for a peer; they yield
  and are woken by the cron-driven wake path (`action=wake`).
- **Context is carried, not reconstructed.** The resume frame is an optimized temp-context
  vector — just enough state to resume cold, so a woken agent doesn't re-derive everything.
- **The stack self-documents.** Every push/pop is an append-only ledger event, giving a full,
  replayable audit trail of the delegation chain.

```
       [Caller / Root: LYRA]            ← terminal root (bottom of stack)
             │  create: push resume frame, dispatch callback://<id>, END TURN
             ▼
      [Holder: SPECTRE]                 ← frame pushed on forward
             │  plans; forward: push its own frame on top, dispatch onward, END TURN
             ▼
       [Holder: Cinder]                 ← top of stack
             │  does the work; return: pop frame, wake SPECTRE
             ▼
      [SPECTRE woken] → return → [LYRA woken] → resolve (bottle deleted, summary kept)
```

---

## 2. Callback Lifecycle (the `claw-callback.py` CLI)

The registry CLI is the single source of truth. **Every command prints a `next_step`** telling
the agent exactly what to do next — follow it. Canonical location on the live host:

```bash
python3 ~/.openclaw/scripts/claw-callback.py <cmd> [flags]
```

Full protocol spec lives at `~/.openclaw/CALLBACKS.md`. Always pass `callback://<id>` along when
dispatching a task over the agent-to-agent message tool — the bottle ID is the only handle a
peer needs.

### a) Register a waking agent

Registers an agent's wake path so the cron wake mechanism knows how to resurface it. Do this
once per agent before it can be a callback target.

```bash
python3 scripts/claw-callback.py register --agent <name> --agent-id <id>
# e.g.
python3 scripts/claw-callback.py register --agent main --agent-id agent:main
```

`--agent` is the network nicename (`main`, `planner`, `coder`, …); `--agent-id` is the routable
handle the gateway uses to deliver the wake event.

### b) Enqueue / create a MIAB (first hop)

The caller creates a bottle, packages its resume context, dispatches, and ends its turn.

```bash
python3 scripts/claw-callback.py create \
  --task "Analyze the generated architecture files" \
  --from main --to planner \
  --summary "Awaiting SPECTRE's architecture spec to integrate into the build plan" \
  --step "Read the emitted architecture map" \
  --step "Diff it against the current module layout" \
  --expects "Clean JSON spec mapping target modules" \
  --integrate "Merge the spec into build-plan.md, then dispatch to coder"
```

This is where you set up the **optimized temp context vector**. Keep frames lean — they exist
only to let a cold-woken agent resume without re-reasoning:

- `--summary` — one line: what you're waiting for and why.
- `--step` — repeatable; the ordered actions to perform when woken.
- `--expects` — the shape/contract of the result you want back.
- `--integrate` — what to do with the result once you have it.

After `create`, dispatch the task (including `callback://<id>`) to `--to` via the agent-to-agent
message tool, then **END YOUR TURN**.

### c) Forward a mid-chain request

When a holder needs to delegate further, `forward` stacks its own return frame **on top of the
parent's** — the entire stack travels with the work.

```bash
python3 scripts/claw-callback.py forward \
  --id cb-XXXX --from planner --to coder \
  --summary "Awaiting Cinder's implementation diff to fold back into the plan" \
  --step "Review the patch for spec compliance" \
  --expects "Unified diff + test results"
```

Same resume-context flags as `create`. After forwarding, dispatch onward and end your turn. The
parent's frame is untouched underneath; it will be woken after yours pops.

### d) Complete and return up the stack

When an agent finishes its part, it pops its frame and surfaces the next holder up the chain.

```bash
python3 scripts/claw-callback.py return \
  --id cb-XXXX --from coder --result "Implemented; 14/14 tests pass, diff attached"
```

`return` prints a ready-to-send `dispatch_message` aimed at the frame's `wake` agent — send it
via agent-to-agent and end your turn. If `return` reports `terminal: true`, control has reached
the origin (bottom of stack); finish the overall task and proceed to `resolve`.

### e) Resolve the terminal root

The origin agent, once the whole task is delivered to the user, tears the bottle down.

```bash
python3 scripts/claw-callback.py resolve --id cb-XXXX --from main
```

The envelope is deleted; a single summary line is retained in the ledger for audit. Only the
root (`terminal: true`) should resolve.

---

## 3. State & Tracking Files

All broker state lives under `$CLAW_HOME/state/callbacks/` — `CLAW_HOME` defaults to `~/.openclaw`
(the CLI otherwise falls back to the parent of its own script dir). Four artifacts live there:

| file                  | written by        | purpose                                              |
|-----------------------|-------------------|------------------------------------------------------|
| `ledger.jsonl`        | `claw-callback.py`| append-only event log (the audit spine)              |
| `cb-<id>.json`        | `claw-callback.py`| one live envelope per in-flight bottle (the stack)   |
| `agent-registry.json` | `register`        | logical agent → routable `agentId` wake map          |
| `queue_state.json`    | `interagent_queue.py` | observer toggle + ledger cursor (see §4)         |

Envelopes are **deleted on completion** (`resolve`/reaped) — only the one-line ledger summary
persists. Documentation uses the logical `state/callbacks/...` path; the observer honors
`$CLAW_HOME` (and a `$CLAW_LEDGER` override) so the skill stays portable.

### `state/callbacks/ledger.jsonl` — the event ledger

Append-only JSON-Lines log. **One event per line**; the observer reads it incrementally by line
offset and never rewrites it. Each record carries `event`, `id`, `by`, and a timestamp, plus
event-specific fields:

| event      | key fields                                  | meaning                                   |
|------------|---------------------------------------------|-------------------------------------------|
| `create`   | `to`, `task`, summary/steps/expects          | bottle enqueued (frame pushed)            |
| `forward`  | `to`                                         | frame stacked on top, work delegated on   |
| `return`   | `wake`                                        | frame popped, next holder up surfaced     |
| `resolve`  | `task`, `result`                             | terminal root closed the bottle           |
| `fail`     | `reason`, `holder`                           | bottle reaped/failed (stale or error)     |

The ledger auto-rotates: when it crosses ~10k lines, `sweep` archives it to `ledger.<stamp>.jsonl`
and starts fresh, so the observer cursor should tolerate rotation (it re-reads from line 0 of the
new file).

### `state/callbacks/queue_state.json` — live toggle & cursor

Small JSON holding the observer's runtime state:

```json
{
  "enabled": false,
  "last_processed_line": 24,
  "target_channel": "channel:1517433532518109195"
}
```

- `enabled` — master toggle. When `false`, the observer skips sweeps entirely (no Discord
  traffic). Flip with `interagent_queue.py on` / `off`.
- `last_processed_line` — the cursor into the ledger; guarantees each event is rendered exactly
  once across runs. Written atomically (temp-file + replace).
- `target_channel` — destination for piped logs (default `#scheduling`,
  `channel:1517433532518109195`).

---

## 4. The Observer (`scripts/interagent_queue.py`)

A read-only transaction observer over the ledger. It converts raw `create`/`forward`/`return`/
`resolve`/`fail` records into beautiful rich-text logs using the agent identity map (nicenames
+ icons), advances the `last_processed_line` cursor, and — when `enabled` and a delivery path is
available — pipes the formatted batch to the `#scheduling` Discord channel.

```bash
# Toggle the live pipe
python3 scripts/interagent_queue.py on      # enable sweeps + Discord delivery
python3 scripts/interagent_queue.py off     # disable (silent)

# Inspect / drive
python3 scripts/interagent_queue.py status  # {enabled, cursor, target_channel}
python3 scripts/interagent_queue.py process # render + deliver new events (respects toggle)
python3 scripts/interagent_queue.py peek    # render new events to stdout WITHOUT advancing cursor or delivering
```

Wire `process` to a frequent cron tick (e.g. every minute) so callback activity streams to
Discord in near-real-time while agents stay yielded. Delivery uses the `openclaw` notify path;
if it isn't on PATH the observer degrades gracefully to stdout JSON so it's safe to run anywhere.

---

## 5. Reaping Stale Bottles (`scripts/reap-callbacks.sh`)

Orphaned bottles (a holder crashed, a wake never fired) would otherwise linger as `pending`
forever. The reaper is a thin wrapper over the CLI's deterministic, LLM-free `sweep` subcommand:
it marks `pending` envelopes older than a configurable age as `failed`, appends a `fail` ledger
event for each (so the observer surfaces the reap to Discord), purges the dead envelope, and
sweeps any dangling `*.json.tmp` write-handles left by interrupted atomic saves.

```bash
scripts/reap-callbacks.sh                 # default: reap bottles older than 120m (CALLBACK_TTL_MIN)
scripts/reap-callbacks.sh --max-age 6h    # custom threshold (s/m/h/d suffixes)
scripts/reap-callbacks.sh --dry-run       # report what WOULD be reaped, change nothing
```

Under the hood it calls `claw-callback.py sweep --older-than <minutes> --fail` (dry-run drops
`--fail`), logs a compact line to `$CLAW_HOME/logs/callback-reaper.log`, and exits non-zero on
error so a scheduler can alert. Run it on a periodic cron / launchd agent (hourly or daily) as
the network's garbage collector.

---

## Quick Reference

```
register  → enable an agent's wake path (once per agent)
create    → push first resume frame, dispatch, END TURN          (caller)
forward   → stack frame on top, delegate onward, END TURN        (mid-chain holder)
return    → pop frame, wake next holder up the stack             (finished holder)
resolve   → tear down bottle at the origin                       (terminal root)
reap      → fail + clean stale/orphaned bottles                  (garbage collector)
```
