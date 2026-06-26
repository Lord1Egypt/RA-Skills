---
name: jarvis-browser-setup
description: "Setup Jarvis Browser Control System for new users. Generates unique WebSocket auth token, configures server, and prepares extension files. Use when user wants to share the browser control system with others or setup a new instance. Fully automated - no manual steps required, OpenClaw handles everything."
---

# Jarvis Browser Setup

Setup Jarvis Browser Control System v3.5 for new users with **fully automated** token generation.

## When to Use

Use this skill when:
- User wants to share browser control with someone else
- Setting up a new instance for another user
- Need to generate new unique auth token
- Preparing distributable package

## Key Feature: FULLY AUTOMATED 🎯

**The user just says:**
```
"Setup Jarvis Browser for me"
```

**And OpenClaw automatically:**
1. 🔑 Generates unique auth token
2. 📦 Creates server config
3. 🚀 Starts WebSocket server
4. ⚙️  Prepares extension files
5. ✅ Provides ready-to-use setup

**No manual steps required!**

## For OpenClaw Users (Recommended)

```bash
# Install skill
clawhub install jarvis-browser-setup

# Then just say:
"Setup Jarvis Browser for me"
# OpenClaw does everything automatically!
```

## For Manual Setup

```bash
python3 ~/.openclaw/workspace/skills/jarvis-browser-setup/scripts/setup.py
```

## Output

- `config.json` - Token & IP configuration
- `server/` - Python WebSocket server (auto-started)
- `extension/` - Pre-configured Chrome extension
- `README.md` - Setup instructions

## Token Format

- 48 random characters (cryptographically secure)
- Example: `XsJ3N-mAtusZ+WSPr0Ca!ExnVdQ8UuGd8J9PCwo9l8bmX3ACylw6Nv`
- Unique per user

## Security

- Each user gets unique token
- Token never shared between users
- Server validates token on every connection

## Requirements

- Python 3.8+
- Chrome/Edge browser
- Port 8765 available

