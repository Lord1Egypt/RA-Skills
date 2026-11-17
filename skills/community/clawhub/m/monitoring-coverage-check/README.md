# Monitoring Coverage Check

An OpenClaw skill for answering two questions: is everything that matters watched, and does
the alert really arrive?

- **Compares** the owner's services, hosts, timed jobs, and backups with the monitors and
  checks that exist, and lists the gaps by type: not watched, watched but silent, paused
  without reason, port instead of function, failure covered but absence not, timing mismatch,
  double watch, watcher unwatched, route untested, expiry blind, version drift.
- **Checks dead man's switches** for timed jobs and backups: start, success, and failure
  signals, period matching the job, grace longer than the longest run.
- **Proves alert routes** with a test the owner approves, one test at a time, and records the
  evidence (time sent, channel, who confirmed arrival).
- **Reports versions** of the monitoring tools and their agents against the newest stable
  release.
- **Reads and proposes.** Changes to monitors, checks, routes, or tools happen only as single
  steps the owner approved. Push URLs, ping URLs, webhooks, and keys never appear in reports.

Works with no API access (the owner pastes lists and screenshots). Optional sections for
Uptime Kuma, Beszel, and healthchecks.io apply only when the owner uses them.

Everything is in the skill file itself. Commands tested read-only against a live Uptime Kuma
2.5, Beszel 0.21, and healthchecks.io setup, November 2026.
