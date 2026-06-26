# Pipeworx Fintech Analyst

FinTech Intel MCP — Compound tools that chain SEC, CFPB, FDIC,

## Setup

```json
{
  "mcpServers": {
    "fintech-intel": {
      "url": "https://gateway.pipeworx.io/mcp?task=fintech%20analysis"
    }
  }
}
```

## Compound tools (start here)

These combine multiple data sources into one call:

| Tool | Description |
|------|-------------|
| `fintech_company_deep_dive` | Complete company financial analysis in one call — SEC filings (10-K), stock quote, company overview, |
| `fintech_bank_health_check` | Bank health assessment — FDIC institution lookup, financials, recent industry failures, consumer com |
| `fintech_market_snapshot` | Financial market conditions dashboard — CFPB complaint trends, FDIC banking industry summary, and op |

## Individual tools

For granular queries, these are also available:

| Tool | Description |
|------|-------------|
| `edgar_search_filings` | Full-text search across all SEC EDGAR filings. Search by keyword, company name, or topic. Optionally |
| `edgar_company_filings` | Get recent SEC filings for a specific company. Accepts a ticker symbol or CIK number. Optionally fil |
| `edgar_company_facts` | Get structured XBRL financial data for a company by CIK. Returns key financial metrics like revenue, |
| `edgar_company_concept` | Get a specific financial metric over time for a company. Returns all reported values across filings  |
| `edgar_ticker_to_cik` | Look up a company CIK number from its ticker symbol. The CIK is needed for other EDGAR tools. |
| `cfpb_search_complaints` | Search the CFPB consumer complaint database. Filter by keyword, company, product category, and date  |
| `cfpb_company_complaints` | Get recent consumer complaints for a specific company, sorted by newest first. Returns complaint det |
| `cfpb_get_complaint` | Get full details for a single consumer complaint by its complaint ID number. |
| `cfpb_top_companies` | Get the companies with the most consumer complaints in a given date range. Useful for identifying wh |
| `cfpb_product_breakdown` | Get complaint counts broken down by product category. Optionally filter by company and/or date range |
| `fdic_search_institutions` | Search for FDIC-insured banks and institutions by name. Returns institution name, CERT number, city, |
| `fdic_get_institution` | Get detailed information for a specific FDIC-insured bank by its CERT (certificate) number. Returns  |
| `fdic_financials` | Get financial call report data for a bank by CERT number. Returns quarterly financial metrics includ |
| `fdic_failures` | List FDIC bank failures, sorted by most recent. Optionally filter by date range. Returns bank name,  |
| `fdic_summary` | Get aggregate industry summary data for all FDIC-insured institutions for a given reporting date. Re |

## Data sources

- **Edgar**: EDGAR MCP — SEC EDGAR public APIs (free, no auth)
- **Cfpb**: CFPB MCP — Consumer Financial Protection Bureau complaint database (free, no auth)
- **Fdic**: FDIC MCP — FDIC BankFind Suite API (free, no auth)
- **Alphavantage**: Alpha Vantage MCP — Stock market data, fundamentals, and earnings
- **Fred**: FRED MCP — Federal Reserve Economic Data (St. Louis Fed)

## Tips

- Start with compound tools — they handle errors and combine data automatically
- Use `ask_pipeworx` if you're unsure which tool to use
- Use `remember`/`recall` to save intermediate findings
