# Stage 3.1 — Validation

> Phase 3 (Govern). Validate every file against its schema BEFORE it is written. Block-on-fail.

## Purpose

Guarantee the data surface is always schema-conformant. No invalid file ever reaches `data/`.

## Inputs

- A staged output file (from gather 2.1 or shape 2.2) + its declared schema.

## Logic

1. Resolve the file's schema:
   - per-package data → `.kiro/{family}/ai-{pkg}-rule-details/data-schema/{pkg}-data.schema.json`
   - demand output → the DFE-owned aggregation schema in `{family}-ws/data/` (e.g. `dashboard-data.schema.json`)
2. Validate the metadata envelope (`$schema`, `$schemaVersion`, `$generatedBy`, `$generatedOn`, `$family`, `$package`, `data`) and the payload against the schema.
3. Check `$schemaVersion` matches the schema's version; on mismatch → trigger re-discovery (1.2) for that package.
4. **Pass** → release the file to distribute (2.3). **Fail** → block the write, report the exact field/expected/actual, and keep the prior version in place.

## Output

Pass/fail verdict per file. On fail, a precise validation report; the data surface is left unchanged for that file.

## Mermaid-Completeness Check

In addition to schema validation, apply this content-completeness check for any field declared as "fenced ```mermaid extraction" in a SOURCE_MAP (e.g. `arch.c4Diagrams.{level}.mermaid`, `arch.diagrams.{key}.mermaid`, `ux.flows[].mermaid`):

1. Read the `path` value from the same object (e.g. `arch.c4Diagrams.l1.path`, or `ux.flows[n].path`).
2. If `path` is `null` or the referenced file does not exist → PASS (source absent, `null` is correct).
3. If the referenced file exists, scan it for a ` ```mermaid ` fenced block.
4. If the file contains a mermaid block BUT the `mermaid` field is `null` → **FAIL**: report `"Mermaid extraction missed: source file [{path}] contains a mermaid block but field is null"`.
5. If the file contains no mermaid block AND `mermaid` is `null` → PASS (correctly degraded).
6. If both file and field are populated → PASS.

**Array fields (e.g. `ux.flows[]`):** Apply the check per-item — iterate every object in the array and validate its `path`/`mermaid` pair independently.

**Severity:** BLOCK (same as schema validation — the file is not written with `null` when content is available).

**Remediation:** Re-run gather (2.1) for the affected package with attention to the Mermaid Block Extraction procedure in `operate/gather.md`.

## Artifact Object-Type Check

For `dashboard-data.json` specifically, apply this structural check on the `packages[].artifacts` array:

1. For each package in each project, inspect `artifacts`.
2. If `artifacts` is not an array → FAIL (schema violation).
3. For each item in `artifacts`:
   - If the item is a **plain string** (not an object) → **FAIL**: report `"Artifact shape violation: packages['{code}'].artifacts[{index}] is a plain string '{value}' — must be an object with {name, status, path}"`.
   - If the item is an object but missing `name` or `status` → **FAIL**: report the missing required properties.
4. All items are objects with at minimum `name` + `status` → PASS.

**Severity:** BLOCK — the dashboard renders `undefined` across the PM tab when this contract is violated.

**Remediation:** Re-run shape (2.2) with attention to the Artifact Object Transform rule in `operate/shape.md`.

## `DAT__ validate`

`DAT__ validate` runs this stage as a **dry-run** over existing files in `data/` without regenerating anything — a fast conformance check. `DFA__ schema` is the deeper standalone audit (the agent).
