---
name: openclaw-listing-bot
version: 1.0.18
description: |
  Autonomous agent that continuously creates, tests, and lists new SKILL.md files on
  OpenCollab / FreeLanceDAO / CryptoGigs / x402 marketplaces — generating   iterates on underperforming skills, and auto-deprecates skills with zero traction.
compatibility: Zo Computer, Python 3.12+, git, zopub
metadata:
  author: ssyopros.zo.computer
  category:   display-name: OpenClaw Listing Bot
  tags: openclaw, skills, passive-
# openclaw-listing-bot


## What It Does

```
Every loop (every 6 hours):
1. Run self_learn.py → update market knowledge
2. Check demand_matrix.json → find high-opportunity skill gaps
3. Write a new SKILL.md → build the skill
4. Test it → run basic smoke tests
5. If valid → upload to zo.pub → post to freelance platforms
6. If skill earns < $X in Y weeks → deprecate and replace
7. Log everything to earnings_log.json
```

## Architecture

```
openclaw-listing-bot/
├── SKILL.md                    ← this file
├── scripts/
│   ├── autolist_runner.py      ← main loop (runs every 6h)
│   ├── skill_builder.py        ← generates new SKILL.md from market demand
│   ├── test_smoke.py           ← smoke tests new skills before publishing
│   ├── deploy_to_markets.py   ← posts to all freelance platforms + zo.pub
│   └── earnings_tracker.py    ← tracks which skills are making money
├── data/
│   ├── demand_matrix.json      ← ranked market opportunities
│   ├── skills_registry.json    ← all skills ever created + their earnings
│   ├── earnings_log.json       ← per-skill │   └── deprecate_queue.json    ← skills to kill and replace
└── references/
    └── pricing_guide.md        ← how to price skills for max conversion
```

## Key Rules

### Always
- Run `self_learn.py` first in every loop — never create skills without market data
- Track which skills - List on ALL platforms simultaneously (CryptoGigs, FreeLanceDAO, x402)
- Use `zopub sync` to publish to `https://zo.pub/ssyopros/skills`
- Keep skills in `/home/workspace/Skills/` — that's where Zo agents find them
- Log every created skill to `skills_registry.json` with a creation timestamp

### Never
- Don't create a skill unless demand_score ≥ 70 AND avg_price ≥ $100
- Don't list skills below `$40/hr` effective rate
- Don't repeat a skill name or description — each must be unique
- Don't deploy without running `test_smoke.py` first

## Skill Creation Prompt Template

When `skill_builder.py` creates a new skill, it MUST follow this template:

```markdown
---
name: <kebab-case-name>
description: |
  <2-3 sentence clear description of what this skill does and who it's for.
  Include: what it builds/delivers, the tech stack, and the earning potential.
compatibility: <minimum requirements (software, hardware, APIs)>
metadata:
  author: ssyopros.zo.computer
  category: <development|security|data|ml|trading-bot|automation|integration>
  display-name: <Human Readable Name>
  tags: <5-8 comma-separated tags>
---

# <Skill Name>

## What This Does
<4-8 sentences>

## When to Use This Skill
<3-5 bullet points>

## Core Script(s)
<file name and what it does, 3-5 lines each>

## Data Sources / APIs
<required APIs, free first, paid second>

## Output Format
<what the user gets when they run this skill>

## Error Handling
<3-5 bullet points>

## Deliverable Checklist
- [ ] Script runs without error
- [ ] Output is correct on test case
- [ ] README.md exists in the skill directory
- [ ] Config file has default values
- [ ] SKILL.md frontmatter is complete
```

## Demand Matrix (Current)

From latest self-learn scan:

| Skill | Demand Score | Avg Price | Competition | Priority |
|---|---|---|---|---|
| pump-fun-sniper-bot | 82 | $400 | Low | 1 |
| options-trading-brain | 80 | $350 | Low | 1 |
| smart-contract-audit | 95 | $500 | Low | 1 |
| ai-model-fine-tuning | 85 | $300 | Medium | 2 |
| defi-protocol-integration | 88 | $350 | Medium | 2 |
| data-visualization | 75 | $150 | High | 3 |
| web-scraping-automation | 72 | $120 | Medium | 3 |
| crypto-portfolio-analysis | 70 | $200 | Medium | 3 |

## Pricing Guide

```
Effective hourly rate = (skill_price × 0.7) / estimated_hours

Floor: $40/hr effective rate
Target: $80-150/hr effective rate

Skill price tiers:
- $50-150: Quick tools, one-shot scripts (1-3hr delivery)
- $200-400: Full integrations, bots, pipelines (4-12hr delivery)
- $500-1000: Complex systems, audits, custom algos (1-3 day delivery)
```

## Running

### Main loop (do this via automation every 6 hours):
```bash
cd /home/workspace/MoneyMachine
python scripts/autolist_runner.py
```

### Manual triggers:
```bash
# Build next skill immediately
python scripts/skill_builder.py --immediate

# Check earnings and kill bad skills
python scripts/earnings_tracker.py --audit

# Publish all skills to zo.pub
zopub sync skills ./services
```

## Success Metrics

- Skills created per week: 2-3
- Time to first sale: < 7 days
- Minimum earnings per active skill: $50/week
- Kill anything below floor after 2-week observation window

## Notes

- Skills live in `/home/workspace/Skills/` — accessible to all Zo agents
- Listings also go to: `/home/workspace/MoneyMachine/services/` for zo.pub sync
- The - If OpenCollab comes back online, add it back to deploy_to_markets.py immediately