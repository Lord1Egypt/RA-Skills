# Schema README — AI-DFE (`dfe-data.json`)

**Package:** AI-DFE — AI-Driven Data Fabric
**Schema:** `dfe-data.schema.json`
**Version:** 1.0.0
**Produced file:** `{family}-ws/data/dfe-data.json`

---

## Purpose

`dfe-data.json` is AI-DFE's self-report: a machine-readable summary of the data layer's own health — which packages are discovered and fresh, which demands are registered, and roll-up counts. It lets dashboards and the `DFA__` agent treat "the state of the data fabric" as just another data file.

## Fields

| Field | Type | Meaning |
|-------|------|---------|
| `status` | enum | `complete` \| `active` |
| `isMaster` | boolean | Whether this DFE is master in a multi-family workspace |
| `masterFamily` | string\|null | Which family's DFE is master |
| `lastFullPass` | date-time\|null | Last `DAT__ all` completion |
| `packages[]` | array | Per-package: name, schemaVersion, outputFile, lastGenerated, status |
| `demands[]` | array | Per-consumer: name, consumer, outputFile, lastGenerated |
| `counts` | object | packagesDiscovered, dataFiles, demands, historySnapshots |

## Metadata Envelope

Every `dfe-data.json` carries the standard envelope: `$schema` (workspace-root-relative), `$schemaVersion`, `$generatedBy: "AI-DFE"`, `$generatedOn`, `$family`, `$package: "AI-DFE"`, and `data`.

## Consumers

- The `DFA__` data-fabric agent (health framing).
- Any family-status or dashboard demand that wants "is the data layer healthy?".

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial self-report schema. |
