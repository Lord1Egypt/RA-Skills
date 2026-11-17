# Stage 2.6 — Cross-Family Operation (Master Mode)

> Phase 2 (Operate). Multi-family aggregation. Deferred in practice until a 2nd family exists, but the mechanism is defined here.

## Purpose

When more than one family shares a workspace, one DFE becomes **master** and operates every family's data — each in that family's own `data/`. No shared folder; no mixing.

## Master Promotion

- **Auto-detection (default):** the newest DFE version becomes master (newest = potentially more capable).
- **Override:** `DAT__ master --set {family}` forces a specific family's DFE as master.
- `DAT__ master` reports the current master.
- Single-active with dormancy: the master runs; other families' DFEs go dormant.

## Logic

1. Master discovers all families present (each has its own `{family}-ws/`).
2. For each family, the master runs Configure → Operate → Govern **in that family's own territory** — it walks to the neighbour's house and does the work there.
3. The master NEVER pulls neighbour data into its own family's folder. Each family's data stays in its own `{family}-ws/data/`.

## Cross-Family Data Exchange

No special mechanism. Family B's shaped data already sits in `familyB-ws/data/`. When a Family A consumer DEMANDs cross-family info:
1. The master reads from `familyB-ws/data/` (already shaped, already there).
2. It includes the value in `familyA-ws/data/{consumer-output}.json`.
3. Family A's `REGISTRY.json` lists the cross-family entry under `cross-family.{B}.files`, and the consumer resolves it through its own registry.

## Graceful Degradation

In single-family mode, `cross-family` in `REGISTRY.json` is empty and any cross-family DEMAND field resolves to `null`. No error.
