# Pipeworx Housing Analyst

Housing Intel MCP — Meta-pack that chains FRED, BLS, ATTOM, and HUD APIs

## Setup

```json
{
  "mcpServers": {
    "housing-intel": {
      "url": "https://gateway.pipeworx.io/mcp?task=housing%20analysis"
    }
  }
}
```

## Compound tools (start here)

These combine multiple data sources into one call:

| Tool | Description |
|------|-------------|
| `housing_market_snapshot` | Get a national housing market snapshot — 30-year mortgage rates, housing starts, Case-Shiller home p |
| `housing_property_report` | Complete property analysis combining ATTOM data — property details, automated valuation (AVM), sales |
| `housing_rental_analysis` | Rental market analysis for a property and area — estimated rent (ATTOM), fair market rents (HUD, if  |
| `housing_affordability_check` | Check housing affordability metrics — current mortgage rate (national), median home price (national) |
| `housing_employment_outlook` | Labor market indicators relevant to housing — total nonfarm employment, construction employment, res |
| `housing_signal_scan` | Comprehensive housing market signal scan — checks 45+ indicators for reversals, unusual moves, accel |

## Individual tools

For granular queries, these are also available:

| Tool | Description |
|------|-------------|
| `fred_get_series` | Get observations (data points) for a FRED series. Key housing series: MORTGAGE30US (30-year mortgage |
| `fred_search` | Search for FRED series by keyword. Useful for discovering series IDs for housing, employment, inflat |
| `fred_series_info` | Get metadata about a FRED series: title, units, frequency, seasonal adjustment, notes, and date rang |
| `fred_category` | Browse FRED categories. Use category_id=0 for the root. Useful for exploring available data by topic |
| `fred_releases` | Get the latest FRED data releases. Shows upcoming and recent releases of economic data. |
| `bls_get_series` | Get time series data from the Bureau of Labor Statistics for one or more series. Supports employment |
| `bls_search` | Search for BLS series IDs by keyword from a curated catalog of popular housing, employment, wages, p |
| `bls_latest` | Get just the most recent data point for a BLS series. Useful for quick current-value lookups. |
| `bls_popular_series` | List all curated popular BLS series with IDs and descriptions, organized by category (housing, emplo |
| `attom_property_detail` | Get full property characteristics by address — lot size, square footage, bedrooms, bathrooms, year b |
| `attom_property_search` | Search properties by location with optional filters. Search by postal code or by latitude/longitude  |
| `attom_sales_history` | Get complete sales history for a property (up to 10 years) — sale dates, prices, deed types, seller/ |
| `attom_avm` | Get automated valuation (AVM) for a property — estimated market value, confidence score, value range |
| `attom_assessment` | Get property tax assessment details — assessed value, market value, tax amount, tax year, and assess |
| `attom_sales_trend` | Get market sales trends by ZIP code — average/median sale price, volume, and price changes over time |

## Data sources

- **Fred**: FRED MCP — Federal Reserve Economic Data (St. Louis Fed)
- **Bls**: BLS MCP — Bureau of Labor Statistics public data API (v2)
- **Attom**: ATTOM MCP — Premium real estate data from ATTOM Data Solutions
- **Hud**: HUD MCP — U.S. Department of Housing and Urban Development APIs.

## Tips

- Start with compound tools — they handle errors and combine data automatically
- Use `ask_pipeworx` if you're unsure which tool to use
- Use `remember`/`recall` to save intermediate findings
