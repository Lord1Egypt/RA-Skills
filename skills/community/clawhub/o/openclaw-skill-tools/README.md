# OpenClaw Skill Generator & Security Scanner — OpenClaw Skill 🦞🔧

Generate and security-scan SKILL.md files via your OpenClaw agent.

## Quick Install

```bash
clawhub install openclaw-skill-tools
```

## Configuration

```json
{
  "skills": {
    "entries": {
      "openclaw-skill-tools": {
        "enabled": true,
        "env": {
          "TOOLWEB_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## Two Tools in One

**🔧 Skill Generator** — Create professional SKILL.md files from a description
**🔍 Security Scanner** — Scan skills for prompt injection, data exfiltration, credential theft, permission abuse, and scope creep

## Security Checks

- Prompt Injection detection
- Data Exfiltration patterns
- Credential Harvesting
- Excessive Permissions
- Metadata Anomalies
- Scope Creep analysis

## Example

```
You: Scan this skill before I install it: [pastes SKILL.md]

Agent: 🔍 Skill Security Scan
       🔴 CRITICAL: Hidden curl to external URL detected
       🟠 HIGH: Requests file system access beyond stated scope
       ✅ No credential harvesting found
       🛡️ Recommendation: DO NOT INSTALL
```

## Pricing

| Plan | Price/month | API Calls |
|------|------------|-----------|
| Free Trial | $0 | 10/day, 50/month |
| Developer | $39 | 20/day, 500/month |
| Professional | $99 | 200/day, 5000/month |
| Enterprise | $299 | 100K/day, 1M/month |

## License

MIT-0

---

*Built by a CISSP & CISM certified professional at [ToolWeb.in](https://toolweb.in)*
