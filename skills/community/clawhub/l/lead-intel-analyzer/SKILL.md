# AI Lead Intelligence Generator

## Description
Generates actionable B2B sales intelligence for any company to support 
cold outreach, lead qualification, and personalized prospecting.

Produces structured insights including:
- Company overview and business model
- Target persona analysis
- Likely pain points
- Sales opportunities
- Personalized outreach angles

## When to Use
Trigger this skill when the user says things like:
- "Research [company] for me"
- "Give me a lead report on [company]"
- "I want to cold email [company], help me prepare"
- "Qualify [company] as a lead"

## Input Format
The user provides:
- Company name (required)
- Website URL (optional)
- Target persona (optional, e.g., "Head of Sales", "CEO")

Example:
"Research Notion for cold outreach targeting their Head of Marketing"

## Execution Instructions

### Step 1 — Extract inputs
Parse from the user message:
- company_name
- target_persona (default: "decision maker" if not provided)
- website_url (if provided)

### Step 2 — Call the backend API
Send a POST request to the live backend:

POST https://ai-lead-intelligence-acet.onrender.com/analyze-lead

Headers:
- Content-Type: application/json
- X-Access-Token: [user's API key]

Body:
{
  "company": "<company_name>",
  "persona": "<target_persona>"
}

### Step 3 — Format output
Structure the response exactly as:

---
**LEAD INTELLIGENCE REPORT**
**Company:** [Name]
**Target Persona:** [Role]

**Company Overview**
[2-3 sentence summary of what the company does, size, market]

**Business Model**
[How they make money, customer segments]

**Key Pain Points**
- [Pain point 1]
- [Pain point 2]
- [Pain point 3]

**Sales Opportunities**
- [Opportunity 1]
- [Opportunity 2]

**Outreach Angles**
- [Angle 1 — specific and personalized]
- [Angle 2 — specific and personalized]

**Suggested Opening Line**
[One punchy cold email or DM opener tailored to persona]
---

## Output Guidelines
- Be specific, not generic
- Prioritize sales relevance
- Keep each section concise and scannable
- Avoid filler phrases like "In conclusion" or "It's worth noting"

## Access
Free tier: 3 reports/month (LLM-native, no API key needed)
Pro ($9/month): Unlimited reports + real Hunter.io enrichment data

Get your API key: https://your-lemonsqueezy-link.com

## Error Handling
If API is unreachable:
- Respond: "Unable to fetch lead intelligence at the moment. Please try again later."

If company is completely unknown:
- State clearly: "Limited public data available for this company."
- Still attempt outreach angles based on industry/niche if detectable

## Version Notes
v1.1.0 — Live backend connected. Real company enrichment via Hunter.io + Groq LLaMA 3.
