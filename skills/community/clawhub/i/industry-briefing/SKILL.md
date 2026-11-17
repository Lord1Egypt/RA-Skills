---
name: industry-briefing
description: Generate structured industry briefings by searching the web for the latest news and developments. Use when: user asks for a briefing on a specific industry, wants to catch up on breaking news, or needs a summary of recent trends. NOT for: historical analysis, deep technical analysis, or predictions.
homepage: https://github.com/openclaw/industry-briefing
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": {},
        "install": [],
      },
  }
---

# Industry Briefing

Generate structured, up-to-date briefings about any industry, topic, or company by searching the web and synthesizing results.

## When to Use

✅ **USE this skill when:**

- "Give me a briefing on [industry/topic]"
- "What's new in [industry] this week?"
- "Latest news about [company/topic]"
- "Industry update for [sector]"
- "Breaking news summary"

## When NOT to Use

❌ **DON'T use this skill when:**

- Historical analysis → use archives or research reports
- Deep technical analysis → use specialized technical sources
- Predictions/forecasts → use market analysts
- Legal/financial advice → consult professionals

## Quick Command

```bash
# Briefing generation is handled via the tool system.
# The skill provides guidance and templates for creating structured briefings.
```

## Briefing Template

Industry briefings should follow this structure:

### 1. Executive Summary
One-paragraph overview of key developments and overall mood.

### 2. Top Headlines (3-5 stories)
- Most significant recent developments
- Each with source and date
- 1-2 sentence summary

### 3. Trends & Patterns
- Emerging themes across multiple stories
- Shifts in market sentiment
- Regulatory or technology changes

### 4. Companies in Focus
- Key players mentioned
- Recent moves or announcements

### 5. Outlook & Implications
- What this means for stakeholders
- Potential follow-up stories to watch

## Response Structure

Your briefing should output:

```
# Industry Briefing: [Topic]
Date: [Generated Date]

## Executive Summary
[Overview paragraph - 2-3 sentences about the big picture]

## Top Headlines
1. **[Headline 1]** ([Source], [Date])
   - [1 sentence summary]
   
2. **[Headline 2]** ([Source], [Date])
   - [1 sentence summary]

3. **[Headline 3]** ([Source], [Date])
   - [1 sentence summary]

## Key Trends
- **[Trend 1]**: [Why it matters, evidence from 2+ sources]
- **[Trend 2]**: [Why it matters, evidence from 2+ sources]
- **[Trend 3]**: [Why it matters, evidence from 2+ sources]

## Companies to Watch
- **[Company]**: [What they did/announced]
- **[Company]**: [What they did/announced]

## Outlook
- [Implication 1 - how this affects the industry]
- [Implication 2 - potential future developments]
- [Implication 3 - who benefits/loses]

Sources: [List of URLs/sources used]
```

## Tiered Result Types

### Quick Brief (schedule=short)
- 2-3 headlines max
- 1 trend
- 1 company
- ~500 words

### Standard Brief (schedule=full/default)
- 3-5 headlines
- 2-3 trends
- 2-3 companies
- ~750-1000 words

### Deep Briefing (schedule=deep)
- 5-7 headlines
- 3-4 trends
- 3-5 companies
- Full outlook
- ~1500 words

## Parameters & Optimization

### Time Ranges

- `freshness=day`: Last 24 hours
- `freshness=week`: Last 7 days (default)
- `freshness=month`: Last 30 days
- `freshness=year`: Last 12 months

### Language

- `language=en`: English (default)
- `language=zh`: Chinese
- `language=es`: Spanish

## Quality Guidelines

1. **Factuality**: Cross-reference information when possible, especially for breaking news
2. **Balance**: Include positive and negative developments
3. **Sources**: Prioritize reputable sources; cite all sources
4. **Objectivity**: Present facts without injecting personal opinion
5. **Clarity**: Use concise language, avoid jargon

## Example Briefings

### Tech Industry Brief (Abbreviated)

