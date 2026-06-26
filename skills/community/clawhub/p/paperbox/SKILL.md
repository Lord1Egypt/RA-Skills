---
name: paperbox
description: Upload AI-generated HTML games, apps, or generative art to PaperBox (paperbox-beta.vercel.app) and return a shareable link. Use when the agent has created an HTML game, app, generative art, or interactive project and the user wants to share it. Triggers on phrases like "share this", "upload to PaperBox", "publish my app", "get a link", or after any HTML game/app/art creation task.
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
      },
  }
---

# PaperBox

Publish a self-contained HTML game, app, or generative art to [PaperBox](https://paperbox-beta.vercel.app) and return a live, shareable URL.

## Endpoint (confirmed working)

```
POST https://paperbox-beta.vercel.app/api/games
```

## Workflow

1. Ensure the HTML is complete and self-contained (all CSS/JS inlined).
2. POST to the API using `run_terminal_cmd` or an HTTP tool — **do NOT use the browser**.
3. Parse the JSON response and extract `data.shareableUrl`.
4. Send that URL back as a **text message** to the user via the same channel they used (Telegram, WhatsApp, etc.). Do not open any browser or navigate anywhere.

### Request

```bash
curl -X POST https://paperbox-beta.vercel.app/api/games \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <from openclaw.json skills.entries.paperbox.apiKey>" \
  -d '{
    "title": "My Snake Game",
    "description": "A classic snake game built with HTML5 canvas",
    "htmlContent": "<!DOCTYPE html><html>...</html>"
  }'
```

### Response (success)

```json
{
  "success": true,
  "data": {
    "projectId": "cmmk7bame0003gywakm5c0ora",
    "slug": "my-snake-game-1773122429317",
    "shareableUrl": "https://paperbox-beta.vercel.app/project/my-snake-game-1773122429317",
    "title": "My Snake Game",
    "message": "Game published successfully. Share this link with others."
  }
}
```

The shareable link is at `data.shareableUrl` — use this exact value. Do not construct the URL manually from the slug.

### Field reference

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | Max 100 chars |
| `description` | string | yes | Max 500 chars |
| `htmlContent` | string | yes | Full self-contained HTML |

## Output to user

After a successful upload:
- **Reply in chat** (Telegram, WhatsApp, or whatever channel the user is on) with the `data.shareableUrl` from the API response
- Do NOT open a browser, navigate to any URL, or use any browser tool
- Format the reply as:

> ✅ Your project is live on PaperBox!
> 🔗 View it (use Safari or Chrome on phone): {data.shareableUrl}
> 📤 Share this link — no account needed.

## Error handling

| Status | Meaning | Action |
|---|---|---|
| 401 | Invalid API key | Check `PAPERBOX_API_KEY` credential |
| 400 | Bad request | Check required fields and valid HTML |
| 413 | HTML too large | Minify CSS/JS |
| 500 | Server error | Retry once; report to user if it persists |
