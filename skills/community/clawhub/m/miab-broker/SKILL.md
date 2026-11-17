---
name: miab-broker
description: Operate the Message-in-a-Bottle (MIAB) LIFO callback stack — the async inter-agent transport that lets agents delegate work, yield their turn, and get woken when results return instead of CPU-idling on poll loops. Use when registering wake paths, creating/forwarding/returning/resolving callbacks, or invoking the callback reaper.
permissions:
  env: [CLAW_HOME, CALLBACK_TTL_MIN]
  file_read:
    - "$CLAW_HOME/state/callbacks/**"
  file_write:
    - "$CLAW_HOME/state/callbacks/**"
    - "$CLAW_HOME/logs/callback-reaper.log"
  network: []
---

# MIAB Broker — Asynchronous Callback Message-in-a-Bottle Stack

This skill formalizes the **Message-in-a-Bottle (MIAB) LIFO Callback Stack**: the file-based asynchronous transport that the LYRA agent network uses to hand work between specialist agents without blocking a runtime turn.

It governs the protocol lifecycle of a bottle as it travels down a delegation chain and unwinds back up (`register → create → forward → return → resolve`).

**This skill reads and writes persistent state on disk and changes how agent wake events are routed.** See §4 for the security model and §5 for the exact files it touches.

**This skill makes no network calls.** `network: []` above covers everything in this
directory, with nothing scoped out of it in prose.

That became true by construction in ADR-001 T23: the two closed-bottle notifier scripts that used
to sit in `scripts/` — `notify_closed_bottles.py`, which shells out to `openclaw message send`, and
its `notify_closed_dryrun.py` companion — now live in the `miab-observer` reader, where the
delivery sink belongs and where `network` is declared for it. Nothing here reaches the network, and
nothing here reads the `CLAW_CLOSED_*` environment.

---

## 1. What the MIAB LIFO Callback Stack Is

Traditional multi-agent coordination wastes turns. A caller delegates a task, then **sits in a poll loop** asking "are you done yet?" — burning CPU, wall-clock, and tokens while the holder does the real work. The MIAB stack removes the poll loop entirely.

Instead of waiting, a caller pushes a lightweight **resume frame** onto an active registry ledger and **ends its turn immediately**. The frame is the "message in a bottle": a compact, self-contained capsule describing *what to do when woken* — a one-line `summary`, an ordered set of `steps`, what the caller `expects` back, and how to `integrate` the result. The agent's expensive session is freed the instant the bottle is dispatched.

The structure is a **stack (LIFO)**, not a flat queue. When a holder delegates further mid-chain (a `forward`), its own resume frame is **pushed on top** of the parent's frame, and the whole stack of frames travels with the work. As each agent finishes its part and calls `return`, the top frame is popped and its `wake` target is resurfaced — execution unwinds back up the chain in reverse order, exactly like a function call stack. The agent at the bottom of the stack is the **terminal root** (the original caller); when control returns to it, it finishes the overall task and `resolve`s the bottle.

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

### A note on agent names

The broker routes on **functional ids** (`main`, `planner`, `coder`, …) — those are the values you
pass to `--from` / `--to` and register with `register --agent`. The **persona names** that appear in
the diagram above and in the examples below (LYRA, SPECTRE, Cinder …) are display names from the
reference deployment, shown so the examples read naturally. They are illustrative, not required:
your ensemble will have its own.

| functional id | reference persona | typical role |
|---|---|---|
| `main` | ✨ LYRA | origin / terminal root — creates and resolves bottles |
| `planner` | 🥷⚔️ SPECTRE | decomposition and architecture; forwards mid-chain |
| `coder` | 💥 Cinder | implementation |
| `reviewer` | 🥷👁️ ECHO | review and verification |
| `debug` | 🔬 Zero | diagnosis |
| `utility` | 🛠️ Swift | general-purpose tasks |
| `free` | 🌌 VOID | scouting / research |
| `sigma` | ⚡ SIGMA | domain-specific (portfolio) |
| `sweep` | 🧹 Callback Reaper | not an agent — the reaper's ledger identity |

**`agent-registry.json` is the source of truth for routing**, and lookup is exact-match on the
functional id. An agent that self-identifies by persona (returning as `ECHO` rather than
`reviewer`) will miss the registry — register the persona as well, or use functional ids
consistently in `--from` / `--to`.

