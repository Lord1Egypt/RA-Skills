# Lucid Platform Notes

## Cron Context Constraints

- **`execute_code` is blocked in cron jobs**. Journal discovery must use `terminal(find ...)` with shell filters (`-newermt`, `-name`, `-type f`) instead of `execute_code` with `os.walk`. See `gotchas.md` for the exact `find` patterns.
- **`memory` tool may be unavailable in cron context**. If memory writes fail, skip them — the skill's own data files (ingestion_log, decisions, evidence, config) are the durable store. Memory is a convenience layer, not required for correct operation.
- Cron sessions have a lighter toolset than interactive sessions. Always check for tool availability before assuming a tool exists.

## Iteration Budget

The 40-journal-per-run cap and incremental cursor keep turn count well within the default iteration budget. Each filing cycle (read journal → check duplicate → file → advance cursor) resets the activity-based timeout in Hermes v0.8+, so long runs complete naturally without inactivity timeouts.

## Cron Configuration

Cron runs use isolated session, light context. Operators with high journal volume (many active skills) may benefit from raising `max_turns` to 150 in their agent config.

## Heartbeat

No heartbeat entry. Lucid needs one substantial batch run per day, not lightweight polling.

## Mid-Run Termination Safety

If a session terminates mid-run, no filed work is lost. The cursor advances after each successful filing. The next run picks up from the first unprocessed journal.