# Notification Templates v2.1

> Note: v2.1 uses file-based notifications only. No external messaging (Feishu, Slack, etc.).
> Check `pending-review.json` for pending items, or run `auto-evolve.py log`.

---

## Iteration Log Entry

```
## Iteration {version}

Date: {date} UTC
Status: {status}
Mode: {mode}
Risk Level: {risk_level}

Changes detected: {n}
Optimizations found: {n}
Pending review: {n}
Duration: {duration}s
Alert: {has_alert}
```

---

## Execution Preview

```
⚠️  {Mode} Mode: About to execute {n} change(s):
  [1] {color} {risk} {description}
  [2] {color} {risk} {description}
  ...

Semi-auto: run `auto-evolve.py confirm` to apply.
Full-auto: executing per rules.
```

---

## Pending Approval Notice

```
📋 Pending Approval — Iteration {version}

{mode}: {count} items need review:

[1] {risk} {description}
    File: {file_path}
    Category: {category}

[2] {risk} {description}
    ...

---
Semi-auto confirm with:
  auto-evolve.py confirm
  auto-evolve.py confirm --iteration {version}

Approve specific items:
  auto-evolve.py approve 1,3

Reject an item:
  auto-evolve.py reject 2 --reason "too risky"
```

---

## Confirmation (Semi-Auto)

```
✅ Confirmed {count} items from iteration {version}

Committed and pushed.
Recorded in .learnings/approvals.json
```

---

## Rejection Confirmation

```
❌ Rejected item {id}: {description}

Reason: {reason}
Recorded in .learnings/rejections.json

This change will not be re-recommended.
```

---

## Approval Confirmation

```
✅ Approved {count} items from iteration {version}

Committed and pushed.
Recorded in .learnings/approvals.json
```

---

## Rollback Confirmation

```
🔄 Rollback Complete — {rollback_version}

Rolled back: {target_version}
Reason: {reason}
Reverted items: {count}

---
To undo this rollback, run:
  git revert {new_commit_hash}
```

---

## Learning History Entry (Rejection)

```json
{
  "id": "{hash}",
  "type": "rejection",
  "change_id": "{id}",
  "description": "{description}",
  "reason": "{reason}",
  "date": "{date}",
  "repo": "{repo_path}"
}
```

---

## Learning History Entry (Approval)

```json
{
  "id": "{hash}",
  "type": "approval",
  "change_id": "{id}",
  "description": "{description}",
  "reason": null,
  "date": "{date}",
  "repo": "{repo_path}"
}
```

---

## Alert (Quality Gate Failure)

```json
{
  "iteration_id": "{version}",
  "date": "{date}",
  "alert_type": "quality_gate_failed",
  "message": "Syntax errors detected in repository",
  "details": {
    "errors": ["path/to/file1.py", "path/to/file2.py"]
  }
}
```

---

## Closed Repository Sanitization Notice

```
🔒 Closed Repository: {repo_path}

pending-review.json has been sanitized:
- File paths replaced with [REDACTED]
- Content hashes used for reference
- No code content in logs

Manual review required for this repository.
```

---

## Scan Complete (Dry Run)

```
🔍 Scan Complete (dry-run)

Mode: {mode}
Changes found: {n}
Optimizations: {n}
Low risk: {n}
Medium risk: {n}
High risk: {n}
Pending: {n}

No changes committed.
Run without --dry-run to apply.
```

---

## Schedule Setup Instructions

```
# Set scan interval (hours)
auto-evolve.py schedule --every 168   # weekly
auto-evolve.py schedule --every 24    # daily

# To activate, create an OpenClaw cron job:
openclaw cron add --name auto-evolve-scan \
  --command 'python3 ~/.openclaw/workspace/skills/auto-evolve/scripts/auto-evolve.py scan' \
  --interval 168h
```

---

## Error Notification

```
❌ Auto-Evolve Error

Command: {command}
Error: {error_message}

Iteration {version} logged.
Manual intervention may be required.
```
