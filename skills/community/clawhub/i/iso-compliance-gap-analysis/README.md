# ISO Compliance Gap Analysis — OpenClaw Skill 📜🔍

Multi-standard ISO gap analysis with a single message to your OpenClaw agent.

## Quick Install

```bash
clawhub install iso-compliance-gap-analysis
```

## Configuration

```json
{
  "skills": {
    "entries": {
      "iso-compliance-gap-analysis": {
        "enabled": true,
        "env": {
          "TOOLWEB_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## 3 Standards Supported

| Standard | Focus |
|----------|-------|
| ISO 27001 | Information Security Management |
| ISO 27701 | Privacy Information Management |
| ISO 42001 | AI Management Systems |

## 5 Assessment Areas (23 Questions)

Governance, Risk Management, Technical Controls, Privacy Controls, Documentation

## Example

```
You: Assess our ISO 27001 and 27701 readiness. We have basic
     security policies, annual risk assessments, MFA deployed,
     but no DPIAs or formal DSAR process.

Agent: 📜 ISO Compliance Gap Analysis
       Overall: 52%
       ISO 27001: 65% — Strong governance, weak documentation
       ISO 27701: 38% — No DPIAs, manual DSAR, no consent framework
       🎯 Action 1: Implement DPIA process for high-risk processing
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
