# Pipeworx Govcon Analyst

GovCon Intel MCP — Compound tools that chain SAM.gov, USAspending,

## Setup

```json
{
  "mcpServers": {
    "govcon-intel": {
      "url": "https://gateway.pipeworx.io/mcp?task=govcon%20analysis"
    }
  }
}
```

## Compound tools (start here)

These combine multiple data sources into one call:

| Tool | Description |
|------|-------------|
| `govcon_contractor_profile` | Complete government contractor dossier — SAM.gov entity registration, federal award history (USAspen |
| `govcon_opportunity_scan` | Government contracting opportunity search — open SAM.gov opportunities, set-aside contracts (8(a), H |
| `govcon_agency_landscape` | Federal agency contracting landscape — spending overview, recent awards, SBIR program stats, and spe |

## Individual tools

For granular queries, these are also available:

| Tool | Description |
|------|-------------|
| `sam_search_opportunities` | Search active federal contract opportunities on SAM.gov. Filter by keyword, NAICS code, set-aside ty |
| `sam_get_opportunity` | Get full details for a specific federal contract opportunity by its solicitation number. Returns poi |
| `sam_entity_search` | Search for registered entities (vendors/contractors) in the SAM.gov entity database. Returns UEI, CA |
| `sam_set_aside_opportunities` | Search federal contract opportunities filtered by small business set-aside type. Useful for finding  |
| `usa_spending_by_agency` | Get federal spending breakdown by agency for a given fiscal year and optional quarter. Shows how muc |
| `usa_award_search` | Search federal contract awards by keywords, agency, date range, and NAICS code. Returns recipient, a |
| `usa_spending_by_category` | Get federal spending broken down by category: NAICS code, PSC (product/service code), recipient, awa |
| `usa_recipient_profile` | Get a specific contractor or recipient\ |
| `usa_spending_trends` | Get federal spending over time for given keywords or agency. Returns spending grouped by fiscal year |
| `sbir_search_awards` | Search SBIR/STTR awards by keyword, agency, year, company, or state. Returns awards with company nam |
| `sbir_get_award` | Get details for a single SBIR/STTR award by its award ID. Returns full award information including c |
| `sbir_search_solicitations` | Search SBIR/STTR solicitations (funding opportunities). Returns topics with description, agency, and |
| `sbir_company_awards` | Get all SBIR/STTR awards for a specific company. Returns the full list of awards with amounts, agenc |
| `sbir_agency_stats` | Get SBIR/STTR award counts by agency. If an agency is specified, returns the count for that agency.  |

## Data sources

- **Samgov**: SAM.gov MCP — Federal contract opportunities and entity registration data
- **Usaspending**: USAspending MCP — Federal spending data from USAspending.gov API
- **Sbir**: SBIR MCP — wraps the SBIR.gov public API (free, no auth)

## Tips

- Start with compound tools — they handle errors and combine data automatically
- Use `ask_pipeworx` if you're unsure which tool to use
- Use `remember`/`recall` to save intermediate findings
