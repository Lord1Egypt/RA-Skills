---
name: ntriq-world-bank-economic-indicators
description: "Free API for World Bank economic indicators and macro data. No subscription. Access GDP, inflation, poverty rates, trade data, development metrics. Government data, pay-per-use."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [economics,development]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# World Bank Economic Indicators

Free World Bank macro-economic data API. Access GDP, inflation, poverty rates, trade data, and 1,500+ development indicators for 217 economies. No subscription required — replaces paid economic data subscriptions.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country_code` | string | ✅ | ISO 3166-1 alpha-2 (or `all` for all countries) |
| `indicators` | array | ✅ | World Bank indicator codes (e.g., `NY.GDP.MKTP.CD`) |
| `date_range` | string | ❌ | Year range e.g. `2015:2024` |
| `per_page` | integer | ❌ | Results per page (default: 50, max: 1000) |

## Example Response

```json
{
  "country": "Brazil",
  "iso2": "BR",
  "indicators": {
    "NY.GDP.MKTP.CD": {"label": "GDP (current US$)", "value": 2080000000000, "year": 2023},
    "FP.CPI.TOTL.ZG": {"label": "Inflation, consumer prices (annual %)", "value": 4.62, "year": 2023},
    "SL.UEM.TOTL.ZS": {"label": "Unemployment (% of labor force)", "value": 7.8, "year": 2023},
    "NE.TRD.GNFS.ZS": {"label": "Trade (% of GDP)", "value": 38.1, "year": 2023}
  }
}
```

## Use Cases

- Emerging market investment research and screening
- Country economic risk model data ingestion
- Academic economic research data collection

## Access

```bash
# x402 endpoint — pay $0.01 USDC per call (Base mainnet)
POST https://x402.ntriq.co.kr/world-bank-econ

# Service catalog
curl https://x402.ntriq.co.kr/services
```

[x402 micropayments](https://x402.ntriq.co.kr) — USDC on Base, gasless EIP-3009
