---
name: paragon-mls
description: "Fetch real estate listings from Paragon MLS (paragonrels.com / fnimls.com) APIs and perform four-square rental property analysis. Use when: (1) looking up MLS property details by MLS number or listing ID, (2) analyzing rental properties for cash flow and cash-on-cash return, (3) comparing multiple investment properties, (4) extracting structured data from Paragon MLS listings. Supports any Paragon-backed MLS region (globalmls, imls, hudson, gamls, triangle, etc.)."
metadata:
  openclaw:
    requires:
      bins:
        - node
    mcp:
      paragon-mls:
        command: node
        args:
          - /home/umbrel/.openclaw/workspace/deal-analyst/paragon-mls-mcp/dist/index.js
---

# Paragon MLS

Fetch real estate listings from Paragon MLS APIs and analyze rental investment properties.

## Quick Start

1. Build and configure the MCP server once:

```bash
cd paragon-mls-mcp && npm install && npm run build
```

2. Add to `mcporter` config (or your MCP client config):

```bash
mcporter config add paragon-mls --command "node /home/umbrel/.openclaw/workspace/deal-analyst/paragon-mls-mcp/dist/index.js" --transport stdio
```

3. Use the tools:

```bash
# Fetch all listings from a shared MLS link
mcporter call paragon-mls.fetch_listings mlsId="6d70b762-36a4-4ac0-bedd-d0dae2920867" systemId="globalmls"

# Fetch a single property by MLS number
mcporter call paragon-mls.fetch_property mlsNumber="201918514" systemId="globalmls"

# Analyze a deal with the spreadsheet-compatible Four-Square model
mcporter call paragon-mls.analyze_deal mlsNumbers="201918514" systemId="globalmls" holdingPeriodYears:5 downPaymentPct:0.25

# Analyze multiple properties with custom assumptions
mcporter call paragon-mls.analyze_deal mlsNumbers="201918514,202012345" systemId="globalmls" downPaymentPct:0.25 interestRate:0.065 monthlyInsurance:250 repairBudget:10000 landValue:35000

# Compare velocity banking strategies for a deal
mcporter call paragon-mls.vb_calc debtBalance:350000 interestRate:0.05 loanTermYears:30 monthlyIncome:8000 monthlyExpenses:4878.875681 extraPayment:1000

# Get raw JSON data
mcporter call paragon-mls.raw_listings mlsNumbers="201918514" systemId="globalmls"
```

## Tools

### `fetch_listings`
Fetch all property listings from a Paragon MLS listing GUID. Returns parsed property data for all active listings.

- **mlsId** (required): Paragon MLS listing GUID from the URL
- **systemId** (default: `globalmls`): MLS region ID (subdomain of paragonrels.com)

### `fetch_property`
Fetch a single property by its MLS number. Returns structured property data.

- **mlsNumber** (required): MLS number for the property
- **systemId** (default: `globalmls`): MLS region ID
- **mlsId** (optional): Listing GUID for link generation

### `analyze_deal`
Perform a spreadsheet-compatible Four-Square analysis on one or more properties. Returns the major columns from the Google Sheet, including NOI, DSCR, principal paydown, appreciation, depreciation, ROI, ROE, and IRR.

Key inputs:
- **mlsNumbers** (required): Comma-separated MLS numbers
- **systemId** (default: `globalmls`): MLS region ID
- **holdingPeriodYears** (default: `5`)
- **offerPricePct** (default: `1`)
- **downPaymentPct** (default: `0.20`)
- **interestRate** (default: `0.07`)
- **loanTermYears** (default: `30`)
- **vacancyRate / repairsPct / capexPct / mgmtPct** for recurring expense assumptions
- **closingCosts / repairBudget / reservePrepaid / privateMoneyLender / landValue** for capital stack and tax assumptions
- **monthlyPropertyTaxes / monthlySchoolTaxes / monthlyInsurance / monthlyWater / monthlySewer / monthlyGarbage / monthlyElectric / monthlyGas / monthlyHoa / monthlyLawnSnow / monthlyLegalAccounting** for direct spreadsheet column overrides
- **unitRent1..unitRent7 / laundryIncome / storageIncome / miscIncome** for income overrides

### `vb_calc`
Compare amortized debt, extra payments, chunking/basic acceleration, and advanced velocity banking.

- **debtBalance** (required)
- **interestRate** (required)
- **loanTermYears** (default: `30`)
- **extraPayment** (default: `0`)
- **monthlyIncome** (required)
- **monthlyExpenses** (required)
- **helocRate** (default: `0.2399`)
- **advancedRate** (default: `0.08`)
- **helocLimit** (default: `20000`)
- **chunkMonths** (default: `6`)

### `raw_listings`
Fetch raw JSON data from the Paragon API for custom analysis. Returns unprocessed listing data.

- **mlsNumbers** (required): Comma-separated MLS numbers
- **systemId** (default: `globalmls`): MLS region ID

## System IDs

Common Paragon MLS system IDs (the subdomain before `.paragonrels.com`):

| Region | System ID |
|--------|-----------|
| Eastern NY / Southern Adirondack | `globalmls` |
| InterMountain (Idaho) | `imls` |
| SW Colorado | `cren` |
| Hudson County, NJ | `hudson` |
| Georgia | `gamls` |
| Triangle Region, NC | `triangle` |

Check your local MLS website URL to find the correct system ID.

## How It Works

The server calls Paragon's public CollabLink API endpoints:

1. **CreateGuid** — generates a session GUID for API calls
2. **GetNotificationAppData** — resolves a listing GUID into MLS numbers
3. **GetListingDetails** — fetches property data for each MLS number

Property data is parsed from Paragon's nested JSON structure, handling both the "new" format (section-based `DetailOptions`) and "old" format (array-based).

## Limitations

- Paragon's API is public but unofficial; it may change without notice
- Each MLS region may format listing data differently; the parser handles common formats but edge cases may require custom handling
- No authentication is required for public listing data
- The API returns data over HTTP (not HTTPS) for some regions
- Rate limiting may apply; the server processes listings sequentially with no intentional delay