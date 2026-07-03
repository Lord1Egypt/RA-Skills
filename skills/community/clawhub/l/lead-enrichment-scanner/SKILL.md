---
name: lead-enrichment-scanner
version: 1.0.1
author: "NASSER AL-SOLAITTI"
description: "B2B lead enrichment using public web scraping and optional LLM metadata extraction. Input: company names or domains. Output: basic company info, email patterns, and scraped homepage content. Use when user says 'enrich a company', 'look up a company', or 'find info on a company'.
permissions:
  - network: scrape public homepage content via HTTPS only
  - filesystem-write: write output CSV to user-specified location
  - env: read MINIMAX_API_KEY from environment (for optional LLM metadata extraction)
privacy: |
  This skill scrapes ONLY public homepage content of companies you specify. No LinkedIn, no private databases.
  When MINIMAX_API_KEY is set, company descriptions are sent to api.minimax.chat for metadata extraction.
  No personal data is collected. No outreach drafts are generated in v1.0.
  Decision-maker names, LinkedIn profiles, CRM import, and outreach draft generation are planned for v1.1.
compliance: |
  You are responsible for lawful use of scraped contact data. Do not use scraped emails for unsolicited outreach
  without complying with CAN-SPAM, GDPR, and applicable local laws. This tool provides guesses and patterns,
  not verified contacts — verify before use.
---

# Lead Enrichment Scanner

## When to use this skill

Activate when the user wants to:
- Look up basic info on a company from its public website
- Generate email address patterns for a company
- Get a company's description and social links from their homepage
- Run enrichment in dry-run mode to preview output

> **v1.0 limitations:** This is a basic scraper + optional LLM enrichment.
> Decision-maker names, LinkedIn profiles, verified contacts, CRM import, and outreach drafts are NOT implemented (v1.1).

## Prerequisites

- MINIMAX_API_KEY (optional — only needed for LLM-based description extraction)
- OpenClaw gateway running

## Workflow

### 1. Prepare input

Create a text file with company names (one per line):

```bash
cat > companies.txt <<EOF
Stripe
Notion
Linear
EOF
```

### 2. Run enrichment

```bash
clawhub run lead-enrichment-scanner enrich \
  --input companies.txt \
  --output leads.csv
```

**What v1.0 actually extracts:**
- Best-guess domain from company name
- Homepage description (scraped via HTTPS)
- Email address patterns (guessed, not verified)
- Social links found on homepage
- Industry/company size via LLM (optional, MINIMAX_API_KEY required)

### 3. Dry-run mode

```bash
clawhub run lead-enrichment-scanner enrich \
  --input companies.txt \
  --output leads.csv \
  --dry-run
```

### 4. Configure respect for robots.txt

```bash
clawhub run lead-enrichment-scanner configure \
  --respect-robots-txt true \
  --rate-limit-seconds 5
```

## What v1.0 actually does

- ✅ Domain guessing from company name
- ✅ Public homepage scrape (HTTPS only, respects robots.txt)
- ✅ Email pattern generation (guessed, not verified)
- ✅ LLM metadata extraction (optional, MINIMAX_API_KEY required)
- ✅ SSRF protection (blocks private IPs, HTTPS-only)
- ❌ Decision-maker names — NOT implemented (v1.1)
- ❌ LinkedIn profiles — NOT implemented (v1.1)
- ❌ Verified contact emails — NOT implemented (v1.1)
- ❌ CRM import — NOT implemented (v1.1)
- ❌ Outreach draft generation — NOT implemented (v1.1)
- ❌ Bulk parallel processing (--bulk) — NOT implemented (v1.1)

## Output fields

- `name` — company name as provided
- `domain` — guessed domain
- `description` — from homepage scrape or LLM (if key set)
- `email_patterns` — guessed email formats (e.g. `{firstname}@domain.com`)
- `social_links` — LinkedIn/Twitter/GitHub links found on homepage

> **Important:** Email patterns are guesses, not verified deliverable addresses.
> Do not send outreach without verifying addresses first.

## Compliance responsibility

- robots.txt is respected by default
- Rate-limited to 5s between requests
- Scrapes public homepage content only
- You are responsible for GDPR/CAN-SPAM compliance when using contact data
- Do not provide LinkedIn session cookies — they are not used in v1.0

## Cost expectations

- Web scraping: free (public data, HTTPS)
- LLM extraction: ~$0.005 per company (only when MINIMAX_API_KEY is set)
- OpenClaw: free, self-hosted

## Troubleshooting

**Empty description for a company?**
- The homepage may block scraping — try a different domain format

**Email patterns look wrong?**
- Email patterns are guesses, not verified addresses. Always verify before outreach.

**Want LinkedIn enrichment, CRM import, or outreach drafts?**
- Planned for v1.1. Not implemented in v1.0.
