# OT Security Posture Scorecard — OpenClaw Skill 🏭🔒

Assess OT/ICS/SCADA security posture with a single message to your OpenClaw agent.

## What It Does

Send a message like *"Assess the OT security of our manufacturing plant"* via WhatsApp, Telegram, or Discord, and your OpenClaw agent will:

1. Gather details about your OT environment
2. Call the ToolWeb.in Security API
3. Return a detailed scorecard with risk ratings, gaps, and remediation steps
4. Map findings to IEC 62443 and NIST CSF frameworks

## Quick Install

```bash
# Via ClawHub
clawhub install ot-security-posture-scorecard

# Or manually
mkdir -p ~/.openclaw/skills/ot-security-posture-scorecard
cp SKILL.md ~/.openclaw/skills/ot-security-posture-scorecard/
```

## Configuration

Add to your `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "ot-security-posture-scorecard": {
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

## Industries Supported

- Manufacturing & Industrial
- Energy & Utilities
- Water Treatment
- Oil & Gas
- Pharmaceuticals
- Transportation & Logistics
- Mining & Extraction
- Food & Beverage Processing

## Frameworks Covered

- **IEC 62443** — Industrial Automation and Control Systems Security
- **NIST CSF** — Cybersecurity Framework
- **NERC CIP** — Critical Infrastructure Protection (energy sector)
- **ISA/IEC 62443** — Zones and Conduits model

## Example Usage

```
You: Assess the OT security posture of our oil refinery SCADA system.
     We're a large enterprise with partial IT-OT integration.
     CSF scores: Identify 4, Protect 3, Detect 2, Respond 2, Recover 1

Agent: 🏭 OT/IT Convergence Security Assessment
       Organization: Your Oil Refinery
       Overall Score: 45/100 — HIGH RISK
       CSF Average: 2.4/5.0
       ...
       🚨 Top Risk: Inadequate recovery capability for OT systems
       📋 Quick Win: Emergency backup of all PLC programs within 30 days
```

## Also Available

- **IT Risk Assessment Tool** — For IT infrastructure security
- **Data Breach Impact Calculator** — Estimate breach costs
- **ISO Compliance Gap Analysis** — ISO 27001/42001 readiness
- **Threat Assessment & Defense Guide** — Threat modeling

All available as OpenClaw skills from ToolWeb.in.

## Support

- 📧 info@mkkpro.com
- 🌐 https://toolweb.in
- 🔌 https://portal.toolweb.in
- 📺 YouTube: https://youtube.com/@toolweb

## License

MIT-0 (as required by ClawHub)

---

*Built by a CISSP & CISM certified security professional at [ToolWeb.in](https://toolweb.in)*
