name: web
description: Browse and extract content from webpages using the local browser service.
version: 0.1.0
author: PingAGI
metadata: { "openclaw": { "emoji": "🌐" } }

---

# Web Browser Skill

Use this skill when the agent needs to:

- open a webpage
- extract webpage text
- browse websites
- retrieve webpage content

The agent can call the local browser service:
Example command (replace URL with the target webpage):

```
curl -s -X POST http://127.0.0.1:3088/browse \
-H "Content-Type: application/json" \
-d '{"url":"https://example.com"}'
```

The response returns JSON containing:

- page title
- page text
- partial HTML
- optional screenshot (base64)

The agent should extract useful information from the "text" field.
