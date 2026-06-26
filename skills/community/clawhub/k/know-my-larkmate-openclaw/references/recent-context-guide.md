# Recent Context Guide

Use this reference when the task requires reading Lark activity and turning it into a recent-context snapshot for `memory/YYYY-MM-DD.md`.

This skill writes heartbeat-sized context updates into daily notes and leaves long-term promotion to OpenClaw.

## What To Look For

Capture changes that should affect the next few turns:
- active workstreams
- recent decisions
- blockers
- likely next asks
- newly important collaborators
- near-term preferences that change how the agent should work

Skip items that are unlikely to matter soon:
- pure system noise
- repeated auth prompts
- bot cards with no immediate meaning
- one-off trivia
- speculative judgments about the user

## Output Format

Append a compact block in this shape:

```markdown
# [Analysis Title: concrete and time-scoped, e.g. Heartbeat Context Sync - 2026-04-14 10:00]

## Executive summary
[One short paragraph on what changed and why it matters next]

## Key findings
- Finding 1 with enough source detail to trace the claim
- Finding 2 with enough source detail to trace the claim

## Related Activities
1. Supporting chat, meeting, doc, minute, or task
```

Example:

```markdown
# Heartbeat Context Sync - 2026-04-14 10:00

## Executive summary
The user is currently focused on making the OpenClaw skill self-contained and making heartbeat memory updates more reliable for recent context. The immediate implementation boundary is to keep writing high-signal recent context into daily notes and avoid introducing a competing long-term promotion flow.

## Key findings
- The user wants the skill to prioritize recent-context sync into `memory/YYYY-MM-DD.md` rather than managing its own long-term memory layer.
- The skill package should be self-contained and avoid references to legacy materials outside the skill directory.

## Related Activities
1. Revised the skill to remove legacy reference dependencies.
2. Renamed the skill to `know-my-larkmate-openclaw` for packaging safety.
```

## Lark Read Shortcuts

Common read entrypoints:

```bash
lark-cli im +messages-search --start "<ISO-8601>" --page-size 50 --page-all --format json --as user
lark-cli calendar +agenda --start "<ISO-8601>" --end "<ISO-8601>" --format pretty --as user
lark-cli vc +search --start "<ISO-8601>" --page-size 20 --format pretty --as user
lark-cli minutes +search --page-size 20 --format json --as user
lark-cli docs +search --query "<keyword>" --page-size 20 --format json --as user
lark-cli docs +fetch --doc "<doc-token-or-url>" --format json --as user
```

## Read Bounds And Filtering

Use bounded reads by default so heartbeat stays cheap and frequent:
- Messages: last 72 hours, `--page-size 50`, use `--page-all` only when volume is still manageable.
- Calendar and VC: last 7 days.
- Docs and wiki: search first, then deep-read at most 3 high-signal items.
- Minutes: read title or summary first, fetch detailed AI outputs only when clearly relevant.

Prefer these filters before writing memory:
- Group messages by chat or thread before concluding something is a recurring theme.
- Prefer recency plus repetition over volume.
- Treat a single meeting title or doc title as context only, not a stable fact.
- When blocked by permissions or missing tools, record the blockage as a finding instead of inferring around it.
- When blocked by permissions, request only the missing read-only scope(s), rerun the failed read, then continue.

When data is too large:
- Truncate oldest material first.
- Preserve the newest artifacts tied to current workstreams.
- Keep enough source detail to trace each finding back to a specific artifact.
