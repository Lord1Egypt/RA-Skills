---
name: lead-gen
description: Lead generation, prospecting, and qualification for B2B sales. Use when asked to find leads, build prospect lists, research target companies, qualify leads against an ICP, enrich contact data, find decision-maker email formats, scrape company info, score leads, or build a sales pipeline from scratch. Triggers on phrases like "find leads", "build a prospect list", "who should I target", "lead generation", "find decision makers", "ICP research", "sales prospecting", "qualify leads", "enrich contacts", "find emails", "pipeline building".
---

# Lead Generation Skill

Build targeted, qualified prospect lists and enrich them with decision-maker data. Output is pipeline-ready — not raw noise.

## Workflow

### 1. Define the ICP (Ideal Customer Profile)
Ask if not provided:
- **Industry/vertical:** (e.g. SaaS, e-commerce, professional services)
- **Company size:** (employees or revenue range)
- **Geography:** (country, region, or global)
- **Job titles to target:** (e.g. Head of Marketing, VP Sales, Founder)
- **Pain point or trigger event:** (e.g. recently funded, hiring for X role, using competitor Y)

### 2. Build the Target Company List
Use `web_search` with precision queries. See `references/search-playbook.md` for query templates.

Effective discovery sources:
- LinkedIn Sales Navigator signals (via search queries)
- G2/Capterra category pages (companies using specific software)
- Crunchbase (funded companies by stage, industry, date)
- Job boards (companies hiring = growing = buying)
- Industry directories and association member lists
- Subreddits and communities where ICP hangs out

### 3. Find Decision Makers
For each target company:
- Search `"[company] [job title] LinkedIn"` to identify names
- Use `web_search` to find personal/professional profiles
- Cross-reference company About/Team pages

### 4. Enrich Contacts
For each contact, gather:
- Full name, title, company
- LinkedIn URL
- Email format (guess from pattern: firstname@co.com, f.lastname@co.com)
- Company size, industry, location
- Recent trigger events (new role, funding, product launch)

Run `scripts/enrich_leads.py` to format and score the list.

### 5. Score & Prioritize
Score each lead 1–10 using the rubric in `references/scoring-rubric.md`:
- ICP fit (industry, size, title match)
- Buying signals (trigger events, tech stack, intent)
- Reachability (email confidence, LinkedIn activity)
- Timing (recently funded, new hire, Q1 budget cycle)

### 6. Output Format
Deliver as a CSV-ready table + summary:

| Name | Title | Company | Industry | Size | Email (est.) | LinkedIn | Score | Notes |
|---|---|---|---|---|---|---|---|---|

Include:
- Total leads found
- Score distribution
- Top 10 "strike now" leads highlighted
- Suggested outreach angle per segment

See `references/search-playbook.md` for advanced search query patterns.
See `references/email-formats.md` for common company email format patterns.
