---
name: paragon-mls-fetch-property
description: "Fetch a single property from Paragon MLS by MLS number and system ID. Use when looking up one listing's parsed details, including address, price, beds, baths, rents, taxes, and listing links."
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

# Paragon MLS Fetch Property

Use the `paragon-mls.fetch_property` MCP tool to look up one property by MLS number.

Prefer this skill when the user wants one listing summarized, not a portfolio analysis.

## Typical use

- look up a single property from an MLS number
- inspect parsed rent, tax, square footage, and bed/bath fields
- grab map and listing links for one deal
- sanity-check whether the parser extracted usable investment inputs

## Example

```bash
mcporter call paragon-mls.fetch_property mlsNumber="201918514" systemId="globalmls"
```

## Inputs

- `mlsNumber` (required)
- `systemId` (default: `globalmls`)
- `mlsId` (optional, mainly for link generation)

## Output shape

Expect parsed fields like:

- address and formatted full address
- current and previous price when available
- beds, baths, square footage, year built
- unit rents, taxes, HOA, remarks
- Google Maps and Paragon/Zillow-style links

## Notes

- Some MLS regions expose different field labels, so missing fields do not always mean missing property data.
- If the parsed result looks incomplete, use the raw-listings skill next.
