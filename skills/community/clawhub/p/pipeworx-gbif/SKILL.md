---
name: pipeworx-gbif
description: Global biodiversity data — search species, retrieve taxonomy, and find georeferenced occurrence records via GBIF
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🦎"
    homepage: https://pipeworx.io/packs/gbif
---

# GBIF — Global Biodiversity Information Facility

GBIF aggregates biodiversity data from thousands of institutions worldwide — over 2 billion occurrence records. Search the taxonomic backbone, get species classification details, and retrieve georeferenced observations filtered by country.

## Tools

- **`search_species`** — Full-text search across the GBIF species backbone (e.g., "Homo sapiens", "oak", "Panthera leo")
- **`get_species`** — Detailed taxonomic record by GBIF taxon key: kingdom, phylum, class, order, family, genus
- **`get_occurrences`** — Georeferenced observation records for a taxon, optionally filtered by ISO country code

## Ideal for

- Ecological research — where has a species been observed?
- Conservation tools that need range maps based on real observations
- Taxonomy lookups for scientific or educational content
- Biodiversity dashboards comparing species richness across countries

## Example: wolf sightings in Germany

```bash
# First, search for the species
curl -s -X POST https://gateway.pipeworx.io/gbif/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_species","arguments":{"query":"Canis lupus","limit":1}}}'

# Then get occurrences with the taxon key, filtered to Germany
curl -s -X POST https://gateway.pipeworx.io/gbif/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_occurrences","arguments":{"key":5219173,"country":"DE","limit":10}}}'
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-gbif": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/gbif/mcp"]
    }
  }
}
```
