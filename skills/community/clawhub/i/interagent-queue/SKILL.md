---
name: "interagent-queue"
description: "DEPRECATED — renamed to `miab-observer`. This is the final release under the name `interagent-queue`; install `miab-observer` to keep receiving updates. Observe the MIAB transaction ledger: render callback events to a human-readable log, and optionally post closed-bottle summaries to a chat target. Requires miab-broker."
permissions:
  env: [CLAW_HOME, LYRA_WORKSPACE, CLAW_LEDGER, CLAW_QUEUE_STATE, CLAW_QUEUE_LOG, CLAW_REGISTRY,
        CLAW_CLOSED_TARGET, CLAW_CLOSED_STATE, CLAW_CLOSED_ACCOUNT]
  file_read:
    - "$CLAW_HOME/state/callbacks/ledger.jsonl"
    - "$CLAW_HOME/state/callbacks/agent-registry.json"
  file_write:
    - "$LYRA_WORKSPACE/state/callbacks/queue_state.json"
    - "$CLAW_HOME/logs/interagent-queue.log"
    - "$CLAW_HOME/state/callbacks/closed_bottle_state.json"
  network:
    # Indirect egress, and declared anyway. No socket is opened in this skill: the message
    # sink (scripts/notify_closed_bottles.py) shells out to `openclaw message send`, whose
    # transport and destination are configured outside this skill via CLAW_CLOSED_TARGET.
    # The log sink -- the default, and everything under `interagent_queue.py` -- touches
    # nothing but the local filesystem.
    - "openclaw message send (delegated subprocess; destination set by CLAW_CLOSED_TARGET)"
---

> ## ⚠️ This skill has been renamed to `miab-observer`
>
> **1.3.0 is the final release under the name `interagent-queue`.** Development continues as
> **`miab-observer`**, starting at 2.0.0.
>
> **Skill identity is keyed on the frontmatter `name`, so this install cannot follow the rename
> on its own.** No update to `interagent-queue` will ever become `miab-observer` — you have to
> install the new skill deliberately. This notice is the only signal you will get, which is why
> this release exists at all.
>
> **To migrate:**
> 1. Install `miab-observer` 2.0.0.
> 2. Point your cron entries at the new path. The script was renamed too:
>    `scripts/interagent_queue.py` → `scripts/miab_observer.py`. **An existing cron `--command`
>    line will keep invoking the old path and will silently stop working once you remove this
>    skill.**
> 3. Your state carries over untouched. `queue_state.json`, `closed_bottle_state.json`, the log
>    and the broker's ledger are all keyed on `CLAW_HOME` / `LYRA_WORKSPACE`, not on the skill
>    name, so the cursor and dedup state survive. No replay, no re-delivery.
> 4. Remove `interagent-queue`.
>
> **Why the rename.** The name described a queue; the skill is an observer over the broker's
> ledger and never queues anything. `miab-observer` also pairs it with `miab-broker`, which is
> the skill it cannot run without.
>
> **Upgrade regardless of the rename:** 1.3.0 fixes a cursor bug that replayed the entire ledger
> on a corrupt state file — live since 1.2.0 on 2026-07-22. See CHANGELOG.md.

# Interagent Queue — Asynchronous Transaction Observer

This skill governs the transaction processing, formatting, and file-based logging for the **Message-in-a-Bottle (MIAB) LIFO Callback Stack**. It decouples the observer and human-readability layers from the core `miab-broker` protocol.

---

## Prerequisites

- **`miab-broker` skill, version 2.0.0 or later**: `interagent-queue` operates strictly as an
  observer layer over `miab-broker`. `miab-broker` must be installed and initialized to produce
  the transaction ledger (`$CLAW_HOME/state/callbacks/ledger.jsonl`).

  The 2.0.0 floor is set by agent identity, not by the ledger format: `who()` resolves display
  names from the broker's `agent-registry.json`, and the `displayName` and `aliases` fields it
  reads were added by broker T14 in 2.0.0. Against an older broker the registry lookup finds
  nothing and every agent silently falls back to this file's built-in `AGENT_MAP` — which is the
  inconsistency (`SPECTRE` vs `ECHO`) that reading the registry exists to fix. The renderers are
  a weaker constraint: `authority-override` is a 2.0.0 event, but `corrupt` dates to broker
  1.2.0, so the renderers alone would not have forced 2.0.0.

---

## 1. What the Interagent Queue Observer Does

The observer (`scripts/interagent_queue.py`) is a transaction monitor that tails the append-only callback events log (`state/callbacks/ledger.jsonl`). It parses events in real-time or via frequent interval sweeps, matches logical agent references (like `main`, `planner`, `coder`, or `reviewer`) with friendly icons, and formats them into clean, compact, human-readable log entries.

Transaction events are written directly to the interagent queue log file (`$CLAW_HOME/logs/interagent-queue.log` by default, configurable via `CLAW_QUEUE_LOG`).

---

## 2. Invocations & Commands

The utility script `interagent_queue.py` can be driven from the CLI to enable/disable sweeps, check cursor tracking status, or run isolated manual analysis.

