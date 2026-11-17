---
name: liquid-local-leads
description: Find US local businesses to sell to (dentists, plumbers, HVAC, salons, law firms...) by category and place, with a checked email graded A/B/C, a contact name when the email shows one, phone, a website proven by the business's own phone number, socials and buying signals (no website, booking tool, payment system, hiring). $0.03 per lead over x402, no account, no API key.
homepage: "https://api.liquidagent.ai/v1/leads"

metadata:
  openclaw:
    requires:
      bins: ["curl"]
---

# Liquid Leads

**GET `https://api.liquidagent.ai/v1/leads/search?category=<what>&city=<where>&limit=<n>`** returns local businesses
that match, each with name, address, phone, website, the best email with its grade, a contact name when the email
shows one, socials and buying signals.

- Price: **$0.03 USDC per lead returned**, flat, x402 exact (EIP-3009), USDC on Base or Arc. 1 to 1,000 leads per call
  (default 3 = $0.09, or sample=1 for 3 free leads). The 402 quotes the exact total; no leads, no charge.
- Coverage: 30 US states live, more being added. `GET /v1/leads` lists them.
- Place: `city`, `county`, `zip`, or `near=<lat>,<lng>` with `radiusKm`.
- Filters: `email` (required by default, `any`, or `none` for phone-only businesses), `minGrade` (A, B, C),
  `website` (`needs` = no working website), `booking`, `payments`, `hiring=1`, `format=csv`.

## Free first

```bash
curl -s "https://api.liquidagent.ai/v1/leads/count?category=dentist&city=Atlanta"        # how many match, by grade, exact price
curl -s "https://api.liquidagent.ai/v1/leads/categories?city=Atlanta"                    # business types in a place
curl -s "https://api.liquidagent.ai/v1/leads/search?category=dentist&city=Atlanta&sample=1"  # 3 free leads (3 a day)
```

## Reverse lookup and website tech

- `GET https://api.liquidagent.ai/v1/leads/lookup?phone=4043552001` (or `?domain=example.com`): the business behind a phone
  number or website, same fields as a lead. **$0.01**, no match no charge.
- `GET https://api.liquidagent.ai/v1/leads/tech?domain=example.com`: the site's platform, booking tool, payment system,
  hiring and socials. **$0.005**, no match no charge.

## When to use this skill

- The person sells to local businesses and needs a list to contact (agency, SaaS, services, B2B sales)
- They want businesses with no website, no booking tool, or that are hiring (ready-made sales signals)
- They want a CSV to load into a CRM or an outreach tool
- They have a phone number or website and need to know which business it is (CRM cleanup, inbound calls, verification)
- They sell to businesses on a certain platform or without a booking tool and want to check a site first

## How the checks work

A website is only returned when the site carries the business's own phone number; a site we cannot prove is theirs
is dropped, and nothing from it is used. Every email has a working mail domain and is graded: A = the business's own
domain and a named person, B = own domain but a shared inbox (info@) or a free-mail address the business publishes,
C = a live domain not tied to their website.

## Example

```bash
# paid ($0.03 a lead): any x402 client signs the 402 for you, for example AgentCash
npx agentcash fetch "https://api.liquidagent.ai/v1/leads/search?category=plumber&city=Houston&limit=10"
```

Full script: [`examples/leads.js`](../../examples/leads.js). MCP: connect `https://api.liquidagent.ai/mcp` and use
`leads_count` (free) then `leads_search`, `leads_lookup` or `leads_tech` (paid inside the call).
