# SEC EDGAR

Query the SEC's EDGAR database for public company filings and financial data. Search companies, pull recent 10-K/10-Q/8-K filings, and access structured XBRL financial facts.

## Capabilities

**search_companies** -- Find companies by name or ticker. Returns CIK numbers needed for other tools.

**get_company_filings** -- Recent filings for a company by CIK. Optionally filter by form type (10-K, 10-Q, 8-K, DEF 14A, etc.). Each filing includes the accession number, date, and a direct link to the primary document.

**get_company_facts** -- XBRL financial data for a company. Returns curated key metrics: revenue, net income, total assets, liabilities, stockholders equity, cash, EPS, shares outstanding, operating income, gross profit, and R&D expense -- each with the most recent annual value.

## Example: look up Apple's recent 10-K filings

```bash
curl -X POST https://gateway.pipeworx.io/sec/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_company_filings","arguments":{"cik":"320193","form_type":"10-K"}}}'
```

## Common CIK numbers

- Apple: 320193
- Tesla: 1318605
- Microsoft: 789019
- Amazon: 1018724

```json
{
  "mcpServers": {
    "sec": {
      "url": "https://gateway.pipeworx.io/sec/mcp"
    }
  }
}
```
