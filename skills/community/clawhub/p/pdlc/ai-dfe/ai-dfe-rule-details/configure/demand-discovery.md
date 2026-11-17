
# Stage 1.3 — Demander Discovery

> Phase 1 (Configure). Loaded when DFE needs to learn what consumers want. Consumers are **discovered from a registry** (the demander twin of package discovery 1.2), not merely scanned from runtime drops. Ad-hoc drops remain supported as an escape hatch.

## Purpose

Register what each consumer needs, so shape (2.2) can assemble the right outputs. Consumers are discovered the same way producers are: from a declared index (`CONSUMER_REGISTRY.md`) that points at each consumer's own `data-demand/` declaration. This closes the producer/consumer asymmetry — producers ship a `SOURCE_MAP.md` and are enumerated via the family map; consumers ship a `data-demand/{name}.demand.md` and are enumerated via the consumer registry.

## Inputs

- `{family}-ws/data/CONSUMER_REGISTRY.md` — the index of registered consumers (`consumer`, `home`, `demandFile`, `outputFile`, `registeredOn`). Bootstrapped **empty** by the installer; each consumer appends its entry at install time.
- Each registered consumer's `data-demand/{name}.demand.md`, read from the consumer's own `home` folder (the consumer-side twin of a producer's `SOURCE_MAP.md`).
- `{family}-ws/data/demands/*.demand.md` — ad-hoc consumer drops with **no** registry entry (the user escape hatch).
- See `templates/demand-template.md` for the declaration format.

## Logic

1. Read `CONSUMER_REGISTRY.md`; enumerate registered consumers (parallel to package discovery 1.2 reading the family map).
2. **Self-healing scan (Step 1b):** After reading the registry, scan `{family}-ws/tools/extensions/*/data-demand/*.demand.md`. For any demand file whose consumer name has **no matching row** in `CONSUMER_REGISTRY.md`, auto-append a row (consumer name derived from the parent extension folder, `home` = the extension path, ISO timestamp sourced via shell command per the timestamp rule). Log: "Auto-registered {consumer} — demand file found but no registry entry existed." This closes install-time gaps for pre-existing workspaces, manual setups, or out-of-date installers. The registry remains authoritative, but is now also self-correcting.
3. For each registered consumer (including any just auto-registered), read its declared `data-demand/{name}.demand.md` from its `home`. **Materialize** the resolved declaration into `{family}-ws/data/demands/{name}.demand.md` so the shape stage (2.2) reads one place — `demands/` becomes a *resolved cache*, not the source of truth.
4. Also scan `{family}-ws/data/demands/` for any `*.demand.md` that has **no** matching registry entry → treat it as an **ad-hoc** (user-defined) consumer.
5. For each demand (registered or ad-hoc), parse: the **output file name** to produce in `data/`, the **fields needed** (field path, type, source domain = which `{pkg}-data.json` it draws from, description), and the **refresh expectation**.
6. Confirm each demanded field's source domain exists in the `discovered` registry (1.2). Unknown domain → record a warning; that field resolves to `null`.
7. Cache into `dfe-state.md` under `demands.{name}`: `consumer`, `demandFile`, `outputFile`, declared fields, `registered: true|false`, `lastGenerated: null`.
8. If a DEMAND requires a DFE-owned aggregation schema, note which schema validates its output (DFE owns demand/aggregation schemas; per-package schemas stay with packages).

## Output

`demands` registry in `dfe-state.md`, each entry flagged `registered: true|false`. No data files written here.

## Edge Cases

| Situation | Behaviour |
|-----------|-----------|
| Registry empty **and** no ad-hoc drops | No consumer outputs to shape — DFE still produces per-package data (Layer 1). |
| Registered but `data-demand/` missing/malformed | Warn, skip that consumer (graceful, not an error). |
| Demand file exists in `tools/extensions/*/data-demand/` but no registry row | **Self-healed:** auto-register the consumer (Step 1b) and continue. Logged as auto-registration. |
| Registry entry whose consumer `home` is gone | Flag a stale/orphan consumer (surfaced in `DAT__ status` / `DFA__`); skip. |
| Ad-hoc demand in `demands/` with no registry entry | Honored; recorded with `registered: false`. |
| Two DEMANDs target the same output file | Report a collision; do not silently merge. |
| DEMAND references an unknown source domain | Warn; that field → `null` at shape time. |
| Cross-family field requested | Resolve only in master mode (`operate/cross-family.md`); otherwise `null` (single-family graceful degradation). |
