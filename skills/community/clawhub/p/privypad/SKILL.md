---
name: privypad-api
description: >
  Interact with the PrivyPad.com API to read, create, update, delete, and organize
  encrypted notes and groups on behalf of a user. Use this skill whenever the user
  wants to fetch their notes, save something to PrivyPad, search or filter notes
  by group or pinned status, manage note tags, or automate any PrivyPad workflow
  via their API token. Trigger this skill any time PrivyPad, a pp_ token, or note
  management via the PrivyPad API is mentioned — even if the user only asks
  something like "grab my pinned notes" or "save this to PrivyPad".
---

# PrivyPad API Skill

PrivyPad is a zero-knowledge encrypted notes app. This skill covers all interactions
with its public REST API (`https://www.privypad.com/api/v1/`).

---

## Authentication

All note and group endpoints require a **Bearer token** in the `Authorization` header.

```
Authorization: Bearer pp_<uuid>.<base64url-secret>
```

The token is created once in PrivyPad Settings and must be supplied by the user.
Never ask the user for their password — the token is self-contained.

Token management endpoints (`/api/tokens`) use the **session cookie** instead and
are only available in a browser context; do not attempt to call them from scripts.

---

## Base URL

```
https://www.privypad.com/api/v1
```

---

## Endpoints

### Notes

#### List notes
```
GET /notes
```
Query parameters (all optional):
| Parameter | Type    | Description                          |
|-----------|---------|--------------------------------------|
| group     | string  | Filter by group name                 |
| pinned    | boolean | `true` to return only pinned notes   |
| limit     | integer | Max results to return                |
| offset    | integer | Pagination offset                    |

#### Get a single note
```
GET /notes/:id
```

#### Create a note
```
POST /notes
Content-Type: application/json

{
  "title":    "string",
  "content":  "string",
  "group":    "string",   // optional
  "tags":     ["string"], // optional
  "isPinned": false       // optional
}
```

#### Update a note (partial)
```
PATCH /notes/:id
Content-Type: application/json

{
  "title":    "string",   // any subset of fields
  "content":  "string",
  "group":    "string",
  "tags":     ["string"],
  "isPinned": true
}
```

#### Delete / trash a note
```
DELETE /notes/:id
```
Add `?permanent=true` to hard-delete instead of moving to trash.

---

### Groups

#### List groups
```
GET /groups
```
Returns all group names for the authenticated user. No query parameters.

---

## Code Pattern (JavaScript / fetch)

```javascript
const PRIVYPAD_TOKEN = "pp_<uuid>.<base64url-secret>"; // supplied by user
const BASE = "https://privypad.com/api/v1";

async function privypad(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      "Authorization": `Bearer ${PRIVYPAD_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`PrivyPad ${res.status}: ${await res.text()}`);
  return res.json();
}

// Examples
const notes   = await privypad("GET",   "/notes?pinned=true");
const note    = await privypad("GET",   `/notes/${id}`);
const created = await privypad("POST",  "/notes", { title: "Hello", content: "World" });
const updated = await privypad("PATCH", `/notes/${id}`, { isPinned: true });
await              privypad("DELETE", `/notes/${id}`);
const groups  = await privypad("GET",   "/groups");
```

---

## Code Pattern (Python / httpx)

```python
import httpx

TOKEN = "pp_<uuid>.<base64url-secret>"  # supplied by user
BASE  = "https://privypad.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def privypad(method, path, **kwargs):
    r = httpx.request(method, BASE + path, headers=HEADERS, **kwargs)
    r.raise_for_status()
    return r.json()

# Examples
notes   = privypad("GET",    "/notes", params={"group": "Work"})
created = privypad("POST",   "/notes", json={"title": "Hi", "content": "There"})
updated = privypad("PATCH",  f"/notes/{note_id}", json={"isPinned": True})
privypad("DELETE", f"/notes/{note_id}?permanent=true")
groups  = privypad("GET",    "/groups")
```

---

## Important Notes

- **Zero-knowledge**: The server stores notes encrypted. The token embeds the
  client-side secret needed to decrypt them. Never log or expose the token.
- **Trash vs. hard-delete**: `DELETE /notes/:id` moves to trash by default.
  Pass `?permanent=true` only when the user explicitly confirms permanent deletion.
- **HTML content**: The `content` field must be HTML, not Markdown. Use `<h1>`, `<h2>`,
  `<p>`, `<strong>`, `<em>`, `<ul>/<li>`, `<ol>/<li>`, `<hr>` etc.
- **Partial updates**: `PATCH` accepts any subset of fields — only send what changes.
- **Pagination**: Use `limit` + `offset` when fetching large note lists to avoid
  oversized responses.
- **Token scope**: If the user's token was revoked or expired, all API calls will
  return `401`. Prompt the user to generate a new token in PrivyPad Settings.
