---
name: looki-memory
description: Access the user's digital personal memory to retrieve context and generate more personalized, data-driven responses.
---

# Looki Memory

Looki gives you a digital memory captured by the Looki L1 wearable, which sees and hears moments throughout your day. This skill lets AI assistants access your real-world context — the places you went, the people you met, and the things you did — so they can help in ways that go beyond what's on your screen. Use it when you want more personalized, context-aware, data-driven responses.

**Base URL:** Read from `~/.config/looki/credentials.json` → `base_url` field. If the file does not exist, ask the user for both `base_url` and `api_key`.

**Security:**

- Before first use, validate the `base_url` by sending a GET request to `https://open.looki.ai/api/v1/verify?endpoint={base_url}`. Do not include the API key in this request. If validation fails, inform the user and do not proceed.
- Only send the API key in the `X-API-Key` header to `{base_url}/*` endpoints. Do not send it to any other domain.
- Do not save the API key to agent memory, chat history, or any location other than `~/.config/looki/credentials.json`.

## Setup

**Credentials file:** `~/.config/looki/credentials.json`

On first use, check if this file exists. If it does, read `base_url` and `api_key` from it. If it does not, ask the user for both values and offer to save them to this file.

```json
{
    "base_url": "<YOUR_BASE_URL>",
    "api_key": "<YOUR_API_KEY>"
}
```

- `base_url` — The API endpoint URL provided by the user. Do not assume a default; always ask the user if not already saved.
- `api_key` — The user's Looki API key, starting with `lk-`.

Credentials should only be stored in this file. Do not save the API key to agent memory, environment variables, or any other persistent storage.

---

## Authentication

All requests require your API key in the `X-API-Key` header:

```bash
curl "{base_url}/me" \
  -H "X-API-Key: YOUR_API_KEY"
```

---

## Rate Limiting

API requests are limited to **60 requests per minute** per API key. If you exceed this limit, the API will respond with HTTP 429:

```
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "code": 429,
  "detail": "Rate limit exceeded. Please retry after 60 seconds."
}
```

---

## Data Models

### MomentModel

| Field       | Type             | Description                                      |
| ----------- | ---------------- | ------------------------------------------------ |
| id          | string           | Unique identifier of the moment                  |
| title       | string           | Moment title                                     |
| description | string           | Moment description                               |
| media_types | string[]         | Media types included (e.g. `["IMAGE", "VIDEO"]`) |
| cover_file  | MomentFileModel? | Cover file of the moment                         |
| date        | string           | Date in YYYY-MM-DD format                        |
| tz          | string           | Timezone offset in +00:00 format                 |
| start_time  | string           | Start time in ISO 8601 format                    |
| end_time    | string           | End time in ISO 8601 format                      |

### MomentFileModel

| Field      | Type       | Description                      |
| ---------- | ---------- | -------------------------------- |
| id         | string     | Unique identifier of the file    |
| file       | FileModel? | The media file                   |
| thumbnail  | FileModel? | Thumbnail of the file            |
| location   | string?    | Location description             |
| created_at | string     | Creation time in ISO 8601 format |
| tz         | string     | Timezone offset in +00:00 format |

### FileModel

| Field         | Type     | Description                            |
| ------------- | -------- | -------------------------------------- |
| temporary_url | string   | Pre-signed URL (expires in 1 hour)     |
| media_type    | string   | Media type (`IMAGE`, `VIDEO`, `AUDIO`) |
| size          | integer? | File size in bytes                     |
| duration_ms   | integer? | Duration in milliseconds (video/audio) |

### ForYouItemModel

| Field       | Type       | Description                         |
| ----------- | ---------- | ----------------------------------- |
| id          | string     | Unique identifier of the item       |
| type        | string     | Item type (e.g. `COMIC`, `VLOG`)    |
| title       | string     | Item title                          |
| description | string     | Item description                    |
| content     | string     | Item content                        |
| cover       | FileModel? | Cover image file                    |
| file        | FileModel? | Associated media file               |
| created_at  | string     | Creation time in ISO 8601 format    |
| recorded_at | string     | Original recording time in ISO 8601 |

---

## About Me

### Who am I

Returns your basic profile — name, email, timezone, and other details tied to your Looki account.

```bash
curl "{base_url}/me" \
  -H "X-API-Key: YOUR_API_KEY"
```

Response:

