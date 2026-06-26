# 📄 MD Viewer - LAN Markdown Viewer for OpenClaw

A LAN-accessible web viewer for Markdown files optimized for e-readers. Auto-binds to LAN IP for easy sharing.

![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🌐 **Auto LAN Binding** - Automatically binds to LAN IP for easy access
- 📱 **E-ink Optimized** - Light theme, serif fonts, high contrast
- 🔐 **Secure Auth** - Password in URL for sharing + cookie (30 days)
- 🛡️ **XSS Protection** - HTML sanitized with bleach library
- 📜 **History Tracking** - 50 files, enabled by default (can disable)
- 🔄 **No Caching** - Always shows latest file content

## 🚀 Quick Start

### Install

```bash
# Clone to OpenClaw skills directory
git clone https://github.com/hoangcongst/md-viewer.git ~/.openclaw/skills/md-viewer

# Install dependencies
pip3 install markdown bleach
```

### Start Server

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
🔐 Password: xk9mz2p7q4w8
   ⚠️  SAVE THIS PASSWORD - Required for login!
============================================================
```

### Share Link

Links include password token:
```
http://10.0.10.93:8765/view?path=/path/to/file.md&token=PASSWORD
```

### Access

1. Click link → Auto-authenticated
2. Password saved to cookie (30 days)
3. Future visits → Auto-authenticated via cookie

## 🔐 Authentication

### Link + Cookie
- **Links include token** - Easy sharing
- **Cookie saved on access** - 30 days
- **No re-login needed** - Cookie auto-authenticates

### Cookie Details
```
Set-Cookie: md_auth=PASSWORD; Path=/; Max-Age=2592000; HttpOnly; SameSite=Lax
```
- **30 days lifetime**
- **HttpOnly** - Cannot be accessed by JavaScript
- **SameSite=Lax** - CSRF protection

## 📖 E-ink Optimization

- **Light theme** - White background, black text
- **Serif fonts** - Georgia for comfortable reading
- **High contrast** - Clear borders and text
- **No animations** - Saves battery life

## 🛡️ Security

### Blocked Paths
```
❌ /etc/*, /proc/*, /sys/*, /dev/*, /var/log/*
❌ ~/.ssh/*, id_rsa, id_ed25519
❌ ~/.gnupg/*
❌ ~/.aws/*, ~/.gcp/*
❌ .netrc, .pgpass, .env
❌ *.pem, *.key, *.p12, *.pfx
```

### XSS Protection
- HTML sanitized with bleach library
- Only safe tags allowed
- JavaScript blocked

## 🔧 Configuration

```bash
python3 server.py [options]

Options:
  --host HOST          Host to bind (default: auto-detect LAN IP)
  --port PORT          Port (default: 8765)
  --password PASSWORD  Custom password (auto-generated if not set)
  --no-history         Disable history tracking for privacy
  --localhost          Bind to localhost only (no LAN access)
```

### Examples

```bash
# Default: Auto-detect and bind to LAN IP
python3 server.py

# Localhost only (no LAN access)
python3 server.py --localhost

# Custom port
python3 server.py --port 8080

# Disable history for privacy
python3 server.py --no-history
```

## 📦 Dependencies

```bash
pip3 install markdown bleach
```

## 🤝 Integration with AI Agents

The skill triggers when you say:
- "cho tôi xem file md"
- "show me the file"
- "xem file này"
- "mở file"

## 🔒 Notes

- **History enabled by default** - Use `--no-history` to disable
- **Auto LAN binding** - Use `--localhost` for localhost only
- **Token in URL** - For easy link sharing
- **Cookie 30 days** - No frequent re-login

## 🙏 Acknowledgments

- [markdown](https://github.com/Python-Markdown/markdown)
- [bleach](https://github.com/mozilla/bleach)
- [highlight.js](https://highlightjs.org/)
- [OpenClaw](https://openclaw.ai)

## 📄 License

MIT License