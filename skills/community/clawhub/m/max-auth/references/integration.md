# OpenClaw Agent Integration Guide

## When to check auth

Require auth before:
- destructive actions
- package installs or system changes
- sending third-party messages/emails
- mutating external APIs

Read-only work does not need auth.

## Session-scoped pattern

Always pass the current channel/session key.

Examples:
- `telegram:6314900956`
- `discord:channel:1488653811185881133`
- `global`

Node example:

```javascript
const http = require('http');

function checkAuth(sessionKey) {
  return new Promise((resolve) => {
    http.get(`http://127.0.0.1:8456/status?session=${encodeURIComponent(sessionKey)}`, (res) => {
      let body = '';
      res.on('data', (d) => { body += d; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch {
          resolve({ hasSession: false });
        }
      });
    }).on('error', () => resolve({ hasSession: false }));
  });
}
```

Behavior:
1. call `/status?session=<sessionKey>`
2. if `hasSession: true` -> proceed
3. if `hasSession: false` -> refuse and send `https://<host>/auth?session=<sessionKey>`

## Secure secret collection pattern

Use this instead of asking for secrets in chat.

1. `request_secret(...)`
2. send returned URL to the user
3. poll `retrieve_secret({ token })`
4. once retrieved, use the values and do not echo them back into chat

Example request:

```json
{
  "label": "SMTP credentials",
  "fields": [
    {"name": "username", "label": "Username", "type": "text"},
    {"name": "password", "label": "Password", "type": "password"}
  ],
  "session_key": "telegram:6314900956"
}
```

Semantics:
- user submits via HTTPS browser form
- values stay in auth-server memory only
- `retrieve_secret` returns them once
- first successful retrieval consumes them
- no secret needs to appear in chat history

## Shell check example

```bash
SESSION_KEY='telegram:6314900956'
STATUS=$(curl -s "http://127.0.0.1:8456/status?session=$(python3 - <<'PY'
import urllib.parse
print(urllib.parse.quote('telegram:6314900956', safe=''))
PY
)")
```

## Rule

Do not proceed with sensitive work if the relevant session key is not authenticated.
Do not ask the user to paste secrets into chat when `request_secret` is available.
