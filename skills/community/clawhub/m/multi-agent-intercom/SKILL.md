---
name: multi-agent-intercom
description: Enables peer-to-peer cross-communication between isolated OpenClaw agents. Resolves the limitation of `sessions_send` which cannot cross agent boundaries. 100% Zero-Intrusive, safe, compliant, with zero console popups and robust multiline support.
when: "When the user mentions 'multi-agent-intercom', 'intercom', or requests to send a message to another agent. CRITICAL: If this is the very first time using this skill, you MUST run the setup script (`python <SKILL_DIR>/scripts/intercom.py setup`) to generate the protocol SOP, then ask the human user to manually paste it into each agent's AGENTS.md file."
examples:
  - "安装 multi-agent-intercom"
  - "初始化对讲机"
  - "给老程发个消息"
  - "Tell dev to update the avatars."
metadata:
 {
   "openclaw": {
     "requires": { "bins": ["python3", "python", "openclaw"], "anyBins": ["python3", "python"] },
     "emoji": "🗣️",
     "primaryEnv": null
   }
 }
---

# Multi-Agent Intercom

🗣️ **A powerful, secure, and zero-intrusive peer-to-peer communication skill for OpenClaw.**

This skill enables independent OpenClaw agents (e.g., `zz`, `dev`, `rc`) to securely send messages and wake up each other across isolated workspaces. It acts as an asynchronous "intercom system" for your Multi-Agent setup.

---

## 🚀 Quick-Start Instructions

### 1. Initialization (First Time Setup — One-Time Manual Step)

Run the setup script to generate the communication protocol SOP:
```bash
python <SKILL_DIR>/scripts/intercom.py setup
```

**⚠️ Important:** The script will print an SOP block to the screen — it does **NOT** auto-write any files. **You must manually copy the printed SOP block and paste it at the bottom of each agent's `AGENTS.md` file.** After pasting, type `/new` in your chat to reload their brains.

### 2. Send a Message

Determine the target agent's ID and your own ID, then run:
```bash
python <SKILL_DIR>/scripts/intercom.py send <TARGET_AGENT_ID> <YOUR_AGENT_ID> "<YOUR_MESSAGE>"
```
*Note: This script runs asynchronously in the background. It will return immediately. Do not wait or retry.*

### 3. Example (You are 'zz', telling 'dev' to update avatars)

```bash
python <SKILL_DIR>/scripts/intercom.py send dev zz "Hi dev, the Boss wants us to update our avatars today. Acknowledge when done."
```

When 'dev' receives this, the message will be formatted as `[From Agent zz] Hi dev, the Boss wants us to update our avatars today...` — the SOP embedded in `AGENTS.md` tells 'dev' exactly how to respond.

---

## 🌟 Why is this needed?

By design, OpenClaw agents run in isolated databases and sandboxes. The built-in `sessions_send` tool can only send messages within an agent's own subagent hierarchy. If Agent A tries to use `sessions_send` to message Agent B, it will result in a "Session not found" error.

**Multi-Agent Intercom** solves this by leveraging the native `openclaw agent` CLI mechanism to safely bridge these isolated environments, allowing agents to act as equal peers in a decentralized company.

## 🛡️ Security First: Zero-Intrusive & 100% Compliant

- **No File Tampering**: Does NOT automatically modify or rewrite any system files. You remain in full control.
- **No Shell Injection**: Safe subprocess argument lists prevent RCE vulnerabilities.
- **True Silent Execution**: Uses `CREATE_NO_WINDOW` + `close_fds` on Windows for zero console popups.
- **Anti-Loop Breaker**: The protocol prevents infinite "Received → Thank you" loops.

## ✨ Features

- **Cross-Boundary Messaging** — reach any agent on the same system
- **Robust Multiline Support** — bypasses Windows `cmd.exe` argument truncation via PowerShell routing
- **Internationalization (i18n)** — auto-detects OS language (English / Chinese)
- **Immediate Wake-up** — bypasses sleep states, forces target to process now
- **Persistent Context** — targets the `main` session by default

## ⚠️ Command Reference

| Command | What it does |
|---------|-------------|
| `python intercom.py setup` | Prints the SOP block for manual copy-paste into AGENTS.md |
| `python intercom.py send <target> <sender> "<msg>"` | Sends a message to another agent |

> **Note:** There is NO `install` subcommand. Use `setup` to generate the SOP.

## Requirements
- OpenClaw >= 2026.x
- Python 3.x

---
*Created for the OpenClaw / ClawDBot community.*
