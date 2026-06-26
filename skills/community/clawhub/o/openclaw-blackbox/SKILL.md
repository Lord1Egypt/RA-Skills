---
name: openclaw-blackbox
description: OpenClaw Blackbox CLI — inspect failed, stalled, expensive, or weird OpenClaw agent runs from local disk evidence; list sessions and failures; find the session behind a request; and generate terminal, Markdown, JSON, or HTML reports. Use when debugging OpenClaw cron runs, session failures, context overflows, missing transcripts/trajectories, message delivery issues, or when an agent needs deterministic run inspection without hidden LLM calls.
clawhubUrl: https://clawhub.ai/shan8851/openclaw-blackbox
homepage: https://github.com/shan8851/openclaw-blackbox
metadata:
  {
    "openclaw":
      {
        "emoji": "🕵️",
        "requires": { "bins": ["blackbox"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@shan8851/blackbox",
              "bins": ["blackbox"],
              "label": "Install OpenClaw Blackbox (npm)",
            },
          ],
      },
  }
---

# OpenClaw Blackbox

Use `blackbox` to inspect local OpenClaw run evidence and produce deterministic debugging reports.

Setup

- `npm install -g @shan8851/blackbox`
- Requires local OpenClaw state; by default it reads `~/.openclaw`
- To inspect another OpenClaw home: `OPENCLAW_HOME=/path/to/.openclaw blackbox doctor`

Health Check

- Check visible OpenClaw evidence: `blackbox doctor`
- JSON health check: `blackbox doctor --json`

List Evidence

- Recent failed or suspicious cron runs: `blackbox list failures --limit 10`
- Filter by label: `blackbox list failures --label context_overflow`
- Emit runnable inspect commands: `blackbox list failures --commands`
- Local sessions across agents: `blackbox list sessions --agent all --limit 20`
- Sessions with specific evidence: `blackbox list sessions --evidence checkpoint_present`

Inspect Runs

- Latest failed run for a cron job: `blackbox inspect --cron-job "Example nightly job" --latest-error`
- Known session: `blackbox inspect --session-id <session-id>`
- Full Markdown report: `blackbox inspect --session-id <session-id> --view full --out reports/run.md`
- JSON report: `blackbox inspect --session-id <session-id> --json-out reports/run.json`
- HTML report: `blackbox inspect --session-id <session-id> --html-out reports/run.html --open`

Find Requests

- Find the session behind a user request: `blackbox find request --query "summarise the failed run" --agent all`
- Find by message id: `blackbox find request --message-id <message-id> --agent main`
- Emit inspect commands only: `blackbox find request --query "failed to send" --commands`

Output

- `inspect` always prints a terminal snapshot
- Markdown defaults to `reports/<run>.md` unless `--out` is set
- Set `BLACKBOX_REPORT_DIR` to change the default report directory
- Discovery commands support `--json` for machine-readable output
- `--view simple` is the default triage report; `--view full` includes fuller evidence and timeline details

Agent Notes

- Prefer Blackbox before guessing why an OpenClaw run failed if local evidence exists
- `find request` / `inspect --query` are conservative; if a query maps to multiple sessions, inspect by explicit `--session-id`
- Reports can include prompts, tool arguments/results, URLs, and local paths; review before sharing externally
- Blackbox is disk-first and should not make hidden LLM calls by default
- Failure labels include `context_overflow`, `message_delivery_failed`, `timeout`, `session_lock_timeout`, `gateway_restart_interrupted`, model/auth labels, tool failure labels, and `unknown_error`
- Evidence labels include `missing_transcript`, `transcript_deleted`, `transcript_reset`, `missing_trajectory`, `checkpoint_present`, and `session_write_in_progress`

Notes

- Exit codes: 0 success, 1 unexpected failure, 2 usage/invalid argument, 3 not found/missing OpenClaw state, 4 ambiguous request match
- Package name: `@shan8851/blackbox`; binary name: `blackbox`; skill/ClawHub slug: `openclaw-blackbox`
