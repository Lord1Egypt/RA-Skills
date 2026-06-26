---
name: paragon-mls-raw-listings
description: "Fetch raw JSON listing payloads from Paragon MLS. Use when debugging parser behavior, inspecting source payloads, or doing custom downstream analysis on unprocessed listing data."
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

# Paragon MLS Raw Listings

Use the `paragon-mls.raw_listings` MCP tool when you need the unprocessed Paragon payloads instead of the normalized parser output.

Prefer this skill for debugging, parser development, or custom downstream processing.

## Typical use

- inspect the original listing JSON when parsed fields look wrong
- compare different MLS region payload structures
- debug missing rent, tax, or square footage fields
- build custom logic on top of the raw source payload

## Example

```bash
mcporter call paragon-mls.raw_listings mlsNumbers="201918514,202012345" systemId="globalmls"
```

## Inputs

- `mlsNumbers` (required)
- `systemId` (default: `globalmls`)

## Output shape

Returns raw JSON payloads for each MLS number requested.

## Notes

- This is the best fallback when the normalized tools are missing a field you care about.
- Raw output is less stable across MLS regions than the parsed tools.