Invoke it at `scripts/interagent_queue.py`, resolved against wherever this skill is installed for you (written `<interagent-queue>` below). There is no fixed absolute path that is correct across installs.

```bash
# Toggle logging sweeps
python3 <interagent-queue>/scripts/interagent_queue.py on
python3 <interagent-queue>/scripts/interagent_queue.py off

# Check cursor status, live state file, log file path, and target ledger
python3 <interagent-queue>/scripts/interagent_queue.py status

# Manually process and sweep all un-processed ledger records into the log file
python3 <interagent-queue>/scripts/interagent_queue.py process

# Peek at new ledger records inside stdout WITHOUT updating your cursor or writing to the log file
python3 <interagent-queue>/scripts/interagent_queue.py peek
```

---

## 3. Storage & State Management

To decouple concerns and ensure multi-platform flexibility (e.g. running under separate user accounts, home directories, or containers), all operational locations resolve dynamically relative to home environments — nothing is hardcoded to a host path:

- **State Document:** `$LYRA_WORKSPACE/state/callbacks/queue_state.json` tracks cursor indexing
  (`last_processed_line`) and live enabled status (overrideable via `CLAW_QUEUE_STATE`). If this
  file exists but cannot be parsed, the observer exits `1` rather than rewinding the cursor —
  see §4.
- **Active Ledger Source:** `$CLAW_HOME/state/callbacks/ledger.jsonl` (provided by `miab-broker`,
  overrideable via `CLAW_LEDGER`).
- **Agent Registry:** `$CLAW_HOME/state/callbacks/agent-registry.json` (read-only, provided by
  `miab-broker`, overrideable via `CLAW_REGISTRY`). Authoritative source for agent display names.
- **Target Log File:** `$CLAW_HOME/logs/interagent-queue.log` (overrideable via `CLAW_QUEUE_LOG`).

---

## 3a. The Message Sink (`scripts/notify_closed_bottles.py`)

Relocated here from `miab-broker` by ADR-001 T23: the broker is the writer, and a delivery sink
is a reader concern. The move is what lets the broker declare `network: []` without scoping it
to one file in prose, and it is why this skill declares network at all.

`interagent_queue.py` remains the default and touches nothing but the local filesystem. The
message sink is separate, cron-driven, and never invoked by the log sink.

```bash
# Render what WOULD be sent, without sending or advancing any cursor
python3 <interagent-queue>/scripts/notify_closed_dryrun.py
python3 <interagent-queue>/scripts/notify_closed_dryrun.py --json
python3 <interagent-queue>/scripts/notify_closed_dryrun.py <cid>

# Deliver closed-bottle summaries to CLAW_CLOSED_TARGET
python3 <interagent-queue>/scripts/notify_closed_bottles.py
```

- **`CLAW_CLOSED_TARGET` is required and fails closed.** Unset, the notifier exits `1` with
  `{"ok": false, ...}` and sends nothing. There is no default target: a hardcoded channel id is
  both a secret in committed text and a way to mistarget delivery on a host that never configured
  the notifier.
- **`CLAW_CLOSED_ACCOUNT`** is optional, passed through as `--account`.
- **Delivery dedup state** lives at `$CLAW_HOME/state/callbacks/closed_bottle_state.json`
  (overrideable via `CLAW_CLOSED_STATE`), and is separate from the log sink's cursor.
- **Egress is delegated, not direct.** The notifier opens no socket; it shells out to
  `openclaw message send`, whose transport and destination are configured outside this skill.

Two known gaps, tracked and not addressed by the relocation: the two sinks still keep
*separate* cursors and dedup state (ADR-001 item 7 merges them, Phase 2), and
`notify_closed_dryrun.py` is still a separate script rather than a `--dry-run` flag
(ADR-001 item 10).

## 4. Failure Behaviour

The observer is a cursor over an append-only ledger, so its dangerous failure is not crashing —
it is **rewinding**. A cursor that silently returns to 0 replays every ledger record that has
ever existed into the log, and duplicated output is harder to notice, and harder to undo, than
no output at all.

So the state file is treated as load-bearing:

| Condition | Behaviour |
|---|---|
| `queue_state.json` absent | Genuine fresh start. Cursor begins at 0. |
| `queue_state.json` present but unparseable, not a JSON object, or carrying a `last_processed_line` that is not a non-negative integer | **Exit `1`** with `{"ok": false, ...}` on stderr. The cursor is never rewound and nothing is written to the log. |

Recovery is deliberate and belongs to the operator: inspect the file, repair it to the last known
good `last_processed_line`, or delete it to accept a full replay.

Two related guarantees, unchanged: `peek` never advances the cursor or writes to the log, and
`process` advances the cursor only once the batch has been delivered — or when the sweep produced
nothing to deliver.

## Quick Reference

```
on      → enable automated sweeps and active log file writing
off     → disable log writing (silent mode)
status  → view live cursor count, target log file, and active environment parameters
process → sweep the ledger, append new events to the log file, and advance cursor
peek    → inspect new transaction events on stdout without affecting the cursor or log file
```
