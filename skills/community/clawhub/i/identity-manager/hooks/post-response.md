---
name: identity-post-response-hook
description: Runs after every agent response. Verifies all ops completed, memory is valid, group entries are current, and soul was written for CRITICAL/HIGH events. Reports any gaps.
---

# Post-Response Hook

## When This Runs
AFTER delivering response. Before turn ends. Silent unless breach found.

---

## Verification Checklist

### Check 1 — Entries on Disk
For every slug in pre-hook `ops_queued`:
- [ ] `identity/<slug>/entry.md` exists
- [ ] File modified this turn

FAIL → log breach, append warning to response.

### Check 2 — Group Entries Current
For any group whose member was created/updated this turn:
- [ ] `identity/<group-slug>/entry.md` exists
- [ ] `members[]` list is current
- [ ] `pairwise_dynamics[]` is current if new member added

FAIL → repair group entry now. Log repair.

### Check 3 — AI Entries Complete
For any entry with `subtype: ai` created/updated this turn:
- [ ] `ai_context` block exists (may have `[pending]` fields)
- [ ] `sibling_ais` field updated if this AI is in a group with other AIs

FAIL → repair ai_context block. Log repair.

### Check 4 — _index.md Currency
- [ ] Every slug touched this turn in `_index.md`
- [ ] `Last updated` is today

FAIL → repair `_index.md` now. Log repair.

### Check 5 — Memory Sync
- [ ] `memory/identities.json` contains all slugs touched this turn
- [ ] JSON valid against `memory/schema.json`
- [ ] Root `updated` field is today

FAIL → repair + revalidate. Log repair.
Repair fails → log critical breach.

### Check 6 — Soul Write-Through
If CRITICAL or HIGH soul events fired this turn:
- [ ] `soul/identity_context.md` written
- [ ] CRITICAL in `[CRITICAL FLAGS]`
- [ ] HIGH in appropriate section (`[GROUPS]` / `[AI ENTITIES]` / `[ACTIVE ENTITIES]`)

FAIL → write soul now. Log delayed write.

### Check 7 — Open Questions Synced
For every entry touched this turn with open questions:
- [ ] Questions appear in `soul/identity_context.md` `[OPEN QUESTIONS]`

FAIL → sync now.

---

## Hook Log Entry

```json
{
  "ts": "YYYY-MM-DDTHH:MM:SSZ",
  "hook": "post-response",
  "checks_passed": 7,
  "checks_failed": 0,
  "repairs_made": [],
  "breaches": [],
  "soul_verified": true,
  "groups_verified": ["group-slug"],
  "ai_entries_verified": ["ai-slug"]
}
```

---

## Breach Report Format

```
[identity-manager] ⚠ Sync breach detected:
  - Check 5 failed: memory/identities.json schema validation error
  - Affected slugs: [slug]
  - Manual repair needed: re-run memory sync
```

Append to delivered response. Never swallow silently.
