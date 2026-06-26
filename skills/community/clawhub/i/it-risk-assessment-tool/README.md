# IT Risk Assessment Tool — OpenClaw Skill ⚡🔍

Comprehensive IT risk scoring across 6 domains with a single message to your OpenClaw agent.

## Quick Install

```bash
clawhub install it-risk-assessment-tool
```

## Configuration

```json
{
  "skills": {
    "entries": {
      "it-risk-assessment-tool": {
        "enabled": true,
        "env": {
          "TOOLWEB_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## 6 Security Domains Assessed

| Domain | Controls |
|--------|----------|
| 🏗️ Infrastructure | Segmentation, Firewall, Patching |
| 🔒 Data Protection | Classification, Encryption, Backup |
| 🔑 Access Control | MFA, PAM, Access Reviews |
| 📋 Compliance | Policies, Regulatory, Training |
| 🚨 Incident Response | IR Plan, Monitoring, Threat Intel |
| 🤝 Vendor Risk | Assessment, Contracts, Monitoring |

## Example

```
You: Run an IT risk assessment. We have basic firewalls, no MFA,
     monthly patching, encrypted data in transit, no IR plan.

Agent: ⚡ IT Risk Assessment
       Overall Score: 35/100 — HIGH RISK
       🚨 Access Control: Critical (no MFA)
       🚨 Incident Response: Critical (no IR plan)
       📋 Action 1: Implement MFA across all access points
```

## Pricing

| Plan | Price/month | API Calls |
|------|------------|-----------|
| Free Trial | $0 | 10 calls |
| Starter | ₹2,999 (~$36) | 500 |
| Professional | ₹9,999 (~$120) | 5,000 |
| Enterprise | ₹49,999 (~$600) | Unlimited |

International: Select PayPal at checkout for USD/EUR/GBP.

## License

MIT-0

---

*Built by a CISSP & CISM certified professional at [ToolWeb.in](https://toolweb.in)*