```
# Industry Briefing: Technology & AI
Date: 2026-07-05

## Executive Summary
The tech sector continues to rapidly advance with major breakthroughs in renewable AI models and autonomous vehicles. Regulatory authorities around the world have intensified efforts to balance innovation with consumer protection.

## Top Headlines
1. **Tesla Unveils Dojo Supercomputer at AI Day** (TechCrunch, Today)
   - Tesla showcases new Dojo supercomputer designed specifically for training autonomous vehicle models.

2. **New EU AI Act Implementation Guidelines Released** (Bloomberg, 2 days ago)
   - EU provides detailed guidance on classifying AI systems for compliance by May 2026.

3. **Global Semiconductor Shortage Eases in Q2** (Reuters, 3 days ago)
   - Chipmakers report improved production rates, signaling potential relief for supply chains.

## Key Trends
- **Manufacturing Optimization**: Multiple announcements reveal focus on autonomous manufacturing, with Tesla and BMW partnering to integrate AI into factories.
- **AI Safety Standards**: Governments across North America, Europe, and Asia are publishing unified safety standards, rooted in NIST guidelines.

## Companies to Watch
- **Tesla**: Accelerating Dojo deployment with 1000-petaflop cluster targeting 50x faster training.
- **NVIDIA**: Releases Hopper successor architecture rumored to include generative AI accelerators.
- **ASML**: Secures Chinese market access, reports record EUV shipments to China.

## Qualified Outlook
Look for Tesla's next-gen Full Self-Driving demo this quarter. Expect consolidation in the AI chip space as companies seek to scale. EU AI Act implementation will be a major driver of standardization.

Sources: TechCrunch, Bloomberg, Reuters
```

### Healthcare Industry Brief

```
# Industry Briefing: Healthcare & Biotech
Date: 2026-07-05

## Executive Summary
Major developments in personalized medicine and gene editing highlight rapid advancements in healthcare. Partnerships between pharma companies and AI startups are accelerating drug discovery timelines.

## Top Headlines
1. **CRISPR Therapeutics Reports 90% Cure Rate for Sickle Cell** (Nature Genetics, 1 day ago)
   - Long-term data from exa-cel trials shows sustained benefit with manageable side effects.

2. **Apple Health App Revolutionizes Chronic Disease Monitoring** (CNBC, 2 days ago)
   - Apple introduces proactive monitoring with AI-driven insulin sensitivity and heart health predictive analytics.

3. **FDA Approves First AI-Generated Drug Molecule** (FiercePharma, Today)
   - Sanofi's diabetes candidate becomes the first fully AI-designed drug to receive regulatory clearance.

## Key Trends
- **AI-Driven Clinical Trials**: Companies are using AI to reduce trial recruitment times by 40-50%, particularly for rare diseases.
- **Remote Patient Monitoring Market Grows**: Remote monitoring devices and wearables market expands 35% YoY as hospitals embrace continuous data.

## Companies to Watch
- **CRISPR Therapeutics**: Targets $1B+ in exa-cel sales by 2028 with expanded indications.
- **DeepMind/Isomorphic Labs**: Partner with GSK and Illumina to rapidly advance epigenetic cancer therapies.
- **Medtronic**: Major expansion into ambulatory care devices, launches AI-powered pacemaker monitoring system.

## Qualified Outlook
Look for more AI-designed drugs entering trials in late 2026. Medicare/Medicaid coverage decisions for exa-cel and similar treatments will be a key driver of patient access and market adoption.

Sources: Nature Genetics, CNBC, FiercePharma
```

## Styles & Identity

- **Professional**: Corporate/small business audiences — concise, structured, business-oriented
- **Academic**: Research/education settings — detailed citations, technical context, balanced perspectives
- **Accessible**: General readers — avoiding jargon, clear explanations, plain language

## Fallback Strategies

- **Primary**: Use `web_search` then `web_fetch` for deep dives
- **Secondary**: If searches fail or timeout, summarize what retuns without speculation
- **Tertiary**: For technical or niche topics, target specific sites (TechCrunch, Bloomberg, Reuters)


Limitations: Only retrieves publicly available information. Financial markets, corporate strategies, investor insights, or non-public initiatives require specialized reporting. Cross-reference with regulatory filings when discussing legal changes or compliance matters.
