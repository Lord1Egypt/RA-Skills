# Plaud Workflow Patterns

## Telegram `/plaud` router

Use one command with sub-actions:

```text
/plaud [action] [target]
```

Routing rules:

- Empty action: show help plus latest 3 recordings.
- Unknown action: treat the full text after `/plaud` as a search query.
- Missing target for `summary`, `actions`, `transcript`, or `export`: use the latest meaningful recording.
- Latest meaningful recording: prefer the newest item over 30 seconds when possible, so accidental tiny clips are skipped.

V1 actions:

- `recent`
- `last`
- `find`
- `summary`
- `actions`
- `transcript`
- `export`
- `status`
- `login`

## Meeting digest

Input: recording ID or search criteria.

Output structure:

1. Executive summary
2. Topics discussed
3. Decisions
4. Action items with owners and dates
5. Open questions
6. Speaker list, if available

## Follow-up email draft

Use this structure:

```text
Subject: Follow-up from [meeting]

Hi [name],

Thanks for the conversation today. My takeaways:

- [takeaway]
- [decision]
- [open item]

Next steps:

- [owner] to [action] by [date]

Best,
[Sender]
```

Do not send externally without approval.

## Recording search strategy

- Exact title or keyword: use `query` or `plaud search`.
- Date-bound request: use `date_from` and `date_to`.
- "Last recording": use first item from recent list, then verify duration and title.
- Ambiguous match: show top candidates instead of guessing.

## Export package

When the user asks to save a recording package, create a folder with:

- `summary.md`
- `transcript.txt`
- `metadata.json`

Use safe filenames based on recording name and date.
