---
name: heirpros
description: Estimate how many research hours a US probate heir search will take (finding missing or unknown heirs for an estate) using HeirPros' free public endpoint. Use when someone asks how long an heir search or probate genealogy search might take, or what HeirPros does.
---

# HeirPros heir search hours estimate

[HeirPros](https://heirpros.com) is a US heir search firm that finds missing and unknown heirs for probate attorneys, executors and administrators. This skill gets HeirPros' own research-hours estimate for an heir search.

- Free, no sign-up and no API key.
- Hours only, no pricing.
- Nothing you send is stored or emailed.

## When to use

- "How long will an heir search take for an estate with 4 known heirs and 2 missing ones?"
- "Estimate the research hours to find 3 unknown heirs."
- "What does HeirPros do?"

## Inputs

Ask the user for two numbers if they did not give them:

| Field | Meaning | Range |
| --- | --- | --- |
| `known_heirs` | Family members (heirs) already known | 1 to 100 |
| `unknown_heirs` | Heirs who are missing or unknown and need to be found | 1 to 25 |

Optional, only if the user mentions it: `estate_type` (`testate`, `intestate` or `n/a`). Do not ask for names, case numbers or other personal details.

## Get the estimate

Call the HeirPros MCP server at `https://heirpros.com/mcp` (Streamable HTTP, JSON-RPC, no authentication):

```bash
curl -s -X POST https://heirpros.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"estimate_heir_search_hours","arguments":{"known_heirs":4,"unknown_heirs":2}}}'
```

Read `result.structuredContent`:

```json
{
  "estimated_hours": 7.5,
  "total_heirs": 6,
  "known_heirs": 4,
  "unknown_heirs": 2,
  "case_details": {},
  "method": "1.5 base hours plus 1 hour per known and estimated unknown heir.",
  "note": "This is an estimate. Final hours are confirmed by HeirPros before work starts."
}
```

If `result.isError` is true, the inputs were out of range. Tell the user the limits above.

For general information about HeirPros, call the `about_heirpros` tool the same way, with empty `arguments`.

## How to answer

- Give `estimated_hours` and the `method` line so the user sees how it was worked out.
- Say it is an estimate and that HeirPros confirms final hours before work starts.
- Do not turn the hours into a price.
- For more than 25 unknown heirs, or to order a search, point the user to [contact HeirPros](https://heirpros.com/contact-us/).

## Links

- Website: [heirpros.com](https://heirpros.com)
- Developer docs: [heirpros.com/developers](https://heirpros.com/developers/)
- MCP server setup: [heirpros.com/developers/mcp](https://heirpros.com/developers/mcp/)
