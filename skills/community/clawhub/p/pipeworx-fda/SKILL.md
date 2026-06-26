---
name: pipeworx-fda
description: US FDA open data — adverse drug event reports, drug labeling/package inserts, and food recall enforcement actions
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "💊"
    homepage: https://pipeworx.io/packs/fda
---

# FDA Open Data

Search the US Food and Drug Administration's public databases. Pull adverse drug event reports (FAERS), look up drug labeling and package inserts, and browse food recall enforcement actions. All data is open and requires no API key.

## Tools

| Tool | Description |
|------|-------------|
| `search_drug_events` | Search FDA adverse drug event (FAERS) reports by drug name, reaction, or keyword |
| `search_drug_labels` | Search drug labeling / package inserts by brand name, generic name, or active ingredient |
| `search_food_recalls` | Search food recall enforcement actions by product name, company, or reason |

## Use cases

- Investigating reported side effects for a specific medication
- Looking up official prescribing information and contraindications
- Monitoring food recalls for safety-critical applications
- Pharmacovigilance research across the FAERS database

## Example: adverse events for metformin

```bash
curl -s -X POST https://gateway.pipeworx.io/fda/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_drug_events","arguments":{"query":"metformin","limit":3}}}'
```

Returns reported reactions, drug dosage info, patient demographics, and outcome classifications.

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-fda": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/fda/mcp"]
    }
  }
}
```
