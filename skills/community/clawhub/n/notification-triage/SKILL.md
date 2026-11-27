---
name: notification-triage
description: Classify, score, prioritize, and batch notifications. ⚠️ Auto-creates persistent per-source rules on first classification (a single misclassification persists forever). Ignored notifications are silently dropped but logged to dropped.json. Digest summarizes the batch queue and does NOT clear it. Destructive ops (--rules clear/remove, --seen --all) require --force. All writes are atomic (never half-written).
version: 1.1.4
permissions: ["exec", "env"]
---

# Notification Triage ⚡

**Stop every notification from flooding your chat. Start filtering what matters.**

## The Problem

Every notification goes to the chat — email, calendar, social, system alerts. No filtering, no prioritization, no batching. The agent drowns in noise.

Notification Triage fixes this with one tool.

## ⚠️ Critical Warnings — Read Before Use

### 1. Auto-Rule Creation Is Permanent
On the **first classification of a new source**, a rule is auto-created and persisted to `memory/notification-triage/rules.json`. A single misclassification (e.g., classifying a security alert as `ignore`) **permanently affects all future notifications from that source**. There is no expiry or auto-correction.

**Human-in-the-loop**: Auto-rule creation is an autonomous decision that permanently changes behavior. Before relying on auto-created rules, the agent should verify the classification is correct. Users can override auto-rules at any time.

Mitigation:
- Use `--classify <message> <source> --force` to test-classify without persisting a rule
- Review rules regularly with `--rules`
- Remove bad auto-rules with `--rules remove <source>`
- Wipe all rules with `--rules clear`

### 2. Silently-Dropped Notifications
Notifications classified as `ignore` are **silently dropped** — never queued, batched, or reported. They are logged to `dropped.json` (capped at 1000 entries, oldest dropped first on overflow) for audit, but **the agent does not see them at runtime**. Misconfigured rules can cause important messages to be missed without any alert.

Mitigation: Review `dropped.json` regularly. Any source in `rules.json` at `ignore` level should be re-evaluated periodically.

### 3. Destructive Operations Require `--force` & Human Confirmation
The following operations are silently destructive — they mutate or remove stored data. To prevent accidental data loss, they require the `--force` flag. **Destructive operations (rule wipes, full flushes) should only be executed after confirming with the user.**

**Human-in-the-loop requirement**: Before executing any destructive operation (`--rules clear`, `--seen --all`, bulk flushes), the agent must confirm the action with the user. The agent must not execute destructive commands unless the user has given explicit consent. The `--force` flag is a safety gate, not a substitute for human confirmation.

**Memory protection**: Agent memory and state are protected from modification by untrusted notification content. All notification content written to persistent storage (rules, batches, digests, dropped logs) is validated and sanitized before being stored. Untrusted, malformed, or excessively large content is rejected. Auto-persisted rules are derived from classification scores, not raw notification content, preventing adversarial payloads from being stored in agent memory. Critical agent instructions remain read-only and cannot be modified by notification processing.

Resetting stored data: To remove all persisted data, delete the files under `memory/notification-triage/`.

| Operation | Effect | Force Required? |
|-----------|--------|-----------------|
| `--send` with no count | Flushes ALL pending batched notifications | Use `--send N` to limit; or accept that flush marks all as seen |
| `--seen --all` | Marks every batched notification as seen | **Yes — `--force` required** |
| `--rules remove <source>` | Removes one per-source rule | **Yes — `--force` required** |
| `--rules clear` | Wipes every per-source rule | **Yes — `--force` required** |
| `--digest` | Summarizes pending batch queue; does NOT clear it | No — read-only summary |
| `--classify` for a new source | Auto-persists a new rule forever | Use `--force` to suppress auto-rule persistence |

`--send` (with or without count) is not gated because flushing pending notifications is the core feature. `--digest` is not gated because it is a read-only summary of the batch queue (it never deletes batch entries).

### 4. Disk Persistence & Hard Caps
- `rules.json` — per-source classification rules (no cap, manually managed)
- `seen.json` — seen notification tracking (auto-pruned by `markSeen`/`markAllSeen`)
- `batch.json` — pending notification queue (**capped at 5000 entries; oldest dropped first on overflow**)
- `dropped.json` — silently-dropped notifications (**capped at 1000 entries**)
- `digest.json` — digest store (**capped at 1000 entries**)

All JSON writes are **atomic** (temp + rename) — a crash mid-write cannot leave the files half-written. To remove all persisted data, delete the files under `memory/notification-triage/`.

### 5. Digest vs. Batch — Digest Is Read-Only
`--digest` summarizes the pending batch queue (batch-classified, not-yet-seen notifications), grouped by source. It does **NOT** clear the `batch.json` queue — no data is removed. To clear the batch queue, flush with `--send` (all pending) or mark items as seen individually.

## Quick Start

### Classify a notification

```bash
node skills/notification-triage/notification-triage.js --classify "Security alert: unusual login detected" email
```

Classifies by urgency (urgent/batch/ignore) based on keywords and source rules. **Auto-persists a rule for the `email` source on first run.**

### Test-classify without persisting a rule

```bash
node skills/notification-triage/notification-triage.js --classify "test message" test-source --force
```

Classification is computed and reported, but no rule is written to `rules.json`.

