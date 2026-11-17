# Stage 1.2 — Package Discovery

> Phase 1 (Configure). Loaded when DFE needs to learn a package's data interface. This is the heavy stage — it runs once per package, then is cached (discover-once).

## Purpose

Learn, for each installed package, what raw data it produces and what shape DFE must emit for it — by reading the package's own data interface. The package is the authority on its own data.

## Inputs

For each installed package `ai-{pkg}`:
- `.kiro/{family}/ai-{pkg}-rule-details/data-schema/SOURCE_MAP.md` — where raw data lives + extraction rules.
- `.kiro/{family}/ai-{pkg}-rule-details/data-schema/{pkg}-data.schema.json` — the output shape.
- `.kiro/{family}/ai-{pkg}-rule-details/data-schema/SCHEMA_README.md` — human docs (optional read).

## Logic

1. Enumerate installed packages from the family map (1.1).
2. For each, locate its `data-schema/` folder. If absent → the package has no interface yet; skip with a `no-interface` note (graceful).
3. Read `SOURCE_MAP.md`: resolve the declared source-file paths (relative to `{family}-ws/`), the field → source → extraction rules, the presence check, and any retention policy.
4. Read `{pkg}-data.schema.json`: capture `$schemaVersion` and the output shape.
5. Cache into `dfe-state.md` under `discovered.{ai-pkg}`: `schemaVersion`, `discoveredOn`, `schemaPath`, `sourceFiles[]`, `outputFile`, `lastGenerated: null`.

## Output

`discovered` registry in `dfe-state.md`. No data files written here.

## Re-Discovery

Re-read a package's interface ONLY when its `SOURCE_MAP.md`/schema timestamp changes, on `$schemaVersion` mismatch, or on `DAT__ discover`. Otherwise the cache stands.

## Edge Cases

| Situation | Behaviour |
|-----------|-----------|
| `data-schema/` missing | Package has no interface — skip, note `no-interface`. Not an error. |
| Schema invalid JSON | Report; skip that package; continue with the rest. |
| SOURCE_MAP references a non-existent source | Allowed — that field resolves to `null` at gather time. |
