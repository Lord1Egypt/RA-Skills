---
name: Xiaohongshu (RedNote) API
description: Search Xiaohongshu notes, inspect creator profiles, resolve share links, and drill into note comments, replies, and note detail endpoints through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu"}}
---

# Xiaohongshu (RedNote)

Use this skill for Xiaohongshu note discovery, creator benchmarking, comment mining, and RedNote share-link resolution. It fits workflows where the user starts from a keyword, a note ID, a shared link, or an author ID and wants structured platform data rather than a generic summary.

## When To Use It

- The user wants Xiaohongshu note search, keyword expansion, or creator discovery around a topic.
- The task is about a specific note, comment thread, reply chain, or creator page on Xiaohongshu.
- The user can provide `keyword`, `noteId`, `userId`, `shareUrl`, or cursor-style pagination values such as `lastCursor`.
- The user needs note metadata, engagement context, creator signals, or comment text sourced directly from Xiaohongshu endpoints.

## Representative Operations

- `getSearchNoteV3`: Note Search — Search Xiaohongshu notes by keyword for topic discovery, competitor tracking, and content collection.
- `getNoteDetailV7`: Note Details — Pull note metadata, media, and engagement fields for deep inspection of a single post.
- `getUserV4`: User Profile — Inspect creator profile data for account research and benchmark comparisons.
- `shareUrlTransferV1`: Share Link Resolution — Convert a copied Xiaohongshu share link into note identifiers before running detail or comment queries.

## Request Pattern

- 15 read-only `GET` operations are available in this skill.
- Common inputs are `keyword`, `noteId`, `userId`, `lastCursor`, `page`, `commentId`, and `shareUrl`.
- Several endpoints are versioned variants for note detail, comments, and user data; prefer the smallest endpoint that matches the user request.
- If the user only has a shared Xiaohongshu URL, resolve it first and then continue with detail or comment endpoints.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getSearchNoteV3`, `getNoteDetailV7`, `getUserV4`, `shareUrlTransferV1`.
3. Pick the smallest matching operation instead of guessing.
4. Ask the user for any missing required parameter. Do not invent values.
5. Call the helper with:

```bash
node {baseDir}/bin/run.mjs --operation "<operation-id>" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

## Environment

- Required: `JUST_ONE_API_TOKEN`
- This skill uses `JUST_ONE_API_TOKEN` only for authenticated Just One API requests.
- Keep `JUST_ONE_API_TOKEN` private. Do not paste it into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu&utm_content=project_link).

## Output Rules

- Lead with the concrete Xiaohongshu outcome: note match, creator insight, resolved note ID, or comment finding.
- For search-driven requests, restate the keyword, page, sort mode, and any note-type filter before summarizing results.
- For note detail requests, surface title text, author, media type, engagement signals, and any obvious commercial or trend cues before raw JSON.
- For creator-profile or published-note requests, highlight follower-facing signals and the most relevant recent notes first.
- If the backend errors, include the backend payload and the exact operation ID.
