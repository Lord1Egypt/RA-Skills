---
name: gov-permit-scraper
description: Scrape government permit databases (liquor licenses, business registrations, contractor permits, health permits) to generate B2B sales leads. Enriches raw permit data with business emails via web scraping, then auto-emails outreach. Use when building lead lists from public records, scraping state licensing databases, generating B2B leads from government data, prospecting newly licensed businesses, or building insurance/services outreach pipelines targeting permit holders.
---

# Gov Permit Scraper — Public Records to Sales Pipeline

Turn government permit databases into enriched B2B lead lists with automated outreach.

## Pipeline Overview

1. **Scrape** — Pull new permits from state/county databases
2. **Filter** — Remove irrelevant permits (distributors, manufacturers, renewals)
3. **Enrich** — Find business emails via Brave Search + contact page scraping
4. **Store** — Append to Google Sheets or CSV with deduplication
5. **Email** — Send personalized outreach via Resend/SMTP
6. **Drip** — Follow up at day 3 and day 7

## Supported Data Sources

### Texas (TABC — Liquor Licenses)
- Source: `https://www.tabc.texas.gov/public-information/new-permits-issued/`
- Data: Business name, permit type, address, county, issue date
- Best for: Insurance agents, POS vendors, food service suppliers

### Adaptable to Any State
The scraper pattern works for any government permit database:
- Contractor licenses
- Restaurant health permits
- Real estate licenses
- Professional licenses (medical, legal, etc.)
- Business registrations (Secretary of State)

## Requirements

- **Brave Search API key** — for email enrichment
- **Resend API key** (or SMTP) — for outreach emails
- **Google Sheets OAuth** (optional) — for lead tracking

## Quick Start

```bash
# Set environment variables
export BRAVE_API_KEY=your_key
export RESEND_API_KEY=your_key

# Run the TABC pipeline
node scripts/permit-pipeline.js --source tabc --since 2026-03-01

# Dry run (no emails sent)
node scripts/permit-pipeline.js --source tabc --since 2026-03-01 --dry-run
```

## Configuration

Edit `scripts/config.json`:
- `source`: Which permit database to scrape
- `filterKeywords`: Permit types to exclude
- `enrichmentMethod`: brave | deepcrawl | direct
- `emailTemplate`: Customizable pitch template
- `sheetId`: Google Sheets ID for lead tracking
- `fromEmail`: Sender email address

## Scripts

- `scripts/permit-pipeline.js` — Main scrape → enrich → email pipeline
- `scripts/config.json` — Pipeline configuration

## Email Strategy

### Initial Outreach (Day 0)
Congratulate on new license, offer relevant service. Keep under 100 words.

### Follow-up (Day 3)
Quick bump with one additional value point.

### Break-up (Day 7)
Last touch, include social proof or case study link.

## References

- See `references/data-sources.md` for government database URLs by state
- See `references/compliance.md` for CAN-SPAM and cold email legal guidelines
