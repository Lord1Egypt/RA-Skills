# Digest Template

Use this structure for weekly or daily relationship digests. Default: this week, both streams, top 5 recommendations with pagination.

## Relationship Digest — {scope} ({date range})

**Stream**: {Work / Personal / Both}
**Sources checked**: {what context was available}
**Opportunities found**: {total count}
**Showing**: {X} of {total}

---

### Work

{Top recommendations for work contacts, ranked by composite score.}

#### {Name}

- **Stream**: {Work / Personal}
- **Signal**: {trigger}
- **Why now**: {timing + appropriateness + channel fit — answer all three}
- **Score**: {composite} — {High / Medium / Low} evidence ({source})
- **Channel**: {email / LinkedIn / Slack}
- **Language**: {drafting language} (detected from {history / profile / field / default})
- **Tone**: {from tone framework}
- **Draft**: > {1-3 sentences in the contact's language}
- **Action**: Approve to send / Edit / Snooze / Skip

---

### Personal

{Same format, personal contacts ranked by composite score.}

---

### Watching

{Signals scoring 3.2–4.1 in compact form:}

| Person | Signal | Evidence | Score | Suggested action |
|--------|--------|----------|-------|------------------|
| {name} | {signal} | {level} | {score} | {action} |

---

**Summary**: {X} recommended now, {Y} watching, {Z} below threshold.

These are drafts — nothing has been sent. Showing {X} of {N} opportunities. Say "next" for more, or tell me which to finalize.
