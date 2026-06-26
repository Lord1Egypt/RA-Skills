# Pipeworx Data Analyst

Connect to 252 data sources and 1008+ tools through one gateway. Ask questions in plain English — Pipeworx picks the right tool, fills the arguments, and returns real data.

## Setup

```json
{
  "mcpServers": {
    "pipeworx": {
      "url": "https://gateway.pipeworx.io/mcp"
    }
  }
}
```

## How to use

### Ask anything

Call `ask_pipeworx` with a question. The gateway finds the right API and returns the answer.

- "What is the US trade deficit with China?"
- "What are the side effects of ozempic?"
- "What's the weather in Tokyo?"
- "Get Apple's latest 10-K filing"
- "Find cybersecurity government contracts"

### Find specific tools

Call `discover_tools` with a description to browse what's available.

### Scope to a domain

Add `?task=` to the URL for focused sessions with only relevant tools:

- `gateway.pipeworx.io/mcp?task=housing+market`
- `gateway.pipeworx.io/mcp?task=international+trade`
- `gateway.pipeworx.io/mcp?task=drug+safety+research`

### Remember context

Use `remember` and `recall` to save findings across tool calls.

## Compound tools

These combine multiple APIs into one call:

| Tool | Description |
|------|-------------|
| `trade_bilateral_analysis` | Complete bilateral trade analysis between two countries in one call. Combines Comtrade trade flows ( |
| `trade_country_profile` | Comprehensive trade profile for a country — top 10 import/export partners and top 10 import/export c |
| `trade_macro_dashboard` | US trade macro indicators dashboard — customs revenue, exchange rates, trade balance, monthly trends |
| `fintech_company_deep_dive` | Complete company financial analysis in one call — SEC filings (10-K), stock quote, company overview, |
| `fintech_bank_health_check` | Bank health assessment — FDIC institution lookup, financials, recent industry failures, consumer com |
| `fintech_market_snapshot` | Financial market conditions dashboard — CFPB complaint trends, FDIC banking industry summary, and op |
| `pharma_drug_profile` | Complete drug dossier in one call — FDA approvals, drug labels, adverse events, RxNorm properties, d |
| `pharma_pipeline_scan` | Clinical trial pipeline analysis — by condition (e.g., "lung cancer", "Alzheimer") or by sponsor (e. |
| `pharma_safety_report` | Drug safety assessment — adverse event reports, top reaction types, recall history, and drug-drug in |
| `govcon_contractor_profile` | Complete government contractor dossier — SAM.gov entity registration, federal award history (USAspen |
| `govcon_opportunity_scan` | Government contracting opportunity search — open SAM.gov opportunities, set-aside contracts (8(a), H |
| `govcon_agency_landscape` | Federal agency contracting landscape — spending overview, recent awards, SBIR program stats, and spe |
| `housing_market_snapshot` | Get a national housing market snapshot — 30-year mortgage rates, housing starts, Case-Shiller home p |
| `housing_property_report` | Complete property analysis combining ATTOM data — property details, automated valuation (AVM), sales |
| `housing_rental_analysis` | Rental market analysis for a property and area — estimated rent (ATTOM), fair market rents (HUD, if  |
| `housing_affordability_check` | Check housing affordability metrics — current mortgage rate (national), median home price (national) |
| `housing_employment_outlook` | Labor market indicators relevant to housing — total nonfarm employment, construction employment, res |
| `housing_signal_scan` | Comprehensive housing market signal scan — checks 45+ indicators for reversals, unusual moves, accel |

## Response metadata

Every response includes `_meta` with cost breakdown, cache status, next-step suggestions, and error alternatives.
