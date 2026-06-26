# Max Auth - Setup & API Reference

## Overview

Max Auth runs as a local HTTP server on `127.0.0.1:8456` by default. Put HTTPS in front of it for browser/WebAuthn flows.

Architecture:

```text
Browser -> HTTPS reverse proxy -> http://127.0.0.1:8456
Agent   -> http://127.0.0.1:8456 (direct local calls)
```

The browser UI is localized in Portuguese, English, and Spanish.

## Installation

```bash
mkdir -p ~/.max-auth && cd ~/.max-auth
cp <skill-path>/assets/auth-server.js .
cp <skill-path>/assets/package.json .
npm install
node auth-server.js set-password 'your_strong_password'
node auth-server.js
```

## systemd example

```bash
sudo tee /etc/systemd/system/max-auth.service > /dev/null <<'EOF'
[Unit]
Description=Max Auth Server
After=network.target

[Service]
Type=simple
User=%i
WorkingDirectory=/home/%i/.max-auth
ExecStart=/usr/bin/node /home/%i/.max-auth/auth-server.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

Adjust to your environment before enabling.

## Reverse proxy examples

Tailscale serve:

```bash
sudo tailscale serve --set-path=/auth --bg http://127.0.0.1:8456
```

Caddy:

```caddy
example.com {
  reverse_proxy /auth* 127.0.0.1:8456
}
```

nginx:

```nginx
location /auth {
  proxy_pass http://127.0.0.1:8456;
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

## Session-scoped auth API

### GET /auth/status?session=<sessionKey>

Response example:

```json
{
  "hasPassword": true,
  "hasSession": false,
  "sessionExpiresAt": null,
  "source": null,
  "requestedSessionKey": "telegram:6314900956",
  "resolvedSessionKey": "telegram:6314900956",
  "grant": null
}
```

### POST /auth/login

Request:

```json
{
  "password": "...",
  "sessionKey": "telegram:6314900956"
}
```

### POST /auth/logout

Request:

```json
{
  "sessionKey": "telegram:6314900956"
}
```

### GET /auth/verify?session=<sessionKey>

Send bearer token in `Authorization: Bearer ...`.

## Secret form API

### POST /auth/secrets/create

Request:

```json
{
  "label": "Twilio credentials",
  "fields": [
    {"name": "account_sid", "label": "Account SID", "type": "text"},
    {"name": "auth_token", "label": "Auth Token", "type": "password"}
  ],
  "session_key": "telegram:6314900956",
  "expires_in_minutes": 30
}
```

Response:

```json
{
  "ok": true,
  "token": "...",
  "url": "https://your-host/auth/secrets/<token>",
  "expires_at": 1776817421732
}
```

### GET /auth/secrets/<token>
Renders the one-time browser form.

### POST /auth/secrets/<token>/submit
Submits values from the browser form.

### GET /auth/secrets/<token>/poll
Polling semantics:
- `202 {"submitted": false}` while waiting
- `200 {"submitted": true, "values": {...}}` once submitted
- consumes/deletes the values on first successful retrieval
- `404/410` if expired or already consumed

## OpenClaw plugin tools

- `check_auth({ sessionKey })`
- `require_auth({ action, sessionKey })`
- `request_secret({ label, fields, session_key?, expires_in_minutes? })`
- `retrieve_secret({ token })`

## Security notes

- auth server binds to localhost only
- browser access must come through HTTPS
- secret form values are memory-only
- secret retrieval is one-time
- session auth is independent per session key
