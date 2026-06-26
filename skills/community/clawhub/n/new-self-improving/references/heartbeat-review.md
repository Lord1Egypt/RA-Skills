# Heartbeat Review Procedure

Run this during OpenClaw heartbeat cycles or manual review sessions.

## Review Steps

### 1. Check state

Read `.self-improving/heartbeat-state.md` to see when the last review ran.
Skip if last review was less than 24 hours ago (unless forced).

### 2. Scan raw learnings

Read `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`, and `.learnings/FEATURE_REQUESTS.md`.
Count pending entries.

### 3. Evaluate recurrence

For each pending entry:
- Search all `.learnings/` files for similar entries (by keyword, domain, or pattern).
- If a match exists: increment `Recurrence-Count` on the older entry, add `See Also` link.
- If `Recurrence-Count >= 3` and within a 30-day window: add to `REVIEW_QUEUE.md`.

### 4. Process review queue

For each item in `.learnings/REVIEW_QUEUE.md`:
- Determine promotion target (see promotion-rules.md).
- Write the promoted entry to the target file.
- Update the original entry: `Status: promoted`, `Promoted-To: <file>`.
- Remove from `REVIEW_QUEUE.md`.

### 5. Maintenance pass

- Check `.self-improving/HOT.md` line count. If > 80 lines: compact.
- Check `domains/` and `projects/` files. If any > 200 lines: compact.
- Scan HOT for entries not referenced in 30+ days: demote to WARM.
- Scan WARM for entries not referenced in 90+ days: archive to COLD.

### 6. Update state

Write to `.self-improving/heartbeat-state.md`:

```markdown
## Last Review
- **Date**: ISO-8601 timestamp
- **Pending learnings**: N
- **Promoted**: N
- **Demoted**: N
- **Archived**: N
- **Compacted**: yes | no
```

## Constraints

- Do not create new rules from silence or observation alone.
- Do not promote without evidence (explicit correction, repeated pattern, or self-reflection).
- Do not rewrite or delete `.self-improving/` files during heartbeat — only append, merge, or move.
- Do not run review if last review was < 24h ago unless user requests it.
- Keep the review fast: if > 50 pending items, process only the top 20 by recurrence.
