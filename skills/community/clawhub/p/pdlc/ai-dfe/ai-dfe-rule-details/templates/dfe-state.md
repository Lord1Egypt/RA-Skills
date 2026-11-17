<!-- AI-DFE state marker. Generated and owned by AI-DFE. Do not hand-edit. -->
# DFE State

**Marker for:** AI-DFE — AI-Driven Data Fabric
**Status:** {complete | active}
**Family:** {family}
**Last full pass:** {ISO-8601}

> This file is DFE's single source of truth for what it has discovered and produced. It lives in `{family}-ws/data/`. Re-derivation may overwrite it — do not hand-edit.

```yaml
data-fabric:
  family:
    code: "{family}"                 # e.g. pdlc
    workspaceRoot: "{AIFLC-workspace-root}"
    dataRoot: "{family}-ws/data"
    projectsRoot: "{family}-ws/projects"
    portfolioRoot: "{family}-ws/portfolio"
    ideasRoot: "{family}-ws/ideas"
  master:                            # multi-family only; null in single-family mode
    isMaster: {true|false}
    masterFamily: "{family|null}"
  discovered:
    ai-{pkg}:
      schemaVersion: "{semver}"
      discoveredOn: "{ISO-8601}"
      schemaPath: ".kiro/{family}/ai-{pkg}-rule-details/data-schema/{pkg}-data.schema.json"
      sourceFiles:
        - "{family}-ws/projects/PRJ-{ABBREV}-{slug}/{role}/{file}"
      outputFile: "{family}-ws/data/{pkg}-data.json"
      retention: "{forever | keep-last-N | keep-days-T}"
      lastGenerated: "{ISO-8601 | null}"
      status: "{discovered | not-run | no-interface | orphan}"
  demands:
    {name}:
      consumer: "{consumer-name}"
      registered: {true|false}         # true = from CONSUMER_REGISTRY.md; false = ad-hoc drop in data/demands/
      demandFile: "{family}-ws/data/demands/{name}.demand.md"
      outputFile: "{family}-ws/data/{name}.json"
      schema: "{family}-ws/data/{name}.schema.json"
      lastGenerated: "{ISO-8601 | null}"
```

## Field Notes

| Field | Meaning |
|-------|---------|
| `discovered.{pkg}.sourceFiles` | Cached at discovery; basis for monitor (2.4) staleness checks |
| `discovered.{pkg}.lastGenerated` | When `{pkg}-data.json` was last written; compared against source mtimes |
| `discovered.{pkg}.status` | `not-run` = sources absent (null data); `no-interface` = no data-schema/; `orphan` = package gone |
| `demands.{name}.schema` | DFE-owned aggregation schema validating this demand output |
| `demands.{name}.registered` | `true` = consumer is in `CONSUMER_REGISTRY.md` (shipped/installed); `false` = ad-hoc drop in `data/demands/` (user escape hatch) |
| `master.*` | Populated only when multiple families coexist (single-active master,) |
