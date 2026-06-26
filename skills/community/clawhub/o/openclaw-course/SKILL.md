# openclaw-course

Searchable reference for the OpenClaw Masterclass — 7 modules covering installation, configuration, local AI, VPS deployment, security, and skill development.

---

## When to Use

Use this skill when the user asks about:

- Installing or configuring OpenClaw
- Setting up SOUL.md, IDENTITY.md, USER.md, AGENTS.md, HEARTBEAT.md
- Local AI with Ollama
- VPS deployment and remote access
- Security hardening
- Cost optimization strategies
- Creating custom skills
- Troubleshooting gateway or connection issues
- Agent orchestration (Codex, Claude Code, OpenCode)

---

## Quick Reference

| Module | File | Topics |
|--------|------|--------|
| 1 - Foundations | `01-FOUNDATIONS.md` | Installation, first setup, messaging bridges |
| 2 - Soul Architecture | `02-THE-SOUL-ARCHITECTURE.md` | SOUL.md, IDENTITY.md, USER.md, AGENTS.md |
| 3 - Local Power | `03-LOCAL-POWER.md` | Ollama, voice, vision, agentic coding |
| 4 - Context & Costs | `04-CONTEXT-AND-COSTS.md` | Cost optimization, model selection |
| 5 - VPS Employee | `05-VPS-EMPLOYEE.md` | VPS deployment, Tailscale, cron jobs |
| 6 - Security | `06-SECURITY.md` | Hardening, secrets management |
| 7 - Skills & Future | `07-SKILLS-AND-FUTURE.md` | Creating skills, best practices |

---

## Examples

**User:** "How do I configure the Soul file?"
→ Search Module 2, return SOUL.md section with templates and examples

**User:** "Troubleshoot gateway not starting"
→ Search Module 1, return troubleshooting section with diagnostics

**User:** "Set up Ollama locally"
→ Search Module 3, return Ollama setup steps and configuration

**User:** "VPS deployment guide"
→ Search Module 5, return VPS setup instructions

**User:** "Cost optimization tips"
→ Search Module 4, return cost-saving strategies

**User:** "Create a custom skill"
→ Search Module 7, return skill development guide

**User:** "Security best practices"
→ Search Module 6, return hardening checklist

---

## Search Keywords

### Installation & Setup
- `install`, `installation`, `setup`, `getting started`
- `gateway`, `start`, `stop`, `status`
- `telegram`, `whatsapp`, `slack`, `discord`, `imessage`
- `docker`, `systemd`, `service`

### Configuration Files
- `SOUL.md`, `soul`, `personality`, `identity`
- `IDENTITY.md`, `who you are`, `name`, `avatar`
- `USER.md`, `human`, `preferences`, `about me`
- `AGENTS.md`, `rules`, `boundaries`, `red lines`
- `HEARTBEAT.md`, `proactive`, `cron`, `schedule`

### Local AI
- `ollama`, `local model`, `llama`, `mistral`
- `whisper`, `voice`, `speech`, `audio`
- `comfyui`, `image generation`, `vision`
- `codex`, `claude code`, `opencode`, `coding agent`

### VPS & Remote
- `vps`, `server`, `deploy`, `remote`
- `tailscale`, `vpn`, `secure access`
- `cron`, `systemd`, `24/7`, `always on`

### Costs & Optimization
- `cost`, `pricing`, `budget`, `cheap`
- `token`, `context`, `compression`, `summarize`
- `routing`, `fallback`, `model selection`

### Security
- `security`, `harden`, `protect`, `secrets`
- `ssh`, `firewall`, `fail2ban`, `updates`
- `privacy`, `data`, `encryption`

### Skills Development
- `skill`, `create skill`, `custom skill`
- `SKILL.md`, `manifest`, `clawhub`
- `references`, `scripts`, `index.js`

---

## Usage

```bash
# Use via OpenClaw skill system
# The skill automatically searches course content based on user queries

# Or use the CLI directly:
node index.js search "how to install OpenClaw"
node index.js search "SOUL.md example"
node index.js search "VPS setup"
```

---

## File Structure

```
skills/openclaw-course/
├── SKILL.md              # This manifest
├── index.js              # Search functionality
└── references/           # Course modules
    ├── README.md         # Course overview
    ├── 01-FOUNDATIONS.md
    ├── 02-THE-SOUL-ARCHITECTURE.md
    ├── 03-LOCAL-POWER.md
    ├── 04-CONTEXT-AND-COSTS.md
    ├── 05-VPS-EMPLOYEE.md
    ├── 06-SECURITY.md
    └── 07-SKILLS-AND-FUTURE.md
```

---

## Course Overview

The OpenClaw Masterclass is a comprehensive 7-module course that teaches you to build an autonomous AI workforce:

1. **Foundations** — Install OpenClaw, understand core concepts, set up messaging bridges
2. **Soul Architecture** — Configure your agent's personality and operational rules
3. **Local Power** — Run local AI models, add voice/vision, orchestrate coding agents
4. **Context & Costs** — Optimize for cost without sacrificing capability
5. **VPS Employee** — Deploy a 24/7 agent on a VPS with secure remote access
6. **Security** — Harden your infrastructure and manage secrets safely
7. **Skills & Future** — Create custom skills and prepare for what's next

---

*Part of the OpenClaw Masterclass — Build Your Autonomous AI Workforce*
