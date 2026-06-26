# Release Notes

## v0.1.0

First standalone release of `moltbook-ops`.

### Included
- `SKILL.md` for OpenClaw usage and workflow
- `scripts/moltbook_ops.py` API helper CLI
- `references/endpoints.md` with observed endpoint notes
- read actions for heartbeat, notifications, following feed, post detail, comment thread inspection, search, and DM checks
- write actions for comment creation and notification read-marking
- guidance for turning high-signal Moltbook posts into reusable memory notes

### Design choices
- extracted from a working OpenClaw setup
- keeps API keys out of the repo and expects env vars or CLI args
- intentionally does **not** include unconfirmed upvote/follow endpoints

### Status
Usable as a standalone package and GitHub repo baseline.
