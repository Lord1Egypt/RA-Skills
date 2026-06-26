---
name: hardcover-bookshelf
version: 0.1.0
description: >-
  Talk to a user's Hardcover bookshelf via the Hardcover GraphQL API.
  Use when the user wants to manage reading activity in natural language:
  start a book, finish a book, view the Want to Read shelf, or compute
  yearly reading stats such as "how many books did I read last year?".
  Require HARDCOVER_TOKEN before any API call, using the exact `Bearer ...`
  value copied from Hardcover account API settings. Use this skill whenever
  the user mentions Hardcover, reading lists, bookshelves, tracking books,
  or anything related to managing what they're reading.
metadata:
  openclaw:
    primaryEnv: HARDCOVER_TOKEN
    requires:
      env:
        - HARDCOVER_TOKEN
      bins:
        - node
        - npx
    install:
      - kind: node
---

# Hardcover Bookshelf

Use this skill to treat Hardcover as a conversational bookshelf assistant.

It is optimized for prompts like:
- `what's on my reading list`
- `i started reading the complete maus`
- `i finished reading dune`
- `how many books did i read last year`

## Required Environment

Require `HARDCOVER_TOKEN` before making API calls.

**Token format is Option A:** the env var must contain the full Authorization header value exactly as copied from Hardcover, including the `Bearer ` prefix.

Example:

```bash
export HARDCOVER_TOKEN='Bearer eyJ...'
```

If missing or malformed, stop and ask the user to set it correctly.

## Commands

Run these from the skill's root directory. Pass `--json` for machine-readable output.

```bash
npx tsx src/cli.ts list [--limit 20] [--json]
npx tsx src/cli.ts start --title "The Complete Maus" [--json]
npx tsx src/cli.ts finish --title "The Complete Maus" [--json]
npx tsx src/cli.ts count-last-year [--json]
```

These commands call the local TypeScript client in `src/` and centralize auth, schema quirks, and error handling.

## Intent mapping

### "What's on my reading list?"

Interpret reading list as **Want to Read**.

Run:

```bash
npx tsx src/cli.ts list
```

Return a clean bullet list and mention the total shown.

### "I started reading <book>"

Run:

```bash
npx tsx src/cli.ts start --title "<book>"
```

Behavior:
- checks currently-reading shelf first for an exact normalized title match
- falls back to Hardcover search
- if ambiguous, the command returns numbered choices; ask the user to choose before mutating
- if already currently reading, it returns the existing entry instead of creating a duplicate

### "I finished reading <book>"

Run:

```bash
npx tsx src/cli.ts finish --title "<book>"
```

Behavior:
- resolves the title the same way as start-reading
- prefers an existing currently-reading entry for that book
- otherwise updates the most recent existing `user_book` for that book
- sets status to **Read** and uses `last_read_date` as the finish-date field

Note: this is a **best-effort** implementation based on the live schema tested so far. If Hardcover later exposes a better canonical finish-date field for user books, update the client and references.

### "How many books did I read last year?"

Run:

```bash
npx tsx src/cli.ts count-last-year
```

Behavior:
- computes the previous calendar year in UTC
- counts books with `status_id=3` and `last_read_date` inside that year
- returns the total plus a small verification sample

## Safety & ambiguity rules

- Never mutate when title resolution is ambiguous.
- If the command prints multiple choices, ask the user to choose.
- Prefer concise numbered disambiguation.
- Echo the final title and state change after successful writes.

## Files

- `src/client.ts` — Hardcover API client and common operations
- `src/cli.ts` — unified CLI entrypoint
- `references/schema-quirks.md` — live notes on auth, status IDs, and mutation/query quirks
