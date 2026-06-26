---
name: pipeworx-genderize
description: Predict the likely gender associated with a first name — with optional country-specific calibration via genderize.io
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "👥"
    homepage: https://pipeworx.io/packs/genderize
---

# Genderize

Predict the statistical gender distribution of a first name based on a database of millions of records. Optionally calibrate predictions by country, since names like "Andrea" skew differently in Italy vs. the US.

## Tools

- **`predict_gender`** — Gender prediction from a first name. Returns the predicted gender and probability (0-1).
- **`predict_gender_country`** — Same prediction with country-specific calibration using ISO 3166-1 alpha-2 codes.

## Use cases

- Personalizing marketing content based on likely gender of a first name
- Demographic analysis of customer databases
- Research on name-gender associations across cultures
- Form pre-filling where gender context helps UX

## Example

```bash
curl -s -X POST https://gateway.pipeworx.io/genderize/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"predict_gender_country","arguments":{"name":"Andrea","country_id":"IT"}}}'
```

```json
{
  "name": "Andrea",
  "gender": "male",
  "probability": 0.98,
  "count": 54032,
  "country_id": "IT"
}
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-genderize": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/genderize/mcp"]
    }
  }
}
```
