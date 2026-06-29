---
name: gocreative-enrichment
description: Lead enrichment, company enrichment, work-email finder & email validation for AI agents — plus company firmographics, domain/DNS/WHOIS intelligence, and LinkedIn/GitHub profile data. Enrich any lead or company by domain, or find and verify emails. Pay-per-call in USDC via x402 — no API key, no signup.
tags: [enrichment, b2b, leads, company-data, email-finder, email-validation, firmographics, domain, dns, whois, linkedin, prospecting, sales]
author: gocreative
version: 1.0.0
license: MIT
---

# GoCreative Enrichment

> Turn a domain or name into full B2B context — company data, emails, domain intel — one install, pay-per-call, no API key.

## When to use this
- An agent is **building or qualifying a lead** and needs company/contact data.
- An agent must **find or verify a work email** before outreach.
- An agent is **researching a company or domain** (firmographics, DNS, WHOIS, tech).

## How it's paid (x402 — no key, no signup)
Each tool is a plain HTTPS GET. The first call returns **HTTP 402** with a price; your OpenClaw wallet auto-pays the small USDC fee (Base) and retries, returning JSON.

## Tools (live endpoints)
| Call | What you get | Price |
|---|---|---|
| `GET https://api.gocreativeai.com/v1/enrich/company/{domain}` | B2B company enrichment from a domain (firmographics) | ~$0.05 |
| `GET https://api.gocreativeai.com/v1/enrich/email/{name-and-domain}` | Find a person's likely **work email** from name + company domain | ~$0.02 |
| `GET https://api.gocreativeai.com/v1/bundle/email-360/{email}` | **Email 360**: deliverability validation + provider/domain enrichment | ~$0.15 |
| `GET https://api.gocreativeai.com/v1/enrich/domain/{domain}` | Domain intel: DNS + WHOIS + TLS, fused | ~$0.05 |
| `GET https://api.gocreativeai.com/v1/enrich/linkedin/{profile}` | LinkedIn profile enrichment | ~$0.05 |
| `GET https://api.gocreativeai.com/v1/bundle/company-360/{domain}` | **Company 360**: full domain intelligence bundle | ~$0.15 |

URL-encode arguments. Email finder example: `/v1/enrich/email/jane-doe-stripe.com`.

## Examples
- Enrich a lead: `GET /v1/enrich/company/airbnb.com` → firmographic profile.
- Find + verify an email: `GET /v1/enrich/email/jane-doe-acme.com` → then `GET /v1/bundle/email-360/jane@acme.com`.
- Research a domain: `GET /v1/enrich/domain/acme.com` → DNS + WHOIS + TLS.

## Why GoCreative
Real fused data (firmographics, DNS/WHOIS/TLS, deliverability), **per-call pricing with no signup or monthly seat** — cheaper than legacy enrichment APIs that bill $500/mo. Pairs with `gocreative-compliance` for screen-then-enrich workflows.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
