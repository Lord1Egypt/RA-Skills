---
name: nano-diary-hook
description: Post diary entries to a Nano diary platform via webhook. Supports creating new entries and AI-powered merging with existing handwritten diaries.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - NANO_DIARY_HOOK_TOKEN
      bins:
        - curl
      primaryEnv: NANO_DIARY_HOOK_TOKEN
---

# Nano Diary Hook

Post diary content to a user's Nano diary platform via webhook token.

## When to use

Use this skill when the user wants to:
- Write or submit a diary entry for a specific date
- Log daily thoughts, activities, or reflections to their diary
- Send AI-generated diary content to their Nano account

## Environment

- `NANO_DIARY_HOOK_TOKEN` (required): The user's personal webhook token, generated from Nano diary settings page.

## API

**Endpoint:**

```
POST https://image.yezishop.vip/api/diary-hook/${NANO_DIARY_HOOK_TOKEN}
```

**Headers:**

```
Content-Type: application/json
```

**Request body:**

```json
{
  "date": "YYYY-MM-DD",
  "content": "Diary content text"
}
```

- `date` (required): Date in `YYYY-MM-DD` format, e.g. `2026-03-06`
- `content` (required): The diary content as plain text

**Example:**

```bash
curl -X POST "https://image.yezishop.vip/api/diary-hook/${NANO_DIARY_HOOK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-03-06", "content": "Today I learned how to publish OpenClaw skills to ClawHub."}'
```

## Response

Success (new diary created):
```json
{ "success": true, "merged": false, "diary_id": 123 }
```

Success (merged with existing handwritten diary via AI):
```json
{ "success": true, "merged": true, "diary_id": 123 }
```

Error responses:
```json
{ "success": false, "error": "date and content are required" }
{ "success": false, "error": "date must be in YYYY-MM-DD format" }
{ "success": false, "error": "Invalid token" }
```

## Behavior

- If no diary exists for the given date, a new entry is created.
- If a diary already exists with handwritten content, the submitted content is automatically merged with it using AI to produce a coherent combined entry.
- If a diary exists but has no handwritten content, the submitted content is saved directly.

## Notes

- Content should be plain text (not Markdown or HTML).
- One diary entry per date. Submitting again for the same date will update the existing entry.
- The merge process is asynchronous; the API responds immediately while AI merging happens in the background.
