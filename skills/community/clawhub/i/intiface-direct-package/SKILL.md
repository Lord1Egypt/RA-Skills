---
name: "intiface-direct"
description: "Control 750+ BLE intimate devices via Intiface Central using direct Buttplug v4 WebSocket protocol"
metadata: {"openclaw": {"requires": {"bins": ["node"], "skills": []}}}
---

# Intiface Direct — Buttplug v4 Device Control

Control any [Buttplug.io-compatible device](https://iostindex.com) — 700+ toys across all major brands — from natural language through OpenClaw. Connects directly to **Intiface Central** via WebSocket using the **Buttplug v4 protocol**. No MCP bridges, no unstable middleware.

The full agent-friendly SKILL.md is in `skills/intiface-direct/SKILL.md`. It includes:

- **🤖 Zero-to-Hero Guide** for any agent learning from scratch
- **🔧 Setup & Prerequisites** — Intiface Central, device pairing, dependencies
- **🔌 Connector Script** — CLI tool (`list`, `vibrate`, `loop`, `stop`)
- **📦 Buttplug v4 Protocol Reference** — exact JSON for handshake, device list, output commands
- **⚠️ Common Protocol Mistakes** — wrong vs. right JSON comparisons
- **🎵 Pattern Library** — Curren's massage, curren-massage, thrust, hard, deeper scripts with durations and auto-stop
- **🎨 Custom Pattern Templates** — two reusable patterns for agents to write their own sequences
- **🛠 Decision Framework** — connector vs. temp script
- **⚖️ Agent Rules & Safety** — permission, auto-stop, single-connection, no unattended operation
- **🧪 Troubleshooting** — 13 entries with likely causes and fixes
- **🌐 Remote Access** — LAN, WSL2 direct, socat tunnel

Key improvements over v1:
- Zero-to-Hero section for brand-new agents
- Pattern library documenting all scripts with auto-stop info
- Common protocol mistakes section
- Single-connection rule added
- Device persistence note (re-scan not needed each time)
- Path context note for Curren's scripts
- 500ms disconnect note on vibrate command
