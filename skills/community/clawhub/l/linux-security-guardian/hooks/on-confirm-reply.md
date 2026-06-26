---
name: linux-security-guardian-on-confirm-reply
description: Processes owner APPROVE/DENY/SKIP replies for pending confirmation actions.
---

# On-Confirm-Reply Hook

## Trigger
Owner message contains: APPROVE <ID> / DENY <ID> / SKIP <ID>

## Parse Reply
```
Extract: action = APPROVE/DENY/SKIP
Extract: ID = ACT-YYYYMMDD-NNN, FW-YYYYMMDD-NNN, or <client>-<server>-<type>-<id>

ID format: <client>-<server>-<type>-<NNN>
Example: client-1-server-01-ACT-20260529-001

Search: actions/<client>/<server>/pending-confirm/<ID>-*.md
If not found → search all pending-confirm across all clients/servers
  → Still not found? "Action ID <ID> not found. Use STATUS to see all pending."
```

## On APPROVE
```
1. Read the full action spec from pending-confirm file (includes client + server)
2. Confirm safety: run pre-action.md checks with client/server context
3. Execute the action via SSH MCP (connect to the server from the action file)
4. Run post-action.md verification
5. Move file: actions/<client>/<server>/pending-confirm/ → actions/<client>/<server>/history/
6. Reply: "✓ Action <ID> executed on <client>/<server>: <what was done> | Result: <success/fail>"
7. Update soul [PENDING CONFIRMATIONS] — remove entry
```

## On DENY
```
1. Move file to actions/<client>/<server>/history/ with status: denied
2. Note in AUDIT_LOG.md: "<ID> denied by owner YYYY-MM-DD"
3. Reply: "Action <ID> denied and logged for <client>/<server>."
4. Update soul — remove from pending
```

## On SKIP
```
1. Keep file in actions/<client>/<server>/pending-confirm/ with status: skipped + date
2. Note expiry: skip is valid for 7 days, then re-queues
3. Reply: "Action <ID> skipped. Will re-appear in next audit if finding persists."
```

## Bulk Operations
Owner can send: "APPROVE ALL" → approve all pending (with safety checks on each)
Owner can send: "STATUS" → list all pending confirmations with descriptions