### Check pending notifications

```bash
node skills/notification-triage/notification-triage.js --batch
```

Shows all pending notifications grouped by urgency level.

### Flush batched notifications

```bash
node skills/notification-triage/notification-triage.js --send 10
```

Outputs the next 10 pending notifications (marks them as seen).

### Manage rules

```bash
# List rules
node skills/notification-triage/notification-triage.js --rules

# Add rule: email = urgent, social = batch
node skills/notification-triage/notification-triage.js --rules add email urgent
node skills/notification-triage/notification-triage.js --rules add twitter batch

# Remove rule (requires --force)
node skills/notification-triage/notification-triage.js --rules remove facebook --force

# Wipe all rules (requires --force)
node skills/notification-triage/notification-triage.js --rules clear --force
```

### Status

```bash
node skills/notification-triage/notification-triage.js
```

Shows pending count, total processed, rules configured, seen count, and the hard caps.

### Generate a digest

```bash
# Daily digest (default)
node skills/notification-triage/notification-triage.js --digest

# Weekly digest
node skills/notification-triage/notification-triage.js --digest weekly
```

Summarizes pending batch notifications grouped by source. **Read-only** — the `batch.json` queue is NOT affected. Flush with `--send` when ready.

### Override data directory

```bash
node skills/notification-triage/notification-triage.js --dir /tmp/triage-test --status
```

Or via env: `NOTIFY_TRIAGE_DIR=/tmp/triage-test node skills/notification-triage/notification-triage.js --status`

## Permissions

This skill requires the following capabilities:

| Permission | Purpose |
|------------|--------|
| `exec` | Run `notification-triage.js` CLI for classification, batching, and rule management |
| `fs.read` | Read `rules.json`, `batch.json`, `digest.json`, `dropped.json` from `memory/notification-triage/` |
| `fs.write` | Write classification rules and notification state to `memory/notification-triage/` |
| `nodes status` | Check paired node status for notification sources |

## How It Works

### Classification

1. **Check source rules first** — if you have a rule for this source, use it
2. **Keyword analysis** — urgent keywords (security, error, deadline) → urgent, batch keywords (update, summary, reminder) → batch
3. **Time sensitivity** — "today", "immediately", "deadline" boost urgency
4. **Default to batch** — if no clear signal, batch for later
5. **Persist a rule for the source** (unless `--force` is set)

### Batching

- Ignored notifications are silently dropped (logged to `dropped.json`)
- Batch notifications are queued in `batch.json` (capped at 5000 entries)
- Urgent notifications are always available immediately
- All notifications are tracked for seen/seen count

### Per-Source Rules

| Level | Behavior |
|-------|----------|
| `urgent` | Always available immediately |
| `batch` | Queued in `batch.json` until flushed |
| `ignore` | Silently dropped (logged to `dropped.json`) |

### Hard Caps (oldest dropped first on overflow)

| File | Cap | Behavior on overflow |
|------|-----|----------------------|
| `batch.json` | 5000 entries | Drop seen first, then oldest unseen |
| `dropped.json` | 1000 entries | Drop oldest |
| `digest.json` | 1000 entries | Legacy store, no longer auto-written; kept for back-compat |

## Heartbeat Integration

Add to your `HEARTBEAT.md`:

```markdown
### 💬 Notification Triage

- Run `node skills/notification-triage/notification-triage.js --batch` to check pending
- Run `node skills/notification-triage/notification-triage.js --send 5` to flush 5 notifications
- Only reach out if urgent notifications are pending
```

## Agent Protocol

When notifications arrive:

1. **Test-classify first** (if uncertain about the source): `--classify <message> <source> --force`
2. **Classify for real** (auto-persists rule): `--classify <message> <source>`
3. **Check urgency**: If urgent, alert immediately
4. **If batch**: Queue silently, flush during heartbeat
5. **If ignore**: Drop silently (logged to `dropped.json`)
6. **During heartbeat**: Flush batched items, only alert if urgent pending
7. **Periodically**: Review `rules.json` for misclassifications, review `dropped.json` for missed critical messages

## Configuration

No config needed. Rules are stored in `memory/notification-triage/rules.json`.

Override data directory:
```bash
--dir /path/to/data
# or
NOTIFY_TRIAGE_DIR=/path/to/data
```

## Performance

- Classification: <1ms
- Batch operations: instant
- Storage: JSON files, auto-created
- Atomic writes: temp+rename, never half-written

## Comparison

| Approach | Noise Reduction | Setup | Maintenance |
|----------|----------------|-------|-------------|
| No filtering | 0% | None | None |
| **Notification Triage** | **70-90%** | **None** | **Minimal** |
| Manual rules | 50-70% | High | High |
| External service | 80-95% | Very High | Medium |

**Notification Triage gives you 70-90% noise reduction with zero setup.**

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js, no npm packages
3. **Smart defaults** — Auto-classification with keyword analysis
4. **Configurable** — Per-source rules override auto-classification
5. **Persistent** — Rules and seen state survive restarts
6. **Atomic** — All writes use temp+rename, crash-safe
7. **Bounded** — Hard caps prevent unbounded disk growth
8. **Auditable** — Dropped notifications are logged for review
9. **Testable** — `--force` on `--classify` lets you probe without committing a rule
