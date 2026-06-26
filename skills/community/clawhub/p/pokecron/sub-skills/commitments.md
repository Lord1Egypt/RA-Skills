# Commitments

Inferred follow-up promises. "I'll check on that tomorrow" → auto-scheduled
commitment. Due commitments are automatically injected into agent task
prompts at fire time via `buildCommitmentContextForPrompt`, so the agent's
future self sees what its past self promised.

## Create

```bash
poke --commit "Follow up on PR review" --due 2h \
  --channel CH --target TGT
```

- `--commit "reason"` — what was promised, in user-facing language.
- `--due DUR` — when it's due (e.g. `30m`, `2h`, `1d`). Default `1d`.
- `--kind TYPE` — categorization. One of `event_check_in`,
  `deadline_check`, `care_check_in`, `open_loop` (default `open_loop`).
- `--sensitivity LVL` — one of `routine` (default), `personal`, `care`.
- `--agent AG` — agent to attribute (optional; useful for tracking
  which voice made the promise).

## List

```bash
poke --commitments
# === Commitments (2 pending, 1 due) ===
#   [DUE] open_loop · Follow up on PR review · due 2026-…
#   [...] care_check_in · Check on Alice · due 2026-…
```

`[DUE]` means inside the due window (now ≥ `dueWindow.earliestMs`).

## Resolve

```bash
poke --commit-done cm-20260510-192219-f41b6e4e
poke --commit-cancel cm-20260510-192219-f41b6e4e
```

Resolved commitments are kept in the store with `status=completed` /
`cancelled` for audit; they just stop appearing in `--commitments`.

## Auto-injection into agent prompts

When a `--task` reminder fires, due commitments matching the same
`(agent, channel, target)` scope get appended to the task prompt as a
context block. The agent sees them as part of its instructions and can
act ("I notice I promised to check on the PR review — let me do that
now").

Use this for: recurring "sweep the morning" or "afternoon check" agents
that should naturally pick up open commitments without you having to
schedule each one individually.

## Schema (informational)

Stored in `.runtime/state/commitments.json`. Per-commitment:

- `id` — `cm-YYYYMMDD-HHMMSS-<rand>`
- `reason` / `suggestedText`
- `agent` / `channel` / `target` — scope for matching against task fires
- `kind` / `sensitivity` / `source` (currently always `agent_promise`)
- `status` — `pending` / `completed` / `cancelled`
- `dueWindow.earliestMs` / `latestMs` (latest = earliest + 1h)
- `confidence` (currently always 0.8 for explicit `--commit`)
- `dedupeKey` — hash of `(channel, target, reason)`, blocks dupes
- `createdAtMs` / `updatedAtMs` / `attempts`

## Anti-pattern

Don't use `--commit` for things that need a specific fire time — that's
what `--remind`/`--task` with `--at` is for. Commitments are vaguer
("sometime tomorrow", "this week") and depend on a recurring task
catching them in its scope. If the user said "remind me at 3pm to call
mom", that's a reminder, not a commitment.
