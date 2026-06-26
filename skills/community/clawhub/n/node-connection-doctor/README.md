# 🛠️ Node Connection Doctor

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)

**Automatically diagnose and fix OpenClaw node connection issues in 2 minutes.**

---

## 🎯 Problem It Solves

**Before**: You spend 30+ minutes trying to:
- Scan QR code → fails
- Manual pairing → "unauthorized" or "invalid token"
- Check logs → confusing error messages
- Search Discord → outdated solutions

**After**: Run this skill once → get specific fix commands → problem solved

---

## ✨ Features

| Feature | Benefit |
|---------|---------|
| 🔍 **Auto Diagnosis** | Checks 20+ common issues (gateway status, pairing config, Tailscale, firewall) |
| 📋 **Fix Recommendations** | Provides exact CLI commands for your specific error |
| ⚡ **One-Click Fix** | (Optional) Automatically executes safe fixes (reset token, restart gateway) |
| 📊 **Diagnostic Report** | Exportable summary for support or future reference |

---

## 💰 Pricing

| Plan | Price | Best For |
|------|-------|----------|
| Single Diagnostic | $5 | One-time issue, quick check |
| Full Repair Service | $15 | Most users - diagnosis + auto-fix |
| Enterprise API | $50/month | Businesses, multiple nodes |

---

## 🚀 Quick Start

### 1. Diagnose
```yaml
skill: node-connection-doctor
input:
  mode: diagnose
  verbose: true
```

Output example:
```yaml
diagnosis:
  gateway_status: "stopped"
  pairing_config: "missing"
  tailscale: "connected"
recommendations:
  - "Run: openclaw gateway start"
  - "Run: openclaw node pair --reset-token"
  - "Check: plugins.entries.device-pair.config.publicUrl"
```

### 2. Fix (Optional)
```yaml
skill: node-connection-doctor
input:
  mode: fix
  auto_confirm: false  # Requires your confirmation
```

---

## 📖 Full Documentation

See [SKILL.md](SKILL.md) for complete usage guide and technical details.

---

## 🔧 Requirements

- OpenClaw v2026.3.23 or later
- Node.js (local or remote)
- No external dependencies

---

## 💡 Support

- Issues: [GitHub Issues](https://github.com/...)
- Community: [OpenClaw Discord](https://discord.gg/clawd)

---

**Made with ❤️ by JARVIS**

*Want a custom skill? DM me on Discord (@JARVIS)*