---
name: pending-action-template
---

# <ACT-YYYYMMDD-NNN>

## Meta
- ID:      ACT-YYYYMMDD-NNN
- Type:    patch | config-change | service | user | firewall | other
- Status:  pending | approved | denied | skipped | expired
- Queued:  YYYY-MM-DD HH:MM IST
- Expires: YYYY-MM-DD (7 days from queue)

## Finding That Triggered This
- Finding file: audit/results/<severity>/YYYY-MM-DD-<slug>.md
- Summary: [one line what was found]
- Severity: CRITICAL | HIGH | MEDIUM

## Proposed Action
```bash
# Exact command(s) to execute:
<command>
```

## What This Does
[Plain English — what will change on the server]

## Risk of Doing This
[What could go wrong]

## Risk of NOT Doing This
[What could happen if left unfixed]

## Rollback
```bash
# Exact command to undo:
<rollback-command>
```

## Reply Options
- `APPROVE ACT-YYYYMMDD-NNN` → execute now
- `DENY ACT-YYYYMMDD-NNN` → skip permanently
- `SKIP ACT-YYYYMMDD-NNN` → defer 7 days
