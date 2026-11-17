# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Before deploy

- `node --import tsx evals/contract.mjs` passes against the adapted graph: a `claudeCode` harness on
  an Anthropic connector, `commitments` writable, `gtm_activities` and `gtm_accounts` read-only, no connector action but
  Slack,
  `postMessage` with `channelId` locked, no Slack read, one cron, `TRACKER_TIMEZONE` in the
  repository env.
- `cargo-ai project check` prints `agent:commitment_tracker bound to <your repo>#<branch>` with no
  trailing subdirectory.
- `cargo-ai connection connector list` shows authorized GitHub, Slack and Anthropic
  connectors.
- `cadence/log/calls/` on the default branch holds at least one entry dated in the last 30 days with
  an unchecked action.
- `gtm_activities` is filled by something (a sync, a play, or seeded test rows), and `gtm_accounts` has a
  row per test account with an `owner_id`.
- The cron runs after call-capture's, and `TRACKER_TIMEZONE` names the team's day.

## First runs

Keep the Slack permalinks and the model rows as evidence.

- **Extract.** One row per unchecked action in the window, each quoted, with `promised_by`, a due
  date and `source_entry`. No row for a checked or STALE-CHECK action.
- **Re-run.** Sending the trigger text again the same morning adds no row and posts nothing.
- **Close.** Seed one `gtm_activities` row that plainly does one open promise and one unrelated row on
  the same account (`cargo-ai storage record create-bulk --model-uuid <gtm_activities uuid> --records
  '[{"data":{…}}]'`); the next run sets that commitment `done` with `gtm_activities:<id>` in
  `closed_evidence`, and the unrelated row closes nothing.
- **Post.** One message lists only open rows due today or earlier, grouped by owner, overdue first,
  with every source entry on the last line, and those rows carry today's `last_nudged_on`.
- **Theirs.** A customer's promise reads as a follow-up to chase.
- **Failed post.** With the bot removed from the channel, the run writes no `last_nudged_on`; after it
  is invited back, the next run posts.

## Isolation

- This is one root skill. Its supporting Markdown lives under `references/`, and no nested
  `SKILL.md` exists.
- No import leaves the folder.
- The run transcripts show no `git commit`, `git push` or pull request, no write to `gtm_activities` or `gtm_accounts`, and no Slack
  call other than `postMessage`.
