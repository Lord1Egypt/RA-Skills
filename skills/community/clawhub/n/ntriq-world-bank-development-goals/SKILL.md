---
name: ntriq-world-bank-development-goals
description: "Free API for UN Sustainable Development Goals (SDG) tracking. No subscription. Track progress by country for poverty, health, education, development metrics. Government data, pay-per-use."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [economics,development]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# World Bank Development Goals

Free API for UN Sustainable Development Goals (SDG) progress tracking. Monitor 17 SDGs and 232 indicators by country, region, or globally using World Bank data. No subscription required — direct World Bank database access.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country_code` | string | ❌ | ISO 3166-1 alpha-2 or `world` for global |
| `sdg_goals` | array | ❌ | SDG numbers 1–17 (default: all) |
| `indicators` | array | ❌ | Specific indicator codes (e.g., `SI.POV.NAHC`) |
| `year_range` | object | ❌ | `{"start": 2010, "end": 2023}` |

## Example Response

```json
{
  "country": "Kenya",
  "sdg_progress": {
    "SDG1_No_Poverty": {
      "headline_indicator": "Poverty headcount ratio at $2.15/day (2017 PPP)",
      "value": 26.8,
      "unit": "% of population",
      "year": 2021,
      "trend": "improving",
      "change_10yr": -14.2
    },
    "SDG3_Good_Health": {
      "under5_mortality_per1000": 41.2,
      "maternal_mortality_per100k": 342,
      "trend": "improving"
    }
  }
}
```

## Use Cases

- Impact investment SDG alignment reporting
- Development organization program monitoring
- ESG fund emerging market sustainability scoring

## Access

```bash
# x402 endpoint — pay $0.01 USDC per call (Base mainnet)
POST https://x402.ntriq.co.kr/world-bank-goals

# Service catalog
curl https://x402.ntriq.co.kr/services
```

[x402 micropayments](https://x402.ntriq.co.kr) — USDC on Base, gasless EIP-3009
