# Security Team

**Your AI security operations center, on autopilot.**

Stop guessing if your apps are secure, your servers are up, or your memory system is healthy. Security Team is a three-council audit system that scans your entire OpenClaw environment for vulnerabilities, downtime, and context drift — alerting you only when something actually needs your attention.

Free and open-source. Zero subscriptions. 100% private.

---

## Features

- **Silent Guardian Alerts:** No "all clear" spam. Security Team stays completely silent unless it finds a real issue. Your notifications are sacred.
- **Three-Council Audit System:**
 - 🛡️ **Security Council:** Scans for exposed API keys, npm vulnerabilities, dangerous file permissions, missing security headers, and secrets leaked in git history.
 - ⚙️ **Platform Council:** Pings your web apps, checks service uptime (Ollama, Qdrant, databases), monitors disk usage, and flags uncommitted repo changes.
 - 🧠 **Memory Monitor:** Validates your AI memory systems — MEMORY.md bloat, daily note gaps, vector DB health, and index freshness.
- **Accepted Risk Management:** Flagged a CORS issue on your dev server? Mark it as "accepted risk" and Security Team stops bothering you about it.
- **Trend Reporting:** Weekly and monthly security posture summaries with trend indicators.
- **Cross-Platform:** Works on macOS and Linux. Scripts auto-detect your OS.
- **Graceful Degradation:** Missing `ripgrep`? Falls back to `grep`. No `npm`? Skips dependency audit. No vector DB? Skips memory checks. It works with what you have.

## What's Included

```
security-team/
 SKILL.md — Agent operating manual (the brain)
 SETUP-PROMPT.md — First-run setup guide
 README.md — This file
 SECURITY.md — Audit & security guarantees
 config/
 security-config.json — Scan targets, thresholds, schedules
 scripts/
 security-scan.sh — Production security scanner
 platform-health.sh — Infrastructure health checker
 examples/
 security-audit-example.md
 platform-check-example.md
 memory-health-example.md
 dashboard-kit/
 DASHBOARD-SPEC.md — Dashboard Builder companion spec
```

## Quick Start

1. **Copy** the `security-team/` folder into your workspace `skills/` directory.
2. **Tell your agent:** "Read the SETUP-PROMPT.md file in the security-team skill and follow the instructions."
3. **Watch the baseline scan** find things you forgot about. 🛡️

That's it. Three steps. Your infrastructure just got a night shift.

## Security & Privacy

![Codex Security Verified](https://img.shields.io/badge/Codex-Security_Verified-blue)

- **Read-only by design** — Security Team observes and reports. It never modifies your files, configs, or infrastructure.
- **No data exfiltration** — Everything runs locally. Your secrets, architecture details, and scan results never leave your machine.
- **Secret redaction** — Even in reports, discovered secrets are redacted (first 6 chars + `***`). Raw values are never echoed.
- **Strict file permissions** — All data files use `chmod 600`, directories use `chmod 700`.

## Requirements

- OpenClaw agent with `exec` and `read` tool access
- `bash` (v4+)
- `curl` (for endpoint health checks)
- Optional: `ripgrep` (faster secret scanning — falls back to `grep`)
- Optional: `npm` or `yarn` (for dependency audit)
- Optional: `openssl` (for SSL cert expiry checks)
- Optional: `qmd` (for memory index freshness)

## Pairs Perfectly With

## Support

Check the `examples/` directory for usage patterns. Questions? Visit [normieclaw.ai](https://normieclaw.ai).
