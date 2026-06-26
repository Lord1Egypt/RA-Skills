# ISO 42001 AIMS Readiness Assessment — OpenClaw Skill 🤖📋

Assess your organization's ISO/IEC 42001:2023 AI Management System readiness with a single message to your OpenClaw agent.

## What It Does

Send a message like *"Check if we're ready for ISO 42001 certification"* via WhatsApp, Telegram, or Discord, and your OpenClaw agent will:

1. Gather details about your AI usage and governance
2. Call the ToolWeb.in Security API
3. Return a readiness score, gap analysis, and remediation roadmap
4. Map findings to ISO 42001 clauses and EU AI Act requirements

## Quick Install

```bash
# Via ClawHub
clawhub install iso42001-aims-readiness

# Or manually
mkdir -p ~/.openclaw/skills/iso42001-aims-readiness
cp SKILL.md ~/.openclaw/skills/iso42001-aims-readiness/
```

## Configuration

Add to your `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "iso42001-aims-readiness": {
        "enabled": true,
        "env": {
          "TOOLWEB_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## Get Your API Key

1. Visit [portal.toolweb.in](https://portal.toolweb.in)
2. Sign up for a plan (free trial: 10 API calls)
3. Copy your API key from the dashboard
4. Add it to your OpenClaw config as shown above

## Pricing

| Plan         | Price/month     | API Calls |
|-------------|----------------|-----------|
| Free Trial  | $0             | 10 calls  |
| Starter     | ₹2,999 (~$36)  | 500       |
| Professional| ₹9,999 (~$120) | 5,000     |
| Enterprise  | ₹49,999 (~$600)| Unlimited |

International users: Select PayPal at checkout for USD/EUR/GBP payments.

## Why ISO 42001?

- **EU AI Act** requires risk-based AI governance — ISO 42001 is the compliance framework
- **Enterprise clients** increasingly require AI governance certifications from vendors
- **Board-level visibility** — demonstrate responsible AI practices to stakeholders
- **Risk reduction** — identify and mitigate AI-specific risks before they become incidents

## Example Usage

```
You: Check our ISO 42001 readiness. We're a mid-size healthcare company 
     using AI for medical imaging. We have ISO 27001 but no AI policy.
     5 AI systems in production.

Agent: 🤖 ISO 42001 AIMS Readiness Assessment
       Organization: Your Healthcare Co
       Overall Score: 35/100 — DEVELOPING
       ...
       🚨 Critical Gap: No AI governance policy
       📋 Priority Action: Establish AI ethics committee within 30 days
```

## Support

- 📧 info@mkkpro.com
- 🌐 https://toolweb.in
- 🔌 https://portal.toolweb.in
- 📺 YouTube: https://youtube.com/@toolweb

## License

MIT-0 (as required by ClawHub)

---

*Built by a CISSP & CISM certified security professional at [ToolWeb.in](https://toolweb.in)*