The sibling `miab-observer` skill keeps its own copy of this mapping for log rendering.

---

## 2. Callback Lifecycle (the `claw-callback.py` CLI)

The CLI is the single source of truth. **Every command prints a `next_step`** telling you exactly what to do next — follow it.

Invoke it at `scripts/bin/claw-callback.py`, resolved against wherever this skill is installed for you (written `<miab-broker>` below). You only need to supply that path on your *first* call: every `next_step` and `dispatch_message` the CLI prints back already contains its own absolute path, valid from any working directory.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py <cmd> [flags]
```

Always pass `callback://<id>` along when dispatching a task over the agent-to-agent message tool — the bottle ID is the only handle a peer needs.

### a) `register` — enable an agent's wake path

Registers an agent's wake path so the cron wake mechanism knows how to resurface it. Do this once per agent before it can be a callback target.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py register --agent <name> --agent-id <id>
```

`--agent` is the network nicename (`main`, `planner`, `coder`, …); `--agent-id` is the routable handle the gateway uses to deliver the wake event (e.g. `agent:planner`, **not** a transient session id).

Optional `--session-key` overrides the wake destination with an exact session (e.g. `agent:main:discord:channel:<id>`) so bottle completions land in a chat session instead of the agent's default lane. When set, `return`/`wake` emit `sessions_send(sessionKey=…)` instructions instead of `cron(action=wake, agentId=…)`.

**Names are case-insensitive and may have aliases.** `--agent ECHO`, `--agent echo` and `--agent Echo` are one agent, stored under the canonical lowercase key. Use `--alias` (repeatable) to register the other names an agent answers to — typically its persona name — so a call addressed to any of them routes to the same entry instead of falling through to the registry-miss path:

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py register \
  --agent reviewer --agent-id agent:reviewer \
  --alias ECHO --display-name "🥷👁️ ECHO (Reviewer)"
```

An alias may not shadow another agent's own name, and may not point at two agents — both are refused. `--display-name` is the human-facing label; the `miab-observer` observer reads it from here rather than keeping its own copy.

`--agent-id` is checked against `^agent:[a-z0-9_-]+$`. A value that doesn't match (a logical name pasted into the routing slot, say) is still stored — refusing would strand existing registries — but `register` returns a `warnings` array saying so, because wakes sent to a non-routing id go nowhere silently.

### b) `create` — enqueue a MIAB (first hop)

The caller creates a bottle, packages its resume context, dispatches, and ends its turn.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py create \
  --task "Analyze the generated architecture files" \
  --from main --to planner \
  --summary "Awaiting SPECTRE's architecture spec to integrate into the build plan" \
  --step "Read the emitted architecture map" \
  --step "Diff it against the current module layout" \
  --expects "Clean JSON spec mapping target modules" \
  --integrate "Merge the spec into build-plan.md, then dispatch to coder"
```

After `create`, dispatch the task to `--to` (see `wake`), then **END YOUR TURN**.

### c) `wake` — get the exact dispatch call

Resolves the target agent in the registry and prints the ready-to-send `dispatch_message` plus the exact `cron(action=wake, …)` call. This is how a task actually reaches its holder; run it after `create` or `forward`.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py wake --id cb-XXXX [--to <agent>]
```

`--to` overrides the target; without it the current holder is used. On a registry miss the command **exits non-zero** and tells you to register the agent first — the `dispatch_message` is still printed so you can send it manually if you know the `agentId`.

### d) `forward` — delegate further mid-chain

When a holder needs to delegate onward, `forward` stacks its own return frame **on top of the parent's** — the entire stack travels with the work.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py forward \
  --id cb-XXXX --from planner --to coder \
  --summary "Awaiting Cinder's implementation diff to fold back into the plan" \
  --step "Review the patch for spec compliance" \
  --expects "Unified diff + test results"
