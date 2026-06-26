---
name: lbs-market-analyzer
description: "Comprehensive geo-spatial market intelligence and site selection evaluation using AMAP (Gaode) LBS API. Use when the user needs: (1) Competitor distribution and market pressure analysis, (2) Site selection evaluation based on 'heat logic' (synergy with office buildings, residential areas, and transit nodes), (3) 'Golden Path' flow analysis, (4) Identification of market gaps or 'blue ocean' areas. Includes automated AMAP API Key provisioning."
---

# LBS Market Analyzer

This skill provides specialized workflows for analyzing business competitors using geographical data from the AMAP (Gaode) LBS API.

## Core Workflow

1. **Setup (Proactive)**: If `AMAP_KEY` is missing from environment/`.env`, run `scripts/amap_key_automator.py` immediately.
2. **Geocoding**: Convert a user's address or point of interest into coordinates.
3. **Competitor Scanning**: Retrieve POIs based on industry keywords and radius.
4. **Structured Reporting**: Generate a density and gap analysis report.

## Usage Guidelines

### 1. Automated Provisioning
If you don't have an AMAP API Key:
`python3 scripts/amap_key_automator.py`
*Note: A browser will open for manual Alipay/AMAP login. The script will then automatically create a Web Service Key and append it to `.env`.*

### 2. Market Analysis Execution
Run the analysis script to fetch data:
`python3 scripts/competitor_analysis.py --address "YOUR_ADDRESS" --keywords "INDUSTRY_KEYWORDS" --radius 3000`

### 3. Insight Generation
After fetching data, use the logic in [references/analysis-logic.md](references/analysis-logic.md) to interpret the results (e.g., identifying "blue oceans" or high-pressure zones).

## Scripts

- **`scripts/amap_key_automator.py`**: Browser automation for AMAP console. Handles login (manual scan) and automatic Key creation.
- **`scripts/competitor_analysis.py`**: Interacts with AMAP API to fetch POI data. Requires `AMAP_KEY`.

## References

- **[references/analysis-logic.md](references/analysis-logic.md)**: Strategies for interpreting data and generating business insights.
- **[references/amap-api-guide.md](references/amap-api-guide.md)**: API status codes, category lists, and parameter limits.
