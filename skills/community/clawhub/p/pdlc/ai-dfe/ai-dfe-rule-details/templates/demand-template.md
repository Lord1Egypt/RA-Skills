# DEMAND — {consumer-name}

> **Template.** A consumer (dashboard, extension, report) declares what data it needs by **shipping this file in its own folder** at `{consumer-home}/data-demand/{name}.demand.md` (the consumer-side twin of a producer's `data-schema/SOURCE_MAP.md` — the contract travels *with* the consumer). At install the consumer also adds a row to `{family}-ws/data/CONSUMER_REGISTRY.md` (Obligation 1). AI-DFE's demander discovery (Stage 1.3) resolves this declaration and materializes it into `{family}-ws/data/demands/{name}.demand.md`, then shapes the output from per-package JSON (Layer 1) — the consumer never touches raw sources. Replace every `{placeholder}`.
>
> *Ad-hoc use:* a user may instead drop this file directly into `{family}-ws/data/demands/` with no registry entry — DFE honors it as an ad-hoc consumer (`registered: false`).

**Consumer:** {consumer-name}
**Output file:** `{name}.json` (AI-DFE writes this to `{family}-ws/data/`)
**Refresh:** {on-demand | session-start | on-change}
**Scope:** {single-project | portfolio | cross-family}

---

## Fields Needed

Declare each field the output must contain. `source domain` = which package's `{pkg}-data.json` it draws from (Layer 1). Use `aggregate` for roll-ups across projects.

| Field path (in output `data`) | Type | Source domain | Description |
|--------------------------------|------|---------------|-------------|
| `{field}` | {string\|number\|boolean\|array\|object} | `{pkg}-data` | {what it is} |
| `projects[].{field}` | array | aggregate over `{pkg}-data` per project | {roll-up across projects} |
| `{field}` | {type} | `cross-family:{other}` | {only resolves in master mode; else null} |

## Shape Notes

- {Any transform: rename, compute, filter, sort, count.}
- {Which fields are required vs. nullable.}

## How This Consumer Reads Its Data (HARD RULE)

1. Know ONE path: `{family}-ws/data/REGISTRY.json`.
2. Read the registry, find the entry for `{name}.json`, get its `path`.
3. Open that path and read the JSON.
4. NEVER hardcode `{family}-ws/data/{name}.json` — always resolve via the registry.

## Schema

AI-DFE owns the validating schema for this demand output: `{family}-ws/data/{name}.schema.json` (DFE-owned aggregation schema). The consumer does not ship its own copy.