```

Same resume-context flags as `create`. After forwarding, dispatch onward (`wake`) and end your turn. The parent's frame is untouched underneath; it will be woken after yours pops.

**Only the current holder may forward** (see §4a). Two chain shapes are refused outright:

- **A cycle** — forwarding to yourself, or to an agent already waiting on the stack. That agent is blocked on this bottle; handing it the work deadlocks the chain.
- **A runaway** — a stack already `MAX_STACK_DEPTH` (8) frames deep.

Both are overridable with `--allow-cycle` when the shape is deliberate.

### e) `return` — complete and unwind up the stack

When an agent finishes its part, it pops its frame and surfaces the next holder up the chain.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py return \
  --id cb-XXXX --from coder --result "Implemented; 14/14 tests pass, diff attached" \
  [--artifact path/or/url]
```

`return` prints a ready-to-send `dispatch_message` aimed at the frame's `wake` agent — send it via agent-to-agent and end your turn. If `return` reports `terminal: true`, control has reached the origin (bottom of stack); finish the overall task and proceed to `resolve`.

### f) `resolve` — tear down at the terminal root

The origin agent, once the whole task is delivered to the user, tears the bottle down.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py resolve --id cb-XXXX --from main [--result "..."]
```

The envelope is deleted; a single summary line is retained in the ledger for audit.

`resolve` requires **both** that `--from` is the bottle's `createdBy` **and** that the stack is empty — the chain has fully unwound and `return` reported `terminal: true`. A non-empty stack means agents are still waiting to be woken, and resolving strands them with no notification. Unwind with `return`, or `cancel` the bottle. `--force` overrides, and records why (§4a).

### g) `cancel` — abort an active stack

Cancel a pending stack to stop runaway processing or token waste.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py cancel --id cb-XXXX --from main --reason "Runaway token usage"
```

Status becomes `cancelled` and the envelope is atomically moved to `$CLAW_HOME/state/callbacks/archive/<id>.json` for retrospective analysis. Any stuck sub-agent that later tries `show` or `return` on that id fails fast, because the file is no longer in the hot directory.

### h) `show` — inspect one bottle

Reload the full context of a bottle: task, holder, the active resume frame, remaining stack, and results so far. This is what a woken agent runs first.

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py show --id cb-XXXX        # human-readable
python3 <miab-broker>/scripts/bin/claw-callback.py show --id cb-XXXX --json # full envelope
```

### i) `list` — see all in-flight bottles

```bash
python3 <miab-broker>/scripts/bin/claw-callback.py list          # status table
python3 <miab-broker>/scripts/bin/claw-callback.py list --json   # programmatic
```

Reports a `quarantined` count if any unreadable envelopes were moved aside during the scan (see §4).

---

## 3. State, Files & Envelope Schema

All broker state lives under `$CLAW_HOME/state/callbacks/` — `CLAW_HOME` defaults to `~/.openclaw`.

| path | written by | purpose |
|---|---|---|
| `ledger.jsonl` | every mutating command | append-only event log (the audit spine) |
| `cb-<id>.json` | `create`/`forward`/`return` | one live envelope per in-flight bottle |
| `agent-registry.json` | `register` | logical agent → routable `agentId` wake map |
| `archive/<id>.json` | `cancel` | cancelled bottles, kept for post-mortem |
| `archive/corrupt/<id>.json` | `list`/`sweep` | quarantined unreadable envelopes |
| `archive/` (other files) | — | **not written by this skill.** Anything here that isn't `cb-*.json` was put there by something else; the broker neither reads nor removes it |
| `$CLAW_HOME/logs/callback-reaper.log` | `reap-callbacks.sh` | reaper run log |

Envelopes are **deleted on completion** (`resolve`/reaped) — only the one-line ledger summary persists.

### Envelope schema

```jsonc
{
  "id":        "cb-20260801214133-9b06a0", // cb- + 14-digit UTC stamp + 6 hex
  "version":   "2.0.0",
  "status":    "pending",                  // pending | resolved | cancelled | failed
  "task":      "…",                        // overall delegated work
  "createdBy": "main",                     // origin agent (the only valid resolver)
  "holder":    "planner",                  // who currently owns the work
  // createdBy, holder and stack[].agent are stored canonically (lower-cased, trimmed)
  "createdAt": "2026-08-01T21:41:33Z",
  "updatedAt": "2026-08-01T22:14:12Z",
  "stack":  [ { "agent": "main", "resume": { … }, "pushedAt": "…" } ],  // LIFO, bottom-first
  "active": { "agent": "…", "resume": { … } },  // frame popped by the last `return`
  "results": [ { "from": "coder", "result": "…", "artifacts": [], "at": "…" } ],
  "history": [ { "at": "…", "agent": "…", "action": "create", "detail": "…" } ]
}
```

A **resume** object accepts exactly four keys — `summary` (string), `steps` (list of strings), `expects` (string), `integrate` (string). Anything else is rejected.

Ledger records are one JSON object per line: `{at, id, event, by, …}` where `event` is one of `create`, `forward`, `return`, `resolve`, `cancel`, `fail`, `corrupt`, `authority-override`. The sibling `miab-observer` skill parses this file — treat the field names as a compatibility contract, and note that adding an event type without adding a renderer there makes it *invisible* rather than an error.

`authority-override` records a call that the §4a rules would have refused and that was forced through: `{id, event: "authority-override", by, action, expected, stack_remaining?}`. It is written *in addition to* the normal event, never instead of it.

---

## 4. Security Model

### 4a. Authority — who may do what to a bottle

`--from` states who is acting. Each mutating command requires that the caller is the agent the envelope says is entitled to act:

| command | requires | rationale |
|---|---|---|
| `forward` | `--from` == current `holder` | only whoever holds the work can delegate it onward |
| `return` | `--from` == current `holder` | only the holder can pop the frame and wake the next agent |
| `resolve` | `--from` == `createdBy` **and** an empty stack | the originator tears down, once the chain has unwound |
| `cancel` | `--from` == `createdBy` | the originator aborts what it started |

Comparison is on canonical names, so an agent that identifies as `ECHO` where the envelope recorded `reviewer` is recognised as the same agent (§2a).

Every one of these accepts `--force`. The call then proceeds and an `authority-override` event is appended to the ledger naming the actor, the action, and the agent that was entitled to it. The override is loud and permanent by design: forcing is sometimes correct — a wedged holder that will never return — and should always be visible afterwards.

**This is authorisation, not authentication.** `--from` is still an unverified assertion: any process that can run the CLI can claim to be any agent. What these rules stop is the accidental case — the misrouted `return`, the wrong agent resolving someone else's chain, the double-popped frame — which is what the ledger shows actually happening. They are not a defence against a local process that is deliberately lying about its identity; see "Known limitations" below.


**Trust boundary.** The broker assumes every process that can read `$CLAW_HOME` is trusted. It is designed for a single-user host running one agent ensemble. It is **not** hardened for a shared or multi-tenant machine.

**What is enforced:**

- **Callback ids are validated** against `^cb-\d{14}-[0-9a-f]{6}$` and every resolved path is asserted to stay inside the callback root. Ids arrive from agent-generated `callback://` text, so this is the boundary against a malformed or hostile id reaching the filesystem.
- **`CLAW_HOME` is validated** on startup: it must be owned by the current user and must not be group- or world-accessible. A poisoned `CLAW_HOME` would otherwise redirect `agent-registry.json`, and with it every wake event.
- **File modes.** The process sets `umask 0077`; state directories are `0700` and state files `0600`.
- **Resume inputs are constrained.** `--resume-file` must live under `$CLAW_HOME` unless `--allow-outside` is passed, is capped at 64 KB, and both `--resume-file` and `--resume-json` are schema-validated.
- **Failures are loud.** Every error path emits `{"ok": false, "error": …}` on stderr and exits non-zero. Unreadable envelopes are quarantined to `archive/corrupt/` with a `corrupt` ledger event rather than silently skipped.

**What is *not* protected — know these before trusting the broker with anything sensitive:**

- **`--from` is an unverified claim.** Any caller can assert any agent identity. Holder and root ownership are not yet enforced, so a misbehaving agent can pop another's frame or resolve a chain it doesn't own.
- **No integrity or replay protection.** Envelopes are plain JSON with no signature. A local process can edit a bottle to redirect its `wake` target or rewrite `resume.steps` — which become instructions read by the woken agent.
- **No concurrency safety.** Envelope writes are not locked; two agents mutating one bottle simultaneously can corrupt it.
- **State is plaintext and retained.** Task text, results, and artifact paths persist in `ledger.jsonl`, which is never pruned. **Do not put secret values in `--task`, `--summary`, or `--result`** — they are written to disk and travel to other agents in `dispatch_message` text.

See `SECURITY.md` for the threat model and reporting contact.

