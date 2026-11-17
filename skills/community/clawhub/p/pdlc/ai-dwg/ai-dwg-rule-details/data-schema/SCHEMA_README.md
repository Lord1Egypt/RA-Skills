# Schema README — AI-DWG (`dwg-data.json`)

**Package:** AI-DWG — AI-Driven Workspace Generator
**Schema:** `dwg-data.schema.json` · **Version:** 1.0.0
**Produced file:** `{family}-ws/data/dwg-data.json` · **Scope:** per-project

## Purpose

Machine-readable projection of AI-DWG's output — whether a dev workspace was generated and the identity it embedded (architecture vs. product vs. none, system/tech identity). AI-DWG is a generator with no state file; this data answers "is the workspace ready, and what is it?".

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `projectId` | `workspace-rules.md` Identity Assembly | Correlation key |
| `workspaceGenerated` | marker presence | Is the dev workspace ready? |
| `identityType` | `workspace-rules.md` | architecture / product / none |
| `primaryTechnology` / `architectureStyle` | Architecture Identity | Tech identity for dashboards |

## Consumers
Family-status demand · AIFLC-PDLC-Dashboard (workspace-ready indicator) · `DFA__`.

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |
