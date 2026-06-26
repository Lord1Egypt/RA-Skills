---
name: inbox-to-action-closer
description: Orchestration skill that processes raw work-item data from Slack, GitHub, calendar, Notion, Trello, and email — supplied by the caller or by other OpenClaw tools — and produces a single merged, prioritised action board with owners, due dates, reply drafts, and follow-up questions. Does not connect to external APIs directly; it normalises, deduplicates, scores, and renders data that is provided to it.
---

# Inbox-to-Action Closer

## Purpose

Process raw pending-work data from multiple sources, deduplicate and score the items, and present one unified action board. This skill does not fetch data from external APIs. It expects raw source data to be supplied by the caller, by other OpenClaw skills, or by tools that have already retrieved it. All output is draft-only until the user explicitly confirms a write action.

## Data Acquisition

This skill does not include API connectors or manage credentials. To use it:
- Supply raw JSON data from each source (Slack messages, GitHub PRs, calendar events, etc.)
- Use existing OpenClaw tools or installed skills that already connect to these services
- Or pipe output from CLI tools (gh, himalaya, slack-cli, etc.) into the normalisation pipeline

The skill handles everything after data retrieval: normalisation, deduplication, scoring, and rendering.

## Supported Source Formats

1. Slack — message and thread JSON (sender, channel, timestamp, participants, permalink)
2. GitHub — PR, issue, and review request JSON (assignee, title, state, URL)
3. Calendar — event JSON (summary, start/end times, attendees, location)
4. Notion — page or task JSON (title, status, assignee, due date, URL)
5. Trello — card JSON (name, list, members, due date, URL)
6. Email — message JSON (from, subject, date, flags, thread references)

## Execution Steps

1. Receive raw source data from the caller or upstream tools.
2. For each source, call the corresponding adapter via `normalize` (src/normalize.ts) to convert raw items into the normalised action-item schema defined in src/types.ts. If a source is missing, skip it cleanly.
3. Pass all normalised items through `dedupe` (src/dedupe.ts) to merge cross-source duplicates using conservative confidence-based matching.
4. Score every item using `score` (src/score.ts) to compute transparent urgency rankings.
5. Generate the final action board using `render` (src/render.ts) in both markdown and structured JSON formats.
6. The orchestration entrypoint is `index` (src/index.ts), which coordinates steps 1-5.

## Safety Rules

1. All output MUST be draft-only by default. NEVER auto-send messages, post comments, close issues, or perform any write action without explicit user confirmation.
2. NEVER auto-post to any source system. Generated reply drafts and suggested actions are proposals, not executions.
3. NEVER perform destructive actions such as deleting items, archiving threads, or dismissing notifications.
4. ALWAYS ask the user for explicit confirmation before executing any write action, including sending replies, posting comments, updating task statuses, or creating new items. This confirmation gate is mandatory and separate from the draft-only default.
5. If a source is unavailable, misconfigured, or returns an error, skip it cleanly and continue processing remaining sources. NEVER fail the entire run because one source is unreachable.
6. MUST NOT fabricate or hallucinate action items. Only surface items that exist in the source data.
7. MUST preserve the original source URL for every action item so the user can verify and act in context.
