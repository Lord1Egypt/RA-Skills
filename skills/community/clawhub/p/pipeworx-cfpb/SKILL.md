# Cfpb

CFPB MCP — Consumer Financial Protection Bureau complaint database (free, no auth)

## cfpb_search_complaints

Search consumer complaints by keyword, company, product, or date range. Returns complaint narratives

## cfpb_company_complaints

Get recent complaints against a specific company (e.g., 'Wells Fargo'). Returns narratives, company 

## cfpb_get_complaint

Retrieve full details for a specific complaint by ID. Returns narrative, company response, resolutio

## cfpb_top_companies

Find companies with the most complaints in a date range. Returns ranked list with company names and 

## cfpb_product_breakdown

Get complaint counts by product category (e.g., 'Credit Card', 'Mortgage'). Filter by company or dat

```json
{
  "mcpServers": {
    "cfpb": {
      "url": "https://gateway.pipeworx.io/cfpb/mcp"
    }
  }
}
```
