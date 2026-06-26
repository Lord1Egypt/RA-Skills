# Lessons Learned in Production

Real failure modes encountered and their fixes.

## Cron Delivery

**Problem:** Cron runs successfully but notifications never reach Telegram.
**Symptom:** `lastDelivered: false`, `lastDeliveryStatus: "not-delivered"` on every run.
**Cause:** `--channel last` doesn't resolve in isolated sessions — no "last" channel exists.
**Fix:** Use `--to <explicit-telegram-chat-id>` when creating/editing the cron.
**Note:** `lastDelivered: false` on empty-inbox runs is EXPECTED (HEARTBEAT_OK is intentionally silent).

## Cron Timeouts

**Problem:** Cron errors out on every run with `consecutiveErrors: 5+`.
**Symptom:** `lastError: "cron: job execution timed out"`, `lastDurationMs` equals your timeout exactly.
**Cause:** Cron prompt instructs it to wait for subagents to complete, which takes 10-30+ minutes.
**Fix:** Fire-and-forget design — spawn subagents without waiting, exit immediately. 120s timeout is sufficient.

## Error Backoff

**Problem:** After fixing a cron issue, it doesn't run for 30-60 minutes.
**Cause:** Exponential backoff after consecutive errors. Edit doesn't reset error count.
**Fix:** Delete and recreate: `openclaw cron delete <id> && openclaw cron add ...`

## Subagent Notification Failure

**Problem:** Subagent completes and opens PR, but no Telegram notification arrives.
**Cause:** Subagents spawned from isolated cron sessions can't reliably use sessions_send to reach the main session.
**Fix:** Have the cron itself announce dispatches in its own reply (before spawning). The cron reply is what reliably delivers to Telegram. Subagent notification is best-effort bonus.

## Missed Tickets (Email Loss)

**Problem:** TinyDesk creates the GitHub issue and assigns it, but the assignment email is never received.
**Cause:** Email delivery is a single point of failure.
**Fix:** Add GitHub poll as safety net in the cron — `GET /search/issues?q=assignee:<bot>+state:open` every 15min. Cross-check against support-tickets.json + existing comments + existing PRs to avoid re-dispatching.

## ACP Spawn Failures

**Problem:** `sessions_spawn` with `runtime: "acp"` fails with "unknown option '--format'".
**Cause:** acpx plugin passes `--format` flag; older Claude Code versions use `--output-format`.
**Fix:** Spawn a subagent (`runtime: "subagent"`) that runs `claude -p --dangerously-skip-permissions --output-format text "..."` via exec instead of using ACP directly.

## Heartbeat vs Cron Confusion

**Problem:** Email checks appear to work (logs show activity) but tickets are missed.
**Cause:** Heartbeat (main session) was doing email checks sporadically; the isolated cron job was either broken or never running.
**Diagnosis:** Check `openclaw cron list --json` — if `lastRunAtMs: null` or `consecutiveErrors > 0`, the cron is the problem.
**Fix:** Separate concerns cleanly: heartbeat handles main-session tasks only, cron handles email + GitHub polling.

## Duplicate Dispatch

**Problem:** Same ticket dispatched multiple times.
**Cause:** GitHub poll marks a ticket as unactioned if the comment or PR check doesn't match exactly.
**Fix:** Add `issue_url` to support-tickets.json immediately on dispatch (before subagent runs). Check this file first in the GitHub poll before checking comments/PRs.
