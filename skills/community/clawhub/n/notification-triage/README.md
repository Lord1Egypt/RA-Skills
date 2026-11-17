# Notification Triage 🔔

**Smart filtering and batching for agent notifications. Classifies by urgency (urgent/batch/ignore), tracks seen state, manages per-source rules, and batches non-urgent items.**

## Why Notification Triage?

Notifications pile up fast — heartbeat checks, build updates, monitoring alerts, scheduled reports. Notification Triage cuts through the noise:

- **Urgency classification** — Keywords and patterns sort into urgent/batch/ignore automatically
- **Per-source rules** — Override classification for specific notification sources
- **Notification batching** — Non-urgent notifications queue for digest delivery
- **Seen tracking** — Mark individually or in bulk, never re-process
- **Digest generation** — Daily or on-demand summaries of batched notifications
- **Zero dependencies** — Pure Node.js, JSON-backed, fully local

---

## Installation

```bash
# Already included in OpenClaw workspace at skills/notification-triage/
# No npm install needed — pure Node.js
```

---

## Quick Start

```bash
# Classify a notification
node skills/notification-triage/notification-triage.js --classify "server down" monitor

# Show pending batch
node skills/notification-triage/notification-triage.js --batch

# List rules
node skills/notification-triage/notification-triage.js --rules

# Add a rule
node skills/notification-triage/notification-triage.js --rules add monitor urgent

# Generate daily digest
node skills/notification-triage/notification-triage.js --digest daily

# Status overview
node skills/notification-triage/notification-triage.js --status
```

---

## Commands Reference

### Classify

```bash
node skills/notification-triage/notification-triage.js --classify <message> <source>
```

Classifies a notification by message text and source. Uses:
- **Urgent keywords**: urgent, critical, security, alert, error, fail, crash, down, breach, leak, hack, attack, payment, billing, deadline, immediate, asap, emergency, outage, incident
- **Batch keywords**: update, summary, report, digest, newsletter, weekly, monthly, reminder, scheduled, notification
- **Time sensitivity**: today, tomorrow, now, immediately, before, by end, due, expires, final, last chance

```
[notify-triage] Classified: urgent (score: 3)
```

### Batching

```bash
# Show pending batch
node skills/notification-triage/notification-triage.js --batch

# Show count of pending
node skills/notification-triage/notification-triage.js --batch 5

# Flush and send batch
node skills/notification-triage/notification-triage.js --send

# Flush count
node skills/notification-triage/notification-triage.js --send 10
```

### Seen Tracking

```bash
# Mark notification as seen
node skills/notification-triage/notification-triage.js --seen <id>

# Mark all as seen
node skills/notification-triage/notification-triage.js --seen --all
```

### Rule Management

```bash
# List all rules
node skills/notification-triage/notification-triage.js --rules

# Add rule (urgent|batch|ignore)
node skills/notification-triage/notification-triage.js --rules add cron batch

# Remove rule
node skills/notification-triage/notification-triage.js --rules remove cron
```

### Digests

```bash
# Daily digest
node skills/notification-triage/notification-triage.js --digest daily

# Hourly digest
node skills/notification-triage/notification-triage.js --digest hourly
```

---

## Classification Algorithm

1. **Source-specific rules first** — If a rule exists for the source, use it immediately
2. **Keyword scoring** — Each urgent keyword +2, each batch keyword -1, time-sensitive +1
3. **Thresholds** — Score ≥ 3 = urgent, Score ≥ 1 = batch, else ignore
4. **Auto-rule creation** — First classification for a source saves its level as a persistent rule

---

## Data Storage

All state stored in `memory/notification-triage/`:

| File | Description |
|------|-------------|
| `batch.json` | Pending notification queue (capped at 1000) |
| `rules.json` | Per-source classification rules |
| `seen.json` | Set of seen notification IDs |
| `digest.json` | Digest entries awaiting batch ||

---

## Programmatic API

```javascript
const NT = require('./skills/notification-triage/notification-triage.js');

// Classify
const result = NT.classifyMessage('server down', 'monitor');
// { source: 'monitor', level: 'urgent', rule: 'auto', score: 2 }

// Add to batch
NT.addNotification('id-1', 'message', 'source', 'batch');

// Get pending
const pending = NT.getBatched(5);

// Flush
NT.flushBatch();

// Mark seen
NT.markSeen('id-1');
NT.markAllSeen();

// Rules
const rules = NT.loadRules();
NT.addRule('source', 'urgent|batch|ignore');
NT.removeRule('source');
NT.listRules();

// Status
NT.showStatus();

// Digest
NT.generateDigest('daily');
```

---

## Testing

```bash
# Run full test suite (24 tests)
node skills/notification-triage/tests/run-self-tests.js
```

Test coverage:
- Urgency classification (7 cases)
- Rule management (4 cases)
- Notification batching (4 cases)
- Seen tracking (2 cases)
- Status output (3 cases)
- Edge cases (4 cases)

---

## Security

| Protection | Status |
|------------|--------|
| **No shell execution** | ✅ Pure Node.js, no exec/system calls |
| **Input validation** | ✅ Messages truncated to 500 chars |
| **JSON-safe** | ✅ All persistence via JSON (no injection) |
| **No external deps** | ✅ Zero npm dependencies |

---

## License

MIT — Part of the OpenClaw skill ecosystem.

---

## Related Skills

- **Environment Manager** — Manage services that generate notifications
- **Smart Backup** — Backup notifications from cron
- **Research Assistant** — Knowledge base for notification trends
