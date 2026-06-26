# 🤖 Jarvis — Chief of AI Staff

> Your always-on, local-first AI executive. Runs on Dell Pro Max GB10 (NVIDIA DGX Spark) with OpenClaw. Zero cloud bills. Zero data egress.

[![ClawHub](https://img.shields.io/badge/ClawHub-jarvis--chief--of--ai--staff-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20arm64-orange)](https://build.nvidia.com/spark/openclaw)

## Quick Install

```bash
clawhub install jarvis-chief-of-ai-staff
```

Then deploy the workspace:

```bash
bash ~/.openclaw/skills/jarvis-chief-of-ai-staff/scripts/deploy-workspace.sh
```

## What Is This?

Jarvis is a production-grade OpenClaw skill that transforms your agent into a **Chief of AI Staff** — a strategic, proactive AI executive that manages operations, communications, research, and business intelligence from your Dell Pro Max GB10.

Unlike generic assistant setups, Jarvis comes with:

- **Executive persona** — Acts as a COO, not a chatbot. Anticipates needs, surfaces problems, filters noise.
- **3-tier memory architecture** — Always-loaded identity + daily context + deep knowledge with semantic search.
- **Security-hardened deployment** — WhatsApp allowlists, sandbox mode, UFW firewall, SSL, and audit logging.
- **GB10 optimization** — Model selection guide, performance tips, and thermal management for 24/7 operation.
- **Sequential setup** — 5 phases, ~30 minutes from install to operational.

## Directory Structure

```
jarvis-chief-of-ai-staff/
├── SKILL.md                    # Main skill file (ClawHub format)
├── README.md                   # This file
├── LICENSE                     # MIT License
├── scripts/
│   ├── deploy-workspace.sh     # Deploys persona files to workspace
│   └── security-harden.sh      # Security audit + hardening
└── templates/
    ├── SOUL.md                 # Behavioral philosophy
    ├── IDENTITY.md             # Name, role, voice
    ├── USER.md                 # Your profile (edit this!)
    ├── MEMORY.md               # Long-term memory starter
    ├── AGENTS.md               # Operating instructions
    ├── HEARTBEAT.md            # Proactive checklist
    └── TOOLS.md                # Environment config
```

## Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Hardware | Any NVIDIA GPU with 16GB+ VRAM | Dell Pro Max GB10 (128GB) |
| OS | Linux (arm64 or x86_64) | Ubuntu on DGX Spark |
| OpenClaw | v1.0+ | Latest stable |
| LLM Backend | Ollama or LM Studio | Ollama with Qwen3.5-35B-A3B |
| Docker | v20+ | Latest (for SearXNG) |

## Security

This skill follows ClawHub security best practices:

- ✅ No network calls to external endpoints
- ✅ No obfuscated or encoded code
- ✅ No binary downloads or package installations
- ✅ No requests for API keys or credentials
- ✅ All shell scripts are readable and auditable
- ✅ Workspace files are plain Markdown
- ✅ All filesystem operations stay within OpenClaw workspace
- ✅ Security hardening script included (not required)

## Credits

**Author:** [Yogesh Huja](https://www.linkedin.com/in/yogeshhuja/) — Founder & CEO, Gignaati

**Book:** [Invisible Enterprises: How to Lead Better with People & AI Agents](https://www.invisible-enterprises.com/) — The best-selling guide for modern leaders.

**Powered by:** [Gignaati](https://gignaati.com) — Enterprise AI, accessible and local-first.

## License

MIT — Use freely, modify freely, attribute kindly. See [LICENSE](LICENSE).
