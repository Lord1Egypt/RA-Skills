---
name: plaud
description: Use when working with Plaud recordings, including /plaud Telegram workflows, listing recent recordings, finding recordings by date or keyword, reading transcripts, summarizing notes, extracting action items, drafting follow-ups, exporting Plaud content, or diagnosing Plaud MCP/CLI authentication.
user-invocable: true
---

# Plaud

Use this skill for Plaud recording workflows in OpenClaw.

## Tool choice

Prefer the Plaud MCP tools when available:

- `plaud__list_files`: list or search recordings
- `plaud__get_file`: get metadata and availability for one recording
- `plaud__get_note`: fetch AI notes, summaries, topics, and action items
- `plaud__get_transcript`: fetch timestamped transcript with speakers
- `plaud__get_current_user`: check authentication
- `plaud__login`: start OAuth
- `plaud__logout`: disconnect

Use the Plaud CLI when:

- The user explicitly asks for terminal or CLI use
- MCP is unavailable or unauthenticated
- You need file export through shell redirection
- You need to inspect CLI install or auth state

CLI reference lives in `references/cli.md`. MCP reference lives in `references/mcp.md`.

## Telegram slash command

This skill supports a single Telegram command shape when the OpenClaw Telegram bot exposes `/plaud` as a custom command:

```text
/plaud [action] [target]
```

Actions:

- `/plaud`: show compact help plus the latest 3 recordings
- `/plaud recent`: list recent recordings
- `/plaud last`: show the latest meaningful recording, skipping tiny accidental clips under 30 seconds when possible
- `/plaud find <query>`: search by title, keyword, or date
- `/plaud summary [target]`: summarize a recording, defaulting to last meaningful recording
- `/plaud actions [target]`: extract action items, owners, dates, and open loops
- `/plaud transcript [target]`: fetch transcript or explain if unavailable
- `/plaud export [target]`: export metadata, summary, and transcript using the CLI helper
- `/plaud status`: check MCP and CLI auth status
- `/plaud login`: start Plaud OAuth

If the user sends `/plaud <text>` and `<text>` is not a known action, treat it as `/plaud find <text>`.

Slash command registration can be handled by OpenClaw native skill commands when `commands.nativeSkills` is enabled. This skill declares `user-invocable: true`, so OpenClaw can expose `/plaud` without adding a separate Telegram `customCommands` entry. Do not replace existing custom commands such as `/commands` or `/menu` just to add this skill command.

## Standard workflows

### List recent recordings

1. Call `plaud__list_files` with `page: 1`, `page_size: 10`.
2. Show name, start time, duration, and ID.
3. If the user asks for "last recording", pick the first item returned unless they specify start time ordering.

### Summarize a recording

1. Resolve the recording ID from the user request.
2. Call `plaud__get_note` first.
3. If notes are empty, call `plaud__get_transcript`.
4. If both are empty, say no transcript or notes are available. Mention duration if known.
5. Include speakers only when speaker labels are present in transcript data.

### Find a recording

1. Use `plaud__list_files` with `query`, `date_from`, or `date_to` when provided.
2. If the request is vague, list the most likely matches and ask the user to choose.
3. Do not access unrelated recordings beyond what is needed to answer.

### Draft follow-up

1. Fetch notes first, transcript second.
2. Extract decisions, open questions, owners, and dates.
3. Draft clearly and label it as a draft. Do not send messages or emails unless the user explicitly asks and approves the final text.

### Export content

For simple exports, use the CLI:

```bash
plaud summary <id> -o summary.md
plaud transcript <id> -o transcript.txt
```

For repeatable Markdown export, use `scripts/plaud-export.js`.

## Authentication

Check auth with `plaud__get_current_user` or `plaud me`.

If unauthenticated:

1. Run `plaud__login` for MCP auth.
2. If CLI auth is needed, run `plaud login`.
3. If OAuth redirects to `localhost:8199`, ask the user to paste the callback URL and submit it to the local listener while it is still running.

## Privacy and safety

- Plaud recordings may contain private conversations. Access only the recording or date range needed for the task.
- Do not reveal transcript contents unless the user asked for that recording.
- Do not download audio unless needed.
- Do not send follow-ups externally without explicit approval.
