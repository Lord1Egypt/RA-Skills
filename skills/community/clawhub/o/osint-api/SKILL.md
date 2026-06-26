---
name: osint-api
description: >
  AI-powered OSINT intelligence reports via API.
  Multiple RSS feeds across 15 categories with enriched analysis,
  domain recon, and automated feed health monitoring.
homepage: https://github.com/ahsan-tariq-ai/osint-api
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env: ["OSINT_API_KEY"]
    primaryEnv: "OSINT_API_KEY"
    files: ["scripts/osint_api.py"]
    externalEndpoints:
      - https://osint.ahsan-tariq-ai.xyz/api/v1
    trust: >
      This skill calls a single hosted API at osint.ahsan-tariq-ai.xyz.
      The helper script (scripts/osint_api.py) makes HTTPS requests to
      that domain only — no other network access, no local files read/written,
      no shell commands executed. The OSINT_API_KEY environment variable is
      required for authenticated endpoints.
---

# OSINT API — Intelligence Reports

AI-powered OSINT intelligence reports via API. Multiple RSS feeds across 15 categories with enriched analysis, domain recon, and automated feed health monitoring.

## External Endpoints

All requests go to a single hosted API:

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `https://osint.ahsan-tariq-ai.xyz/api/v1/reports/enriched` | GET | Intelligence briefings | Yes |
| `https://osint.ahsan-tariq-ai.xyz/api/v1/reports/categories` | GET | List categories | Yes |
| `https://osint.ahsan-tariq-ai.xyz/api/v1/recon/{domain}` | GET | Domain recon (DNS/WHOIS/IP) | Yes |
| `https://osint.ahsan-tariq-ai.xyz/api/v1/social/{username}` | GET | Social media profiles | Yes |
| `https://osint.ahsan-tariq-ai.xyz/api/v1/breach/{email}` | GET | Breach database check | Yes |

## Security & Privacy

- **API key required** — all endpoints require `OSINT_API_KEY` environment variable
- **Single external host** — all requests go to `osint.ahsan-tariq-ai.xyz` only
- **No local file access** — the helper script reads no local files
- **No data persistence** — responses are returned and not saved locally
- **HTTPS only** — all traffic encrypted via TLS
- **Helper script** — `scripts/osint_api.py` is a thin Python wrapper that calls the API. It uses `urllib.request` (stdlib only), makes no shell calls, and performs no local I/O.

## Required Environment

```bash
export OSINT_API_KEY="your_api_key_here"
```

Sign up for an API key at https://osint.ahsan-tariq-ai.xyz

## Tools

### get_reports
Get enriched intelligence briefings across 15 categories.

**Endpoint:** `GET /reports/enriched`

**Parameters:**
| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| category | string | No | all | Filter by category name |

**Usage:**
```bash
python3 scripts/osint_api.py reports
python3 scripts/osint_api.py reports --category geopolitics
```

Or via curl (with API key):
```bash
curl -H "Authorization: Bearer $OSINT_API_KEY" \
  "https://osint.ahsan-tariq-ai.xyz/api/v1/reports/enriched"
```

**Response:**
```json
{
  "status": "success",
  "date": "2026-04-06",
  "reports": [
    {
      "category": "geopolitics",
      "enriched": true,
      "confidence": 0.82,
      "article_count": 47,
      "briefing": "Escalating tensions in Eastern Europe..."
    }
  ],
  "total_categories": 15
}
```

### get_categories
List all available report categories with metadata.

**Endpoint:** `GET /reports/categories`

**Usage:**
```bash
python3 scripts/osint_api.py categories
```

### domain_recon
Get DNS, WHOIS, and IP intelligence for any domain.

**Endpoint:** `GET /recon/{domain}`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| domain | string | Yes | Domain to investigate |

**Usage:**
```bash
python3 scripts/osint_api.py recon --domain google.com
```

### social_lookup
Find social media profiles for a username.

**Endpoint:** `GET /social/{username}`

**Usage:**
```bash
python3 scripts/osint_api.py social --username username
```

### breach_check
Check if an email appears in known breach databases.

**Endpoint:** `GET /breach/{email}`

**Usage:**
```bash
python3 scripts/osint_api.py breach --email user@example.com
```

## Categories

The engine collects from multiple RSS feeds across 15 categories:

| Category | Focus |
|----------|-------|
| cybersecurity | Threats, CVEs, vendor advisories |
| tech_ai | AI/ML news, product launches, research |
| geopolitics | World news, conflict, diplomacy |
| finance | Markets, crypto, economics |
| healthcare | Pharma, biotech, medical research |
| legal_regtech | Law, compliance, regulatory focus |
| marketing_adtech | Marketing industry, ad tech |
| supply_chain | Logistics, freight, supply chain |
| climate_sustainability | Climate change, ESG, green tech |
| real_estate_proptech | Property, PropTech |
| education_edtech | Education technology |
| energy_utilities | Power, energy, utilities |
| agriculture_foodtech | Agriculture, food tech |
| entertainment_media | Gaming, streaming, media |
| labor_workforce | Labor market, workplace intelligence |

## Helper Script

`scripts/osint_api.py` is a thin Python wrapper (stdlib only, no dependencies) that calls the OSINT API. It:
- Makes HTTPS requests to `osint.ahsan-tariq-ai.xyz` only
- Requires `OSINT_API_KEY` environment variable
- Reads no local files, writes no local files
- Executes no shell commands
- Sanitizes all input via `urllib.parse.quote`

## Pricing

| Tier | Price | Requests/Day | Features |
|------|-------|-------------|----------|
| Free | $0/mo | 50 | Market Intelligence (15 categories), Domain Recon |
| Pro | 10 USDC/mo | 1,000 | Everything in Free + Social Lookup (10+ platforms), Breach Check |
| Enterprise | 50 USDC/mo | 10,000 | Everything in Pro + Dedicated Gateway, Enriched Briefings (LLM) |

## Notes

- Reports are refreshed daily via cron — API responses are cached
- Confidence scores: 0.0-1.0 based on article count, source diversity, signal strength
