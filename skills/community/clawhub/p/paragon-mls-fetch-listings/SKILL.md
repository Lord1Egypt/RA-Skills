---
name: paragon-mls-fetch-listings
description: "Fetch all active property listings from a Paragon MLS shared listing GUID. Use when resolving a Paragon link or GUID into the parsed property records behind it."
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

# Paragon MLS Fetch Listings

Use the `paragon-mls.fetch_listings` MCP tool to resolve a shared Paragon MLS GUID into all parsed active listings behind it.

Prefer this skill when the input is a Paragon share link, GUID, or collaboration page rather than a single MLS number.

## Typical use

- unpack a Paragon shared link into the individual properties it contains
- review all active listings attached to a GUID
- turn one collaboration link into structured property records for downstream analysis

## Example

```bash
mcporter call paragon-mls.fetch_listings mlsId="6d70b762-36a4-4ac0-bedd-d0dae2920867" systemId="globalmls"
```

## Inputs

- `mlsId` (required)
- `systemId` (default: `globalmls`)

## Output shape

Returns a JSON object with:

- `count`
- `properties[]`

Each property is already parser-normalized, so this is the best entry point before running deeper analysis.

## Notes

- This depends on the MLS region's public CollabLink endpoints.
- If a GUID resolves but parsing is weak, inspect the source data with the raw-listings skill.
