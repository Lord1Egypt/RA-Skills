# Skill Vetter Report: openclaw-security-audit

═══════════════════════════════════════
Skill: openclaw-security-audit
Source: Community / Open Source
Author: Community
Version: 1.0.0
License: MIT
───────────────────────────────────────
METRICS:
• Files: 6
• Code Size: ~35KB
• Last Updated: 2026-03-19
───────────────────────────────────────
RED FLAGS: None

PERMISSIONS NEEDED:
• Files: Read ~/.openclaw, Write ~/.openclaw/security-reports
• Network: None
• Commands: None
• System: None
───────────────────────────────────────
RISK LEVEL: 🟢 LOW

VERDICT: ✅ SAFE TO SHARE

NOTES:
- Purely defensive security tool
- No external network calls
- No credential hardcoding
- Uses generic paths (~/.openclaw)
- Creates backups before changes
- Masks sensitive data in reports
- MIT licensed for open sharing
═══════════════════════════════════════

## Files Included

| File | Purpose | Size |
|------|---------|------|
| SKILL.md | Skill documentation | 4,415 bytes |
| audit.py | Security scanner | 15,203 bytes |
| harden.py | Credential hardening | 13,947 bytes |
| config.json | Scan configuration | 521 bytes |
| _meta.json | Skill metadata | 557 bytes |
| README.md | Quick start guide | 823 bytes |

## Features

1. **Security Audit** - Scan for sensitive files and credential exposure
2. **Gateway Check** - Verify bind mode and authentication
3. **Credential Hardening** - Migrate credentials to environment variables
4. **JSON Reports** - Generate detailed audit reports
5. **Cross-platform** - Windows, macOS, Linux support

## Privacy & Safety

✅ Only reads OpenClaw configuration
✅ Does not transmit data externally
✅ Masks credential values in reports
✅ Creates backups before modifications
✅ Respects file permissions

❌ No hardcoded credentials
❌ No external network calls
❌ No system file modifications
❌ No elevated permissions required

## Installation

```bash
cd ~/.openclaw/skills
git clone <repo> openclaw-security-audit
```

## Usage

```bash
# Run security audit
python ~/.openclaw/skills/openclaw-security-audit/audit.py

# Harden credentials
python ~/.openclaw/skills/openclaw-security-audit/harden.py
```

## ClawHub Ready

This skill is ready for publication on ClawHub with:
- Clean, documented code
- No privacy leaks
- No security risks
- MIT license
- Community-friendly

---

Report generated: 2026-03-19
