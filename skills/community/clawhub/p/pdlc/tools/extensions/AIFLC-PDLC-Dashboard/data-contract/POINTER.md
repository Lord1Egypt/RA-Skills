# Data Contract — Moved to AI-DFE

> **The dashboard's data schema is no longer owned by this extension (Option B, 2026-06-22).**

The schema that previously lived here (`dashboard-data-schema.json`) is now **owned by AI-DFE**, the family data fabric. There is a single source of truth for the dashboard's data contract:

- **Canonical schema (package source):** `ai-dfe/ai-dfe-rule-details/templates/data-samples/dashboard-data.schema.json`
- **Runtime schema (destination workspace):** `pdlc-ws/data/dashboard-data.schema.json`
- **Demand declaration:** `pdlc-ws/data/demands/dashboard-data.demand.md`

## How the dashboard gets its data now

The extension reads the AI-DFE data surface and never parses `*-state.md` files directly:

1. Read `{family}-ws/data/REGISTRY.json`.
2. Find the `dashboard-data.json` entry → resolve its path.
3. Read that file; the dashboard payload is the envelope's `data` body.

To populate the data surface, run `DAT__ all` (AI-DFE). See the AI-DFE package for details.
