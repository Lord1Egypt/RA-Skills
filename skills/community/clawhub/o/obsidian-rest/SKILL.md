---
name: obsidian-rest
description: Read, write, search, create, append, patch, and manage notes in any Obsidian vault via the Local REST API plugin (Windows, macOS, or Linux). Use when asked to save notes, find information, read a document, append to a file, search the vault, write a runbook, update documentation, or manage Obsidian content. Triggers: "save this to Obsidian", "note this", "add to obsidian", "read my note on X", "find in obsidian", "update the runbook", "what did I save about X", "list my vault", "create a note", "append to", "sv".
homepage: https://github.com/nj070574-gif/openclaw-obsidian-vault-skill
metadata:
  {
    "openclaw":
      {
        "emoji": "💎",
        "requires":
          {
            "env": ["OBSIDIAN_URL", "OBSIDIAN_API_KEY"],
          },
        "config":
          {
            "requiredEnv": ["OBSIDIAN_URL", "OBSIDIAN_API_KEY"],
            "example": "Environment=OBSIDIAN_URL=https://YOUR_HOST:27124\nEnvironment=OBSIDIAN_API_KEY=your_api_key_here",
          },
      },
  }
---

# Obsidian Local REST API Skill

Control any Obsidian vault from OpenClaw using the
[Local REST API plugin](https://github.com/coddingtonbear/obsidian-local-rest-api).
Works on any OS where Obsidian Desktop runs (Windows, macOS, Linux).
No extra CLI tools needed — just curl.

---

## Critical: Known Pitfalls (Read First)

These issues were discovered in real-world use and will cause silent failures if ignored:

### 1. Trailing slashes are mandatory on directory paths
The API returns `{"message":"Not Found","errorCode":40400}` if you omit trailing slashes on directory endpoints.

| Path | Result |
|------|--------|
| `$OBSIDIAN_URL/vault/` | ✅ Correct — lists vault root |
| `$OBSIDIAN_URL/vault` | ❌ 40400 error |
| `$OBSIDIAN_URL/vault/My%20Folder/` | ✅ Correct — lists subfolder |
| `$OBSIDIAN_URL/vault/My%20Folder` | ❌ 40400 error |

### 2. The root health check endpoint is `/` — nothing else
There is no `/api/`, `/api/healthz`, `/healthz`, `/status`, or `/health` endpoint.

| Path | Result |
|------|--------|
| `$OBSIDIAN_URL/` | ✅ Returns plugin status JSON |
| `$OBSIDIAN_URL/api/` | ❌ 40400 error |
| `$OBSIDIAN_URL/api/healthz` | ❌ 40400 error |

### 3. Shell variable expansion may fail in exec contexts
`$OBSIDIAN_URL` and `$OBSIDIAN_API_KEY` are available in the gateway process but child shells
spawned by the exec tool may not inherit them depending on your OpenClaw configuration.
**Always test variable expansion before using them in curl:**
```bash
echo "URL=$OBSIDIAN_URL KEY_LEN=${#OBSIDIAN_API_KEY}"
```
If either is empty, use hardcoded values in your curl commands for this session.

### 4. Never dump raw JSON to the user
Always interpret API responses and reply in plain English. See the Output Formatting section.

---

## Prerequisites

1. **Obsidian Desktop** installed and running with a vault open.
2. **Local REST API plugin** installed and enabled in Obsidian:
   - Open Obsidian → Settings → Community plugins → Browse → search "Local REST API" → Install → Enable.
3. **API Key** copied from: Settings → Local REST API → API Key.
4. **Port** noted (default: `27124`). HTTPS is strongly recommended.
5. **Env vars** set in your OpenClaw service (see Setup below).

---

## Setup

### 1. Add env vars to your OpenClaw systemd service

```bash
sudo nano /etc/systemd/system/openclaw.service
```

Add these two lines in the `[Service]` block:

```ini
Environment=OBSIDIAN_URL=https://YOUR_OBSIDIAN_HOST:27124
Environment=OBSIDIAN_API_KEY=your_api_key_here
```

Then reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart openclaw.service
```

### 2. Verify env vars are live in the gateway process

```bash
PID=$(pgrep -f "openclaw-gateway" | head -1)
cat /proc/$PID/environ | tr "\0" "\n" | grep "^OBSIDIAN"
```

Both `OBSIDIAN_URL` and `OBSIDIAN_API_KEY` should appear with correct values.

### 3. Test the connection

```bash
curl -sk \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  "$OBSIDIAN_URL/" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('OK — Obsidian', d['versions']['obsidian'], '| Plugin', d['versions']['self'], '| Auth:', d['authenticated'])"
```

Expected: `OK — Obsidian 1.x.x | Plugin 3.x.x | Auth: True`

If `$OBSIDIAN_URL` is empty, substitute the literal URL:
```bash
curl -sk \
  -H "Authorization: Bearer YOUR_API_KEY_HERE" \
  "https://YOUR_OBSIDIAN_HOST:27124/" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('OK — Obsidian', d['versions']['obsidian'], '| Plugin', d['versions']['self'], '| Auth:', d['authenticated'])"
```

### 4. Install the skill

```bash
# Via ClawHub
openclaw skills install obsidian-rest

# Or manually
git clone https://github.com/nj070574-gif/openclaw-obsidian-vault-skill.git
cp -r openclaw-obsidian-vault-skill/skill ~/.openclaw/workspace/skills/obsidian-rest
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OBSIDIAN_URL` | ✅ Yes | Full base URL including protocol and port, e.g. `https://192.168.1.100:27124` |
| `OBSIDIAN_API_KEY` | ✅ Yes | API key from Obsidian → Settings → Local REST API |

Always use `curl -sk` — the plugin uses a self-signed certificate by default.

---

## API Reference

All requests require the auth header:
```
Authorization: Bearer $OBSIDIAN_API_KEY
```

### Check API status (root endpoint only)
```bash
curl -sk -H "Authorization: Bearer $OBSIDIAN_API_KEY" "$OBSIDIAN_URL/"
```
Returns: `{"status":"OK","authenticated":true,"versions":{"obsidian":"1.x.x","self":"3.x.x"}, ...}`

---

### List vault root (trailing slash required)
```bash
curl -sk -H "Authorization: Bearer $OBSIDIAN_API_KEY" "$OBSIDIAN_URL/vault/" \
  | python3 -c "import json,sys; [print(f) for f in sorted(json.load(sys.stdin)['files'])]"
```

### List a subfolder (trailing slash required)
```bash
curl -sk -H "Authorization: Bearer $OBSIDIAN_API_KEY" "$OBSIDIAN_URL/vault/My%20Folder/" \
  | python3 -c "import json,sys; [print(f) for f in json.load(sys.stdin)['files']]"
```

> **URL encoding:** spaces → `%20` | forward slash within a path segment → `%2F`

**Encode any path automatically:**
```bash
python3 -c "import urllib.parse; print(urllib.parse.quote('My Folder/My Note.md', safe=''))"
```

---

### Read a note
```bash
curl -sk -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  "$OBSIDIAN_URL/vault/PATH%2FTO%2FNOTE.md"
```
Returns raw Markdown content.

---

### Create or overwrite a note (PUT)
```bash
curl -sk -X PUT \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: text/markdown" \
  --data-binary "# My Note Title

Content goes here." \
  "$OBSIDIAN_URL/vault/PATH%2FTO%2FNOTE.md"
```
Returns HTTP `204 No Content` on success.
**Warning: PUT replaces the entire file. Use POST to append safely.**

---

### Append to an existing note (POST)
```bash
curl -sk -X POST \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: text/markdown" \
  --data-binary "

## New Section $(date +%Y-%m-%d)

Content to append." \
  "$OBSIDIAN_URL/vault/PATH%2FTO%2FNOTE.md"
```
Returns HTTP `204 No Content` on success.

---

### Patch / insert at a heading (PATCH)
```bash
curl -sk -X PATCH \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: text/markdown" \
  -H "Obsidian-API-Operation: append" \
  -H "Heading: My Section Heading" \
  --data-binary "Content to insert under the heading." \
  "$OBSIDIAN_URL/vault/PATH%2FTO%2FNOTE.md"
```
Valid operations: `append` | `prepend` | `replace`

---

### Delete a note
```bash
curl -sk -X DELETE \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  "$OBSIDIAN_URL/vault/PATH%2FTO%2FNOTE.md"
```
Returns HTTP `204 No Content` on success.

---

### Search vault (full-text)
```bash
curl -sk -X POST \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  "$OBSIDIAN_URL/search/simple/?query=YOUR+SEARCH+TERM&contextLength=150" \
  | python3 -c "
import json, sys
results = json.load(sys.stdin)
if not results:
    print('No matches found.')
else:
    print(f'Found {len(results)} match(es):')
    for r in results[:5]:
        print(' -', r['filename'])
        for m in r.get('matches', [])[:1]:
            ctx = m.get('context', '').strip()
            if ctx: print('   ...', ctx[:100])
"
```

---

### Get currently active file in Obsidian
```bash
curl -sk -H "Authorization: Bearer $OBSIDIAN_API_KEY" "$OBSIDIAN_URL/active/"
```

---

### List available Obsidian commands
```bash
curl -sk -H "Authorization: Bearer $OBSIDIAN_API_KEY" "$OBSIDIAN_URL/commands/" \
  | python3 -c "import json,sys; [print(c['id'], '|', c['name']) for c in json.load(sys.stdin).get('commands',[])]"
```

### Execute an Obsidian command
```bash
curl -sk -X POST \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"commandId": "editor:save-file"}' \
  "$OBSIDIAN_URL/commands/execute/"
```

---

## Output Formatting Rules

**Never dump raw JSON to the user. Always interpret results and reply in plain English.**

| Situation | What to say |
|-----------|-------------|
| Status check returns `"authenticated": true` | "✅ Obsidian vault connected — Obsidian v1.x.x, plugin v3.x.x" |
| Status check fails / 40400 error | "❌ Cannot reach Obsidian vault: [exact error]. Check Obsidian is running." |
| Vault listed | "Your vault contains X items: [list files and folders]" |
| Subfolder listed | "Found X notes in [folder]: [list]" |
| Note read | Return the note content (or a summary if it's long) |
| Note created (HTTP 204) | "✅ Created [path]" |
| Note saved / overwritten (HTTP 204) | "✅ Saved to [path]" |
| Note appended (HTTP 204) | "✅ Appended to [path]" |
| Search returns results | "Found X notes matching '[query]': [list filenames]" |
| Search returns nothing | "No notes found matching '[query]'" |
| 40400 error | "❌ API returned Not Found — check the path and trailing slashes" |
| 401 error | "❌ Unauthorised — check OBSIDIAN_API_KEY is set correctly" |

---

## Workflow Guide

### Saving content ("sv" / "save this")
1. Check env vars expand: `echo "URL=$OBSIDIAN_URL LEN=${#OBSIDIAN_API_KEY}"`
2. Pick the right folder from context (infrastructure → `Infrastructure/`, daily log → `Daily/`)
3. Choose a descriptive hyphenated filename, e.g. `Setup-Guide-2026-04-12.md`
4. Check if file exists: `GET /vault/PATH.md` — HTTP 404 means safe to create
5. Use `PUT` to create, `POST` to append to existing
6. Confirm with plain English: "✅ Saved to `Infrastructure/Setup-Guide.md`"

### Finding a note
1. Search: `POST /search/simple/?query=TERM`
2. If multiple results, list filenames and ask which to open
3. `GET` the file and return its content or a summary

### Updating a note
1. Read the file first to understand its structure
2. `POST` to append, or `PATCH` with `Heading` header for targeted insertion
3. Confirm what was added and where

### Creating new folders
New folders are created automatically when you `PUT` a file into a path that doesn't exist yet.

---

## Common Patterns

### Save a runbook
```bash
NOTE_PATH="Infrastructure%2FRunbook-$(date +%Y-%m-%d).md"
curl -sk -X PUT \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: text/markdown" \
  --data-binary "# Runbook — $(date +%Y-%m-%d)

## Steps

1. Step one
2. Step two
" \
  "$OBSIDIAN_URL/vault/$NOTE_PATH"
echo "Saved to vault/$NOTE_PATH"
```

### Append a timestamped log entry
```bash
curl -sk -X POST \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: text/markdown" \
  --data-binary "
- $(date '+%Y-%m-%d %H:%M') — Log entry here" \
  "$OBSIDIAN_URL/vault/Daily%2FLog.md"
```

---

## URL Encoding Quick Reference

| Character | Encoded |
|-----------|---------|
| Space ` ` | `%20` |
| `/` (within a path segment) | `%2F` |
| `#` | `%23` |
| `&` | `%26` |
| `+` | `%2B` |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `curl: (7) Failed to connect` | Obsidian not running or wrong host/port | Check Obsidian is open; verify `OBSIDIAN_URL` |
| `{"message":"Not Found","errorCode":40400}` | **Wrong path** — missing trailing slash, or non-existent endpoint | Add `/` to end of directory paths; use only documented endpoints |
| `HTTP 401 Unauthorized` | Wrong or missing API key | Verify `OBSIDIAN_API_KEY` matches plugin settings |
| SSL certificate error | Self-signed cert | Always use `curl -sk` — never `curl -s` alone |
| `$OBSIDIAN_URL` empty in curl | Env var not inherited by exec shell | Test with `echo $OBSIDIAN_URL`; use literal values if empty |
| Skill shows `△ needs setup` | Env vars not set | Add `Environment=` lines to `openclaw.service`, reload, restart |
| Obsidian on Windows, agent on Linux | Firewall blocking port | Allow TCP 27124 inbound in Windows Defender Firewall |

### Windows Firewall (Obsidian on Windows, OpenClaw on Linux)
```
Windows Defender Firewall → Advanced Settings → Inbound Rules → New Rule
→ Port → TCP → 27124 → Allow → All profiles → Name: "Obsidian Local REST API"
```

---

## Plugin Information

- **Plugin:** [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) by Adam Coddington
- **Default port:** `27124`
- **Protocol:** HTTPS (self-signed cert) or HTTP
- **Obsidian minimum version:** `0.12.0`
- **Plugin version tested:** `3.2.0`
