---
name: lead-gen-research
description: Qualify sales prospects from company lists with social profiling, trigger event research, and personalized outreach angles. Saves 10+ hours/week on manual prospect research.
metadata:
  version: 1.0.0
  author: TKDigital
  category: Sales & Marketing
  tags: [lead generation, sales, prospecting, outreach, CRM, B2B]
---

# Lead Gen Research Skill

Transforms raw company/contact lists into qualified prospect profiles with actionable outreach angles.

## What It Does

Given a list of companies or contacts, this skill:

1. **Social Profiling** — Pulls public info from LinkedIn, X/Twitter, company sites
2. **Trigger Event Detection** — Identifies recent hiring, funding, product launches, leadership changes
3. **Pain Point Mapping** — Matches prospect profile to common pain points in their industry
4. **Outreach Angle Generation** — Creates 2-3 personalized opening lines per prospect
5. **Scoring** — Ranks prospects by likelihood to convert (1-10 scale)

## Usage

### Basic Prospect Research
```
Research these companies for sales outreach:
- Acme Corp (SaaS, Series B)
- Widget Labs (E-commerce, 50 employees)
- DataFlow Inc (Analytics, bootstrapped)

Focus on: content marketing pain points
Our offer: AI-powered content production service
```

### Deep Dive Single Prospect
```
Deep research this prospect:
Company: [Company Name]
Contact: [Name, Title]
Our service: [What we sell]
Give me: trigger events, pain points, 3 personalized email openers
```

### Batch CSV Processing
```
Process this CSV of leads. For each row:
1. Score fit (1-10) based on company size, industry, recent activity
2. Find 1 trigger event
3. Write 1 personalized opening line
4. Flag top 20% as priority outreach

CSV columns: company_name, industry, employee_count, contact_name, contact_title
```

## Output Format

For each prospect:
```
## [Company Name] — Score: [X/10]

**Profile**: [Industry] | [Size] | [Stage] | [Location]
**Trigger Event**: [Recent event that creates urgency]
**Pain Points**: [2-3 likely pain points based on profile]
**Outreach Angles**:
1. [Personalized opener referencing trigger event]
2. [Value prop aligned to pain point]
3. [Social proof / mutual connection angle]

**Recommended Channel**: [Email / LinkedIn / X DM]
**Priority**: [High / Medium / Low]
```

## Best Practices

- Provide your **offer/service description** for better angle generation
- Include **industry context** for more relevant pain points
- Works best with 5-50 prospects per batch (quality vs speed tradeoff)
- Pair with the cold-email-sequence skill for full outreach automation

## References

- `references/scoring-criteria.md` — How prospects are scored
- `references/industry-triggers.md` — Common trigger events by industry
- `references/outreach-templates.md` — Template library for follow-ups
