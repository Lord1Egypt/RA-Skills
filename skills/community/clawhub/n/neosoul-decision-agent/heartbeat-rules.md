# Heartbeat Rules

Use heartbeat to keep `~/decision-making/` organized, prompt pending retrospectives, and surface aging decisions — without creating churn or losing data.

## Source of Truth

Keep the workspace `HEARTBEAT.md` snippet minimal.
Treat this file as the stable contract for decision-making heartbeat behavior.
Store mutable run state only in `~/decision-making/heartbeat-state.md`.

## Start of Every Heartbeat

1. Ensure `~/decision-making/heartbeat-state.md` exists.
2. Write `last_heartbeat_started_at` immediately in ISO 8601.
3. Read the previous `last_reviewed_decision_at`.
4. Scan `~/decision-making/` for files changed after that moment, excluding `heartbeat-state.md` itself.
5. Scan `~/decision-making/decisions/` for records with status `⏳ pending outcome` that are > 30 days old.

## If Nothing Changed and No Pending Retrospectives

- Set `last_heartbeat_result: HEARTBEAT_OK`
- Append a short "no material change" note
- Return `HEARTBEAT_OK`

## If Something Changed

Only do conservative organization:

- Refresh `index.md` if counts or file references drift
- Compact oversized files by merging duplicates or summarizing repetitive entries
- Move clearly misplaced notes to the right namespace only when the target is unambiguous
- Preserve confirmed rules, risk profile, and explicit domain weights exactly
- Update `last_reviewed_decision_at` only after the review finishes cleanly

## Retrospective Prompts (Decision-Specific)

If any `decisions/*.md` file has `status: ⏳ pending outcome` and was created > 30 days ago:

1. List those decisions in `heartbeat-state.md` under `pending_retrospectives`
2. On next session start, surface this prompt:
   ```
   "📋 A few decisions are waiting for retrospectives:
    - [slug] (made on [date])
    Would you like to log outcomes now? A quick retrospective can sharpen future [domain] decisions."
   ```
3. Do NOT auto-fill outcomes — wait for user input

## If Patterns Are Stale (90-day check)

- Scan `domains/*.md` and `types/*.md` for entries not referenced in 90 days
- Move stale entries to `archive/` with a dated archive block
- Log in heartbeat-state.md: `archived: {file}: {entry_summary} — unused 90 days`
- Do NOT delete — archive only

## Safety Rules

- Most heartbeat runs should do nothing
- Prefer append, summarize, or index fixes over large rewrites
- Never delete data, empty files, or overwrite uncertain text
- Never reorganize files outside `~/decision-making/`
- If scope is ambiguous, leave files untouched and record a suggested follow-up instead
- Never auto-complete retrospectives — only prompt, never fill

## State Fields

Keep `~/decision-making/heartbeat-state.md` simple:

- `last_heartbeat_started_at`
- `last_reviewed_decision_at`
- `last_heartbeat_result`
- `pending_retrospectives` — list of decision slugs awaiting outcome
- `last_actions`

## Behavior Standard

Heartbeat exists to keep the memory system tidy and decisions accountable.
If no rule is clearly violated and no retrospective is pending, do nothing.
