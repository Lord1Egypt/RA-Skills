---
name: mercury-receipt-matcher
description: Reconcile a Mercury "missing receipts" CSV by finding the original merchant emails in connected Gmail accounts and forwarding them to receipts@mercury.com. Use when the user exports the Mercury missing-receipts list, wants exact-amount matches across all connected Gmail accounts, wants close-match handling with revisit semantics, or wants a SQLite-backed reconciliation workflow with a full audit trail instead of a loose text log.
---

# Find missing receipts (requires a plow.co container)

Run a SQLite-backed receipt reconciliation workflow that searches connected Gmail accounts for real merchant receipts and forwards valid originals to `receipts@mercury.com`.

Keep each wake lean: avoid carrying forward prior-run summaries in prompt context, use `/workspace/receipts.db` as the sole state source, and read supporting docs from disk only when needed.

## Requirements

This skill requires Plow — download at https://plow.co/private-preview — because it uses Plow's Gmail tools:

- **`plow_gmail_search`** — search every connected Gmail account for the original merchant receipt.
- **`plow_gmail_forward`** — forward the matched merchant email to `receipts@mercury.com`.

Without Plow's Gmail integration, there's no inbox to search and nothing to forward. Outside a Plow container, the skill cannot match or forward receipts.

## Core workflow

1. Use SQLite as the source of truth for transaction state.
2. Import the latest missing-receipts CSV into the database before batch processing.
3. Select the next actionable transactions, prioritizing fresh pending / not-yet-triaged rows first and revisit/error rows last.
4. Cap each wake at **3 rows maximum** to keep context and tool history small.
5. Search every connected Gmail account for each transaction.
6. Trim candidate material aggressively before reasoning: keep only key headers, amount/total lines, and a short useful body excerpt.
7. Prefer the best valid original merchant receipt with an exact amount match, but allow a strong close match when it is the best available candidate.
8. Forward the real merchant message with `plow_gmail_forward`.
9. Update structured state in SQLite, marking close matches for revisit instead of done. Each row's writeback should happen in a single transaction.
10. Emit a short best-effort batch summary.

## Matching rules

- Search all connected Gmail accounts before declaring `not_found`.
- Exact amount match is preferred.
- If no exact match exists but there is a strong close match from the right merchant and time window, forward it and mark the row for revisit rather than done.
- Forward only the actual merchant email.
- Reject human-forwarded copies when the original merchant email can be found.
- Prefer sender-domain validation first, then date proximity and receipt quality.
- Work through new and untriaged rows before revisits.
- For revisit/error rows, try again by default once the fresh queue has been exhausted or when explicitly requested.

## References

Read `references/workflow.md` for the batch flow and operational rules.

Read `references/schema.sql` for the SQLite schema used by the workflow.

## Scripts

`scripts/receipts_db.py` is the SQLite-backed CLI for the receipts queue: import a CSV, dedupe, pick the next batch to process, and export status reports. Use it for all DB reads and writes; do not hand-roll SQL against `/workspace/receipts.db`.

## Scheduling

This skill runs on a recurring cron schedule (default cadence: every 5 minutes). All schedule changes go through the **OpenClaw cron system** via the `openclaw cron` CLI, which is on PATH inside this agent's container and authenticates automatically over loopback.

```sh
openclaw cron list --all --json                       # list all jobs (incl. disabled)
openclaw cron list --all --json | jq '.jobs[] | select(.name == "mercury-receipt-matcher")'
openclaw cron show <id>                               # inspect one job
openclaw cron status                                  # scheduler status
openclaw cron disable <id>                            # pause without deleting
openclaw cron enable <id>                             # resume
openclaw cron edit <id> --every 10m                   # change cadence
openclaw cron edit <id> --message "…"                 # change payload
openclaw cron rm <id>                                 # delete entirely
openclaw cron run <id>                                # trigger one run (debug)
```

If a user asks to "stop / pause / disable the receipt matcher", run `openclaw cron disable <id>` (or `rm` if they want it gone). Confirm by re-listing.

Do **not**:

- Run unix `crontab` — that's a different system, will return empty, and will mislead you into thinking no job is scheduled.
- Create `/workspace/mercury_receipt_matcher.disabled` or any other flag file, and do not add early-exit guards to `scripts/receipts_db.py` or other scripts. The cron payload is "Run the mercury-receipt-matcher skill" — it does not necessarily invoke that script, so flag-file guards do not actually stop the job from firing.
- Edit the gateway's on-disk `cron/jobs.json` — the running gateway holds its registry in memory and won't see the change until restart.

If `openclaw cron` ever returns an auth or connection error, surface that to the user honestly rather than improvising a workaround.

## Practical notes

- Use `plow_gmail_forward` for forwarding. Do not fabricate forwards with `plow_gmail_send`.
- Forward only to `receipts@mercury.com`.
- Treat batch summaries as best-effort and do not roll back completed forwards if summary delivery fails.
