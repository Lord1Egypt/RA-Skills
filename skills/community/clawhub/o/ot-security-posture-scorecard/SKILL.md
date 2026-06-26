---
name: ot-security-posture-scorecard
description: Assess OT/ICS/SCADA security posture and generate risk scorecards with remediation guidance. Use when evaluating operational technology security, industrial control system risks, SCADA vulnerabilities, OT-IT convergence gaps, IEC 62443 compliance, or NIST CSF alignment for critical infrastructure.
version: 1.0.0
homepage: https://portal.toolweb.in
metadata:
  openclaw:
    emoji: "🏭"
    requires:
      env:
        - TOOLWEB_API_KEY
      bins:
        - curl
    primaryEnv: TOOLWEB_API_KEY
    os:
      - linux
      - darwin
      - win32
    category: security
---

# OT Security Posture Scorecard 🏭🔒

Assess the security posture of Operational Technology (OT), Industrial Control Systems (ICS), and SCADA environments. Returns a detailed scorecard with risk ratings, gap analysis, and prioritized remediation steps aligned to IEC 62443 and NIST CSF frameworks.

**Built by a CISSP/CISM certified security professional at [ToolWeb.in](https://toolweb.in)**

## When to Use

- User asks to assess OT or ICS or SCADA security posture
- User wants to evaluate industrial control system risks
- User needs OT-IT convergence security analysis
- User asks about IEC 62443 or NIST CSF compliance for OT environments
- User mentions critical infrastructure security assessment
- User wants a security scorecard for manufacturing, energy, water, or utility systems

## Prerequisites

- `TOOLWEB_API_KEY` — Get your API key from [portal.toolweb.in](https://portal.toolweb.in)
- `curl` must be available on the system

## API Endpoint

```
POST https://portal.toolweb.in:8443/security/itotassessor
```

## Workflow

1. **Gather inputs** from the user. Ask for the following:

   **Required fields:**
   - `org_name` — Name of the organization (e.g., "Acme Manufacturing Corp")
   - `sector` — Industry sector (e.g., "Manufacturing", "Energy", "Water Treatment", "Oil & Gas", "Pharmaceuticals", "Transportation", "Mining")
   - `ot_size` — Size of OT environment (e.g., "Small", "Medium", "Large", "Enterprise")
   - `integration_level` — Level of IT/OT integration (e.g., "Minimal", "Partial", "Full", "Air-Gapped")
   - `csf_scores` — NIST CSF self-assessment scores (each 1-5). Ask the user to rate their maturity in each area:
     - `identify` — Asset management, risk assessment (1=none, 5=optimized)
     - `protect` — Access control, security training, data protection (1=none, 5=optimized)
     - `detect` — Monitoring, detection processes (1=none, 5=optimized)
     - `respond` — Incident response planning and execution (1=none, 5=optimized)
     - `recover` — Recovery planning and improvements (1=none, 5=optimized)

   **Optional fields (use if the user provides them):**
   - `ot_technologies` — List of OT technologies in use (e.g., ["SCADA", "PLC", "HMI", "DCS", "RTU"])
   - `it_tools` — List of IT security tools in use (e.g., ["Firewall", "SIEM", "IDS", "EDR"])
   - `threat_concern` — Primary threat concerns (e.g., "Ransomware targeting OT networks")
   - `compliance` — Target compliance framework (e.g., "IEC 62443", "NIST CSF", "NERC CIP")
   - `known_gaps` — Known security gaps (e.g., "No OT network monitoring, shared credentials on PLCs")
   - `team_maturity` — Security team maturity level (e.g., "No dedicated OT security team")
   - `assessment_depth` — Level of detail: "standard" (default) or "detailed"

2. **Call the API** with the gathered parameters:

```bash
curl -s -X POST "https://portal.toolweb.in:8443/security/itotassessor" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TOOLWEB_API_KEY" \
  -d '{
    "org_name": "<org_name>",
    "sector": "<sector>",
    "ot_size": "<ot_size>",
    "integration_level": "<integration_level>",
    "ot_technologies": ["<tech1>", "<tech2>"],
    "it_tools": ["<tool1>", "<tool2>"],
    "csf_scores": {
      "identify": <1-5>,
      "protect": <1-5>,
      "detect": <1-5>,
      "respond": <1-5>,
      "recover": <1-5>
    },
    "threat_concern": "<threat_concern>",
    "compliance": "<compliance>"
  }'
```

3. **Parse the response**. The API returns a JSON object with:
   - `status` — "success" or error status
   - `report` — Full markdown report containing executive summary, NIST CSF function analysis, top 5 priority risks, technology stack assessment, and step-by-step remediation roadmap
   - `overall_score` — Numeric score (0-100)
   - `csf_avg` — Average CSF score across all 5 functions
   - `risk_level` — Risk rating ("Critical", "High", "Medium", "Low")
   - `org_name` — Organization name echoed back

4. **Present results** to the user in a clear, structured format:
   - Lead with the overall score and risk level
   - Show the executive summary from the report
   - Highlight the top 5 priority risks
   - Present the remediation roadmap phases
   - Offer to dive deeper into any specific section

## Output Format

Present the scorecard as follows:

```
🏭 OT/IT Convergence Security Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Organization: [org_name]
Sector: [sector]
Overall Score: [overall_score]/100 — [risk_level]
CSF Average: [csf_avg]/5.0

[Extract and present key sections from the report field:]
- Executive Summary
- Top 5 Priority Risks (with severity)
- Phase 1 Quick Wins (0-30 days)
- Recommended Technology Additions

📎 Full detailed report available — ask me to show any section
```

**Note:** The `report` field contains a comprehensive markdown report. Present the most actionable sections first (executive summary, top risks, quick wins) and offer to show the full report or specific sections on request.

## Error Handling

- If `TOOLWEB_API_KEY` is not set: Tell the user to get an API key from https://portal.toolweb.in (plans start at ₹2,999/month or ~$36/month)
- If the API returns 401: API key is invalid or expired — direct user to portal.toolweb.in to check their subscription
- If the API returns 429: Rate limit exceeded — wait and retry after 60 seconds
- If the API returns 500: Inform user of a temporary service issue and suggest retrying in a few minutes
- If curl is not available: Suggest installing curl (`apt install curl` / `brew install curl`)

## Example Interaction

**User:** "Assess the security of our water treatment plant's SCADA system"

**Agent flow:**
1. Ask: "I'll need a few details to run the assessment:
   - What's your organization name?
   - How large is your OT environment? (Small/Medium/Large)
   - How integrated are your IT and OT networks? (Minimal/Partial/Full)
   - Can you rate your maturity (1-5) in these areas: Identify, Protect, Detect, Respond, Recover?"
2. User responds: "WaterCo Utilities, medium size, partial integration. Identify: 3, Protect: 2, Detect: 2, Respond: 1, Recover: 1"
3. Call API:
```bash
curl -s -X POST "https://portal.toolweb.in:8443/security/itotassessor" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TOOLWEB_API_KEY" \
  -d '{
    "org_name": "WaterCo Utilities",
    "sector": "Water Treatment",
    "ot_size": "Medium",
    "integration_level": "Partial",
    "ot_technologies": ["SCADA", "PLC", "HMI"],
    "csf_scores": {"identify":3,"protect":2,"detect":2,"respond":1,"recover":1}
  }'
```
4. Present the scorecard: overall score, risk level, executive summary, top risks, and quick wins

## Pricing

- API access via portal.toolweb.in subscription plans
- Free trial: 10 API calls/day, 50 API calls/month to test the skill
- Developer: $39/month — 20 calls/day and 500 calls/month
- Professional: $99/month — 200 calls/day, 5000 calls/month
- Enterprise: $299/month — 100K calls/day, 1M calls/month

##About

Created by **ToolWeb.in** — a security-focused MicroSaaS platform with 200+ security APIs, built by a CISSP & CISM certified professional. Trusted by security teams in USA, UK, and Europe and we have platforms for "Pay-per-run", "API Gateway", "MCP Server", "OpenClaw", "RapidAPI" for execution and YouTube channel for demos.

- 🌐 Toolweb Platform: https://toolweb.in
- 🔌 API Hub (Kong): https://portal.toolweb.in
- 🎡 MCP Server: https://hub.toolweb.in
- 🦞 OpenClaw Skills: https://toolweb.in/openclaw/
- 🛒 RapidAPI: https://rapidapi.com/user/mkrishna477
- 📺 YouTube demos: https://youtube.com/@toolweb-009


## Tips

- For the most actionable results, provide detailed descriptions of your OT environment
- Run assessments quarterly to track improvement over time
- Use the compliance mapping output directly for audit preparation
- Combine with the IT Risk Assessment Tool skill for a holistic IT+OT security view
