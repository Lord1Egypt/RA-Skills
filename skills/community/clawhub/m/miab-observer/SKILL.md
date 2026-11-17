---
name: "miab-observer"
description: "Observe the MIAB transaction ledger: render callback events to a human-readable log, and optionally post closed-bottle summaries to a chat target. The observer half of the MIAB pair; requires miab-broker. Formerly published as `interagent-queue`."
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
    # The log sink -- the default, and everything under `miab_observer.py` -- touches
    # nothing but the local filesystem.
    - "openclaw message send (delegated subprocess; destination set by CLAW_CLOSED_TARGET)"
---

> **Formerly `interagent-queue`.** This skill was published under that name through 1.3.0 and
> renamed here at 2.0.0. If you are migrating: the script is now `scripts/miab_observer.py`, so
> cron `--command` lines need updating, but **all on-disk state carries over untouched** — the
> cursor, dedup state, log and ledger are keyed on `CLAW_HOME` / `LYRA_WORKSPACE`, never on the
> skill name. Nothing replays and nothing is re-delivered. See CHANGELOG.md.

# MIAB Observer — Asynchronous Transaction Observer

This skill governs the transaction processing, formatting, and file-based logging for the **Message-in-a-Bottle (MIAB) LIFO Callback Stack**. It decouples the observer and human-readability layers from the core `miab-broker` protocol.

---

## Prerequisites

- **`miab-broker` skill, version 2.0.0 or later**: `miab-observer` operates strictly as an
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

The observer (`scripts/miab_observer.py`) is a transaction monitor that tails the append-only callback events log (`state/callbacks/ledger.jsonl`). It parses events in real-time or via frequent interval sweeps, matches logical agent references (like `main`, `planner`, `coder`, or `reviewer`) with friendly icons, and formats them into clean, compact, human-readable log entries.

Transaction events are written directly to the observer log file (`$CLAW_HOME/logs/interagent-queue.log` by default, configurable via `CLAW_QUEUE_LOG`).

---

## 2. Invocations & Commands

The utility script `miab_observer.py` can be driven from the CLI to enable/disable sweeps, check cursor tracking status, or run isolated manual analysis.

Invoke it at `scripts/miab_observer.py`, resolved against wherever this skill is installed for you (written `<miab-observer>` below). There is no fixed absolute path that is correct across installs.

```bash
# Toggle logging sweeps
python3 <miab-observer>/scripts/miab_observer.py on
python3 <miab-observer>/scripts/miab_observer.py off

# Check cursor status, live state file, log file path, and target ledger
python3 <miab-observer>/scripts/miab_observer.py status

# Manually process and sweep all un-processed ledger records into the log file
python3 <miab-observer>/scripts/miab_observer.py process

# Peek at new ledger records inside stdout WITHOUT updating your cursor or writing to the log file
python3 <miab-observer>/scripts/miab_observer.py peek
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
  **The default log filename deliberately still says `interagent-queue`.** Renaming it would
  start a second log beside your existing one and silently orphan the first, and it would break
  any log rotation or shipping already pointed at that path — for cosmetics. The 2.0.0
  migration promise is that on-disk state carries over untouched, and this is part of keeping
  it. Set `CLAW_QUEUE_LOG` if you want a different name.

---

## 3a. The Message Sink (`scripts/notify_closed_bottles.py`)

Relocated here from `miab-broker` by ADR-001 T23: the broker is the writer, and a delivery sink
is a reader concern. The move is what lets the broker declare `network: []` without scoping it
to one file in prose, and it is why this skill declares network at all.

`miab_observer.py` remains the default and touches nothing but the local filesystem. The
message sink is separate, cron-driven, and never invoked by the log sink.

```bash
# Render what WOULD be sent, without sending or advancing any cursor
python3 <miab-observer>/scripts/notify_closed_dryrun.py
python3 <miab-observer>/scripts/notify_closed_dryrun.py --json
python3 <miab-observer>/scripts/notify_closed_dryrun.py <cid>

# Deliver closed-bottle summaries to CLAW_CLOSED_TARGET
python3 <miab-observer>/scripts/notify_closed_bottles.py
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