---

## 5. Reaping Stale Bottles (`scripts/reap-callbacks.sh`)

Orphaned bottles (a holder crashed, a wake never fired) would otherwise linger as `pending` forever. The reaper wraps the CLI's deterministic, LLM-free `sweep` subcommand: it marks `pending` envelopes older than a configurable age as `failed`, appends a `fail` ledger event for each, purges the dead envelope, and clears dangling `*.json.tmp` write-handles.

```bash
scripts/reap-callbacks.sh                 # default: bottles older than 120m (CALLBACK_TTL_MIN)
scripts/reap-callbacks.sh --max-age 6h    # custom threshold (s/m/h/d suffixes)
scripts/reap-callbacks.sh --dry-run       # report only, change nothing
```

> **Do not schedule the reaper on the default threshold without measuring your workload first.**
> Delegation latency is typically bimodal — fast machine turnarounds alongside long human- or
> cron-gated waits. A single global TTL that suits the first will destroy live work in the second.
> Run `--dry-run` on a cron for a week and review `$CLAW_HOME/logs/callback-reaper.log` before
> enabling `--fail`.

---

## 6. Troubleshooting

| symptom | cause | fix |
|---|---|---|
| `invalid callback id: '…'` | The id isn't the `cb-<14 digits>-<6 hex>` form. Usually a truncated or hand-typed id | Use the exact id from `create`/`list`; don't abbreviate |
| `CLAW_HOME root … is owned by uid …` | `CLAW_HOME` points at a tree you don't own | Correct the env var, or `chown` the directory |
| `… has mode 0o755 (must not be group- or world-accessible)` | State root is too permissive | `chmod 700 $CLAW_HOME` |
| `--resume-file … is outside CLAW_HOME` | Reading a resume object from an unconstrained path | Move it under `$CLAW_HOME`, or pass `--allow-outside` deliberately |
| `resume context has unknown keys: [...]` | Resume object has keys beyond the permitted four | Use only `summary`, `steps`, `expects`, `integrate` |
| `wake` exits non-zero, `registry_miss: true` | Target agent isn't registered under any name it answers to | `register` it, or add the name it used with `register --alias` |
| `forward refused: --from '…' is not the current holder` | An agent tried to delegate a bottle it doesn't hold | Check `show --id` for the real holder; `--force` if deliberate |
| `resolve refused: … still has N frame(s) on the stack` | The chain hasn't unwound; agents are still waiting | `return` up the chain, or `cancel`; `--force` records an override |
| `resolve refused: --from '…' is not the originator` | A mid-chain agent tried to close someone else's bottle | The `createdBy` agent resolves; `--force` if deliberate |
| `forward refused: '…' cannot forward to itself` | Self-forward — usually a persona/function name confusion | Check the `--to`; `--allow-cycle` if genuinely intended |
| `forward refused: … MAX_STACK_DEPTH=8` | Delegation chain has run away | Unwind it; `--allow-cycle` to override |
| `register` returns `warnings: [… does not look like a routing id …]` | A logical name was passed to `--agent-id` | Pass the routable handle (`agent:<slug>`), not the nicename |
| `callback … is resolved, cannot forward` | Bottle already terminal | Start a new bottle; terminal states are final |
| `list` reports quarantined envelopes | An envelope was unreadable and moved to `archive/corrupt/` | Inspect it there; the `corrupt` ledger event records why |
| Bottle sits `pending` far longer than expected | Wake never delivered, or holder never returned | `show --id` to see the holder, then re-`wake`; there is no automatic redelivery yet |

---

## Quick Reference

```
register  → enable an agent's wake path, + --alias / --display-name (once per agent)
create    → push first resume frame, dispatch, END TURN          (caller)
wake      → emit the exact cron dispatch call for a bottle       (after create/forward)
forward   → stack frame on top, delegate onward, END TURN        (mid-chain holder)
return    → pop frame, wake next holder up the stack             (finished holder)
resolve   → tear down bottle at the origin, stack must be empty  (terminal root)
cancel    → abort a pending stack, archive it for post-mortem    (originator)
show      → reload one bottle's full context                     (woken agent, first call)
list      → table of all in-flight bottles                       (operator)
reap      → fail + clean stale/orphaned bottles                  (garbage collector)
```
