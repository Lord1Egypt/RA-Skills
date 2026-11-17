<!-- AI-DFE consumer registry. The runtime copy lives at {family}-ws/data/CONSUMER_REGISTRY.md. -->
# Consumer Registry — {family}

**Maintained for:** AI-DFE — AI-Driven Data Fabric
**Location (runtime):** `{family}-ws/data/CONSUMER_REGISTRY.md`

> The demander index. Every consumer that wants service from AI-DFE registers here at install time (Obligation 1). Demander discovery (Stage 1.3) reads this file to enumerate consumers, then resolves each one's `data-demand/{name}.demand.md`. The installer bootstraps this file **empty** (no rows); consumers append a row on install and remove it on uninstall.
>
> A consumer that is *not* listed here is **not** discovered automatically — it is served only if a user drops an ad-hoc `*.demand.md` into `{family}-ws/data/demands/` (the escape hatch).

## Registered Consumers

| consumer | home | demandFile | outputFile | registeredOn |
|----------|------|------------|------------|--------------|
| {consumer-name} | {consumer's folder, e.g. tools/extensions/AIFLC-PDLC-Dashboard} | {home}/data-demand/{name}.demand.md | {family}-ws/data/{name}.json | {ISO-8601} |

## Field Notes

| Field | Meaning |
|-------|---------|
| `consumer` | Consumer name — MUST match the `Consumer:` in its `data-demand/{name}.demand.md` and the `consumer` recorded in `REGISTRY.json` |
| `home` | The consumer's own folder (where its `data-demand/` lives) — the contract travels with the consumer |
| `demandFile` | Path to the consumer's declaration (`{home}/data-demand/{name}.demand.md`) |
| `outputFile` | The data file DFE produces for this consumer (`{family}-ws/data/{name}.json`) |
| `registeredOn` | ISO-8601 timestamp of registration. **Source it from a shell command, never from a hosted/internal time tool** (see core-engine "Obtaining the Current Timestamp"). |

## Rules

1. The installer bootstraps this file empty. Do not pre-populate rows.
2. A consumer adds exactly one row per demand it registers, and removes its row(s) on uninstall.
3. Registration (a row here + a shipped `data-demand/` file) is what makes a consumer *discoverable*. Reading `REGISTRY.json` is how it *consumes*. Both are required (Obligation 1 + Obligation 2).
