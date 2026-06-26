---
name: md-viewer
description: LAN-accessible web viewer for Markdown files optimized for e-readers. Auto-binds to LAN IP for easy access. TRIGGER when user says "cho tôi xem", "show me", "mở file", "view file", "xem md", "xem file này", or wants to review a .md file. Instead of reading/summarizing, generate a LAN link for user to view directly in browser from any device on WiFi.
---

# MD Viewer

## Key Principle

**When user says "show me the file", "view this file":**
- ❌ DO NOT read and summarize the content
- ✅ DO generate LAN link for user to view directly

User wants to VIEW the file themselves, not hear a summary.

## Security Features

- ✅ **Only .md files** - Blocks all other file types
- ✅ **Blocked paths** - Cannot access /etc, ~/.ssh, ~/.gnupg, etc.
- ✅ **Password protection** - Auto-generated password with cookie auth (30 days)
- ✅ **XSS protection** - HTML sanitized with bleach library
- ✅ **CSP headers** - Content Security Policy enforced
- ✅ **Auto LAN IP binding** - Binds to LAN IP automatically
- ✅ **Link sharing** - Token in URL for one-time access, saves cookie for future
- ✅ **No caching** - Files always refresh on page reload

## Workflow

### Step 1: Start Server (Auto-generates password and binds to LAN)

```bash
python3 ~/.openclaw/skills/md-viewer/scripts/server.py
```

Output:
```
============================================================
📄 MD Viewer Server Started
============================================================
Local:    http://localhost:8765
Network:  http://10.0.10.93:8765
------------------------------------------------------------
🔐 Password: a1b2c3d4e5f6
   ⚠️  SAVE THIS PASSWORD - Required for login!
============================================================
```

### Step 2: Share Link

Links include password token for easy sharing:
```
http://10.0.10.93:8765/view?path=/path/to/file.md&token=PASSWORD
```

### Step 3: Access

1. Click link → Auto-authenticated via token
2. Password saved to cookie (30 days)
3. Future visits → Auto-authenticated via cookie

## Server Options

```bash
python3 ~/.openclaw/skills/md-viewer/scripts/server.py [options]

Options:
  --host HOST          Host to bind (default: auto-detect LAN IP)
  --port PORT          Port (default: 8765)
  --password PASSWORD  Custom password (auto-generated if not set)
  --no-history         Disable history tracking for privacy
  --localhost          Bind to localhost only (no LAN access)
```

## Blocked Paths

Automatically blocked:
- System: `/etc`, `/proc`, `/sys`, `/dev`, `/var/log`
- SSH: `~/.ssh/`, `id_rsa`, `id_dsa`, etc.
- GPG: `~/.gnupg/`
- Cloud: `~/.aws/`, `~/.gcp/`
- Passwords: `.netrc`, `.pgpass`, `.env`
- Certs: `.pem`, `.key`, `.p12`, `.pfx`

## Features

- Light theme (e-ink optimized)
- Serif fonts for comfortable reading
- High contrast for e-readers
- Syntax highlighting
- Mobile-friendly UI
- History tracking (50 files, enabled by default)
- Cookie-based authentication (30 days)
- XSS protection with bleach
- Auto LAN IP binding

## Dependencies

```bash
pip3 install markdown bleach
```

## Resources

### scripts/

- `server.py` - Web server with security features
- `md-link.py` - Link generator helper