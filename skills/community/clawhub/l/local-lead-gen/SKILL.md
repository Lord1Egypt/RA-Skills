---
name: local-lead-gen
description: Automated local business lead generation and cold outreach pipeline. Scans businesses by niche and city, scores their websites (SSL, mobile, speed, design), identifies bad/outdated sites, enriches with contact info, and sends personalized cold emails pitching services. Use when building lead gen pipelines, prospecting local businesses, finding companies with bad websites, automating cold outreach, or setting up recurring business development workflows.
---

# Local Lead Gen — Automated Business Prospecting & Outreach

Find local businesses with bad websites, score them, and auto-email personalized pitches.

## Pipeline Overview

1. **Scan** — Search businesses by niche + city via Brave Search API
2. **Score** — Check each site: SSL, mobile-friendly, speed, design age, broken elements (0-100)
3. **Filter** — Flag sites scoring <40 as outreach candidates
4. **Enrich** — Extract emails from contact pages using DeepCrawl or direct scraping
5. **Email** — Send personalized cold emails via Resend (or any SMTP provider)
6. **Track** — Log all leads to Google Sheets or CSV with status tracking

## Requirements

- **Brave Search API key** — for business discovery (free tier available)
- **Resend API key** (or SMTP credentials) — for sending cold emails
- **DeepCrawl API key** (optional) — for better contact page parsing
- **Google Sheets OAuth** (optional) — for lead tracking

## Quick Start

```bash
# Set environment variables
export BRAVE_API_KEY=your_key
export RESEND_API_KEY=your_key

# Run the scanner
node scripts/bad-website-hunter.js --niche "restaurants" --city "Austin TX" --limit 20
```

## Configuration

Edit `scripts/config.json` to customize:
- Target niches and cities
- Score thresholds for outreach
- Email templates and sender info
- Suppression list (unsubscribed emails)

## Scripts

- `scripts/bad-website-hunter.js` — Main pipeline: scan → score → enrich → email
- `scripts/config.json` — Pipeline configuration

## Email Templates

The default cold email template pitches web design/development services. Customize in config.json:

```
Subject: Quick question about {business_name}'s website

Hi {first_name},

I was looking at {business_name}'s website and noticed a few things 
that might be costing you customers: {issues_found}.

I help local businesses in {city} modernize their online presence. 
Would you be open to a quick chat about what an upgrade could look like?

Best,
{sender_name}
```

## Scaling

- **Small towns** (pop 5-30K) yield the highest percentage of bad sites
- **Best niches**: restaurants, auto repair, salons, contractors, law offices
- **Send 10-25 emails per day** per domain to avoid spam flags
- **Rotate sending domains** if scaling past 50/day
- **Add drip sequences** (follow-up emails at day 3 and day 7)

## References

- See `references/scoring-criteria.md` for website scoring methodology
- See `references/email-best-practices.md` for cold email deliverability tips
