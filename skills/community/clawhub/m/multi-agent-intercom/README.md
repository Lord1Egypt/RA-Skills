# Multi-Agent Intercom (multi-agent-intercom)

🗣️ **A powerful, secure, and zero-intrusive peer-to-peer communication skill for OpenClaw.**

This skill enables independent OpenClaw agents (e.g., `zz`, `dev`, `rc`) to securely send messages and wake up each other across isolated workspaces. It acts as an asynchronous "intercom system" for your Multi-Agent setup.

## 🌟 Why is this needed?
By design, OpenClaw agents run in isolated databases and sandboxes. The built-in `sessions_send` tool can only send messages within an agent's own subagent hierarchy. If Agent A tries to use `sessions_send` to message Agent B, it will result in a "Session not found" error.

**Multi-Agent Intercom** solves this by leveraging the native `openclaw agent` CLI mechanism to safely bridge these isolated environments, allowing agents to act as equal peers in a decentralized company.

## 🛡️ Security First: Zero-Intrusive & 100% Compliant
This skill was designed with absolute security compliance in mind:
- **No File Tampering**: It does NOT automatically modify or rewrite any of your system files (like `openclaw.json` or `AGENTS.md`). The user remains in full control.
- **No Shell Injection**: Safe subprocess argument lists prevent any RCE vulnerabilities.
- **True Silent Execution**: Uses native Python `CREATE_NO_WINDOW` and clean handle detachment (`close_fds`) on Windows to guarantee absolutely zero console popups when sending background messages.
- **Anti-Loop Breaker**: The protocol explicitly prevents AI agents from engaging in infinite "Received -> Thank you" loops.

## ✨ Features
- **Cross-Boundary Messaging**: Send instructions or notifications to any agent on the same system.
- **Robust Multiline Support**: Bypasses the infamous Windows `cmd.exe` argument truncation bug by intelligently routing commands through PowerShell (`.ps1`) when necessary, ensuring long, multi-paragraph messages are delivered intact.
- **Internationalization (i18n)**: Automatically detects the OS language and generates SOPs/Caller IDs in either English or Chinese.
- **Immediate Wake-up**: Bypasses sleep states and forces the target agent to process the message immediately.
- **Persistent Context**: Targets the `main` session by default, ensuring long-term context is preserved.

## 📦 Installation & Setup

1. Extract the folder into your `~/.openclaw/skills/` directory.
2. Ensure the OpenClaw CLI (`openclaw`) is accessible in your system's PATH.

**One-Time Setup (Manual Copy-Paste Required):**

The setup script does NOT auto-write files. It only prints an SOP block — you copy and paste it manually:

```bash
python scripts/intercom.py setup
```

The script will output an SOP block. **Manually paste that block** into each agent's `AGENTS.md` file, then type `/new` in your chat to reload their brains.

> ⚠️ There is NO `install` subcommand. The script only has `setup` (print SOP) and `send` (deliver message).

## 🚀 How Agents Use It

Agents can use this skill autonomously when they determine they need to contact another agent. The scripts execute asynchronously and safely in the background.

**To send a message:**
```bash
python scripts/intercom.py send <TARGET_ID> <SENDER_ID> "Your message here"
```

**Example (Agent 'zz' messaging 'dev'):**
```bash
python scripts/intercom.py send dev zz "Hi dev, the user wants us to update our avatars. Please acknowledge."
```

When 'dev' receives this, the message is formatted as:
`[From Agent zz] Hi dev, the user wants us to update our avatars...`

The SOP pasted into `AGENTS.md` tells 'dev' exactly how to reply using the same tool.

## ⚠️ Command Reference

| Command | What it does |
|---------|-------------|
| `python intercom.py setup` | Prints the SOP block for manual copy-paste into AGENTS.md |
| `python intercom.py send <target> <sender> "<msg>"` | Sends a message to another agent |

## Requirements
- OpenClaw >= 2026.x
- Python 3.x

---
*Created for the OpenClaw / ClawDBot community.*