```json
{
    "code": 0,
    "detail": "success",
    "data": {
        "user": {
            "id": "string",
            "email": "string",
            "first_name": "string",
            "last_name": "string",
            "tz": "string",
            "gender": "string",
            "birthday": "string",
            "region": "string"
        }
    }
}
```

## My Memories

### What happened these days

Returns a calendar view of moments for a date range, showing which days have recorded moments and a highlight description from each day.

| Parameter  | Type   | Required | Description                                         |
| ---------- | ------ | -------- | --------------------------------------------------- |
| start_date | string | required | Start date in YYYY-MM-DD format (e.g. `2026-01-01`) |
| end_date   | string | required | End date in YYYY-MM-DD format (e.g. `2026-01-31`)   |

```bash
curl "{base_url}/moments/calendar?start_date=2026-01-01&end_date=2026-01-31" \
  -H "X-API-Key: YOUR_API_KEY"
```

Response:

```json
{
    "code": 0,
    "detail": "success",
    "data": [
        {
            "date": "2026-01-15",
            "highlight_moment": {
                "id": "string",
                "title": "string",
                "description": "string",
                "media_types": ["IMAGE", "VIDEO"],
                "date": "2026-01-15",
                "tz": "+08:00",
                "start_time": "2026-01-15T10:00:00+08:00",
                "end_time": "2026-01-15T12:00:00+08:00"
            }
        }
    ]
}
```

### What happened on [date]

Returns everything that was captured on a specific day — each moment with its title, description, time range, and cover image.

| Parameter | Type   | Required | Description               |
| --------- | ------ | -------- | ------------------------- |
| on_date   | string | required | Date in YYYY-MM-DD format |

```bash
curl "{base_url}/moments?on_date=2026-01-01" \
  -H "X-API-Key: YOUR_API_KEY"
```

Response:

```json
{
    "code": 0,
    "detail": "success",
    "data": [
        {
            "id": "string",
            "title": "string",
            "description": "string",
            "media_types": ["IMAGE", "VIDEO"],
            "cover_file": {
                "id": "string",
                "file": {
                    "temporary_url": "string",
                    "media_type": "IMAGE",
                    "size": 1024,
                    "duration_ms": null
                },
                "thumbnail": null,
                "location": "string",
                "created_at": "2026-01-01T10:30:00+08:00",
                "tz": "+08:00"
            },
            "date": "2026-01-01",
            "tz": "+08:00",
            "start_time": "2026-01-01T10:00:00+08:00",
            "end_time": "2026-01-01T12:00:00+08:00"
        }
    ]
}
```

### Recall this moment

Returns the full details of a single moment — its description, location, time range, and cover image.

| Parameter | Type   | Required | Description                                |
| --------- | ------ | -------- | ------------------------------------------ |
| moment_id | string | required | The unique identifier of the moment (UUID) |

```bash
curl "{base_url}/moments/MOMENT_ID" \
  -H "X-API-Key: YOUR_API_KEY"
```

Response:

```json
{
    "code": 0,
    "detail": "success",
    "data": {
        "id": "string",
        "title": "string",
        "description": "string",
        "media_types": ["IMAGE", "VIDEO"],
        "cover_file": {
            "id": "string",
            "file": {
                "temporary_url": "string",
                "media_type": "IMAGE",
                "size": 1024,
                "duration_ms": null
            },
            "thumbnail": null,
            "location": "string",
            "created_at": "2026-01-15T10:30:00+08:00",
            "tz": "+08:00"
        },
        "date": "2026-01-15",
        "tz": "+08:00",
        "start_time": "2026-01-15T10:00:00+08:00",
        "end_time": "2026-01-15T12:00:00+08:00"
    }
}
```

### Photos and videos from this moment

Returns the photos and videos from a specific moment. You can filter to just the highlights or page through all media.

| Parameter | Type    | Required | Description                                        |
| --------- | ------- | -------- | -------------------------------------------------- |
| moment_id | string  | required | The unique identifier of the moment (UUID)         |
| highlight | boolean |          | Filter by highlight status                         |
| cursor_id | string  |          | Cursor for pagination. Omit for the first request. |
| limit     | integer |          | Number of items to return (default 20, max 100)    |

```bash
curl "{base_url}/moments/MOMENT_ID/files?limit=20" \
  -H "X-API-Key: YOUR_API_KEY"
```

Response:

```json
{
    "code": 0,
    "detail": "success",
    "data": {
        "items": [
            {
                "id": "string",
                "file": {
                    "temporary_url": "string",
                    "media_type": "IMAGE",
                    "size": 1024,
                    "duration_ms": null
                },
                "thumbnail": {
                    "temporary_url": "string",
                    "media_type": "IMAGE",
                    "size": 512,
                    "duration_ms": null
                },
                "location": "string",
                "created_at": "2026-01-15T10:30:00+08:00",
                "tz": "+08:00"
            }
        ],
        "next_cursor_id": "string | null",
        "has_more": true
    }
}
```

### Find moments about [topic]

Searches across all your memories using natural language. Returns moments ranked by relevance — useful when you remember the gist but not the exact date.

| Parameter  | Type    | Required | Description                                      |
| ---------- | ------- | -------- | ------------------------------------------------ |
| query      | string  | required | Search query string (1-100 characters)           |
| start_date | string  |          | Filter results from this date (YYYY-MM-DD)       |
| end_date   | string  |          | Filter results up to this date (YYYY-MM-DD)      |
| page       | integer |          | Page number, starts from 1 (default 1)           |
| page_size  | integer |          | Number of results per page (default 10, max 100) |

```bash
curl "{base_url}/moments/search?query=Something&page_size=10" \
  -H "X-API-Key: YOUR_API_KEY"
```

Response:

```json
{
    "code": 0,
    "detail": "success",
    "data": {
        "items": [
            {
                "id": "string",
                "title": "string",
                "description": "string",
                "media_types": ["IMAGE"],
                "cover_file": { ... },
                "date": "2026-01-15",
                "tz": "+08:00",
                "start_time": "2026-01-15T10:00:00+08:00",
                "end_time": "2026-01-15T12:00:00+08:00"
            }
        ],
        "next_cursor_id": null,
        "has_more": true
    }
}
```

## My Highlights

### What's new for me

Returns AI-generated highlights made from your memories — comics, vlogs, and other creative recaps of your real-life experiences.

| Parameter     | Type    | Required | Description                                                                      |
| ------------- | ------- | -------- | -------------------------------------------------------------------------------- |
| group         | string  |          | Filter by item group: `all`, `comic`, `vlog`, `present`, `other` (default `all`) |
| liked         | boolean |          | Filter by liked status                                                           |
| recorded_from | string  |          | Filter by recording date from (YYYY-MM-DD)                                       |
| recorded_to   | string  |          | Filter by recording date to (YYYY-MM-DD)                                         |
| created_from  | string  |          | Filter by creation date from (YYYY-MM-DD)                                        |
| created_to    | string  |          | Filter by creation date to (YYYY-MM-DD)                                          |
| cursor_id     | string  |          | Cursor for pagination                                                            |
| limit         | integer |          | Number of items to return (default 20, max 100)                                  |
| order_by      | string  |          | Sort field: `created_at` or `recorded_at` (default `recorded_at`)                |

```bash
curl "{base_url}/for_you/items?limit=20&group=comic" \
  -H "X-API-Key: YOUR_API_KEY"
```

Response:

```json
{
    "code": 0,
    "detail": "success",
    "data": {
        "items": [
            {
                "id": "string",
                "type": "COMIC",
                "title": "string",
                "description": "string",
                "content": "string",
                "cover": {
                    "temporary_url": "string",
                    "media_type": "IMAGE",
                    "size": null,
                    "duration_ms": null
                },
                "file": {
                    "temporary_url": "string",
                    "media_type": "IMAGE",
                    "size": null,
                    "duration_ms": null
                },
                "created_at": "2026-01-15T10:30:00+08:00",
                "recorded_at": "2026-01-14T18:00:00+08:00"
            }
        ],
        "next_cursor_id": "string | null",
        "has_more": true
    }
}
```

## Realtime

### What's happening right now

Returns the most recent realtime event detected by your Looki device. Requires proactive mode to be enabled in the Looki app.

> **Beta:** This feature is currently in beta testing. You may not have access to enable proactive mode yet.

```bash
curl "{base_url}/realtime/latest-event" \
  -H "X-API-Key: YOUR_API_KEY"
```

Response:

```json
{
    "code": 0,
    "detail": "success",
    "data": {
        "id": "string",
        "description": "string",
        "start_time": "2026-01-15T10:00:00+08:00",
        "end_time": "2026-01-15T10:15:00+08:00",
        "tz": "+08:00",
        "location": "string"
    }
}
```
