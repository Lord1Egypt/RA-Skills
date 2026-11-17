# Stage 2.1 — Gather (Layer 1)

> Phase 2 (Operate). Sources → one `{pkg}-data.json` per package. This is the faithful projection of each package.

## Purpose

Produce one validated `{pkg}-data.json` per discovered package by reading its declared sources and extracting fields per its SOURCE_MAP.

## Inputs

- `dfe-state.md` `discovered.{ai-pkg}` (cached source-file list + schema path).
- The actual declared source files under `{family}-ws/…`.

## Logic

For each package in the `discovered` registry:
1. Run the presence check (from SOURCE_MAP). If the package hasn't run, produce a `{pkg}-data.json` with all payload fields `null` and `status: not-run`. Continue (graceful).
2. For each field in the schema, apply its extraction rule against the declared source file (e.g. parse a state file's front-matter, count register rows, read a JSON value).
3. A missing individual source → that field = `null` (never error).
4. Wrap the payload in the metadata envelope (see `templates/SOURCE_MAP.md` and the schema contract): `$schema`, `$schemaVersion`, `$generatedBy: "AI-DFE"`, `$generatedOn`, `$family`, `$package`, `data: { … }`.
5. Validate against the package schema (hand to 3.1). On failure → block this file, report, keep the prior version.

## Extraction Techniques (semi-structured sources)

Some packages declare rich fields (the dashboard `po`/`arch`/`ux` panes and the enriched `ideas[]`) that come from the **structured sub-sections** of deliverable artifacts. Gather supports these techniques — always reading the *structured* part, never free-form prose:

| Technique | Used for | Rule |
|-----------|----------|------|
| **Markdown table parse** | roadmap horizon table, release table, stakeholder register, NFR tables, tech-stack tables, screen inventory, ADR register | Read the table rows under the named heading → one object per row. |
| **Fenced ```mermaid extraction** | C4 L1/L2/L3 diagrams, security/data/api/infra diagrams, user-flow diagrams | Copy the **verbatim** fenced ```mermaid block from the doc into the field's `mermaid` string. If a source has none, leave `null` (the renderer/`shape` may generate L3 only). |
| **Folder scan** | personas, journeys, flows, epics, ADR files, design-system files, per-idea deliverables | Enumerate files in the declared folder → one `{ name, path, status }` object each; `path` is workspace-root-relative; exclude internal markers (`*-state.md`, `*_README.md`, shared registers). |
| **File-existence check** | `dorReady`/`dodReady`, `baselineDefined` | Boolean = the named file exists; also record its path when present. |
| **`dashboard-summary` block** | free-form roll-ups (vision status/statement, velocity trend, NFR targets, techStack grouping, design-system/wireframe/IA/accessibility counts) | Read the machine-readable `dashboard-summary` YAML block emitted in the package's `*-state.md` (fenced ```yaml **or** ~~~yaml — match the `dashboard-summary:` key). Fall back to safe defaults/zeros when absent. |
| **Enum normalisation** | idea `stage` (lowercase), package `status` | Normalise to the renderer's vocabulary (e.g. register `Status: Routed` → `stage: "routed"`); keep the original where a back-compat field exists. |

These run during Layer-1 gather so the produced `{pkg}-data.json` already carries the rich fields — Layer-2 shape (2.2) then only reshapes from `{pkg}-data.json`, never re-reading sources (its Hard Rule is preserved).

## MANDATORY: Mermaid Block Extraction

When a SOURCE_MAP declares a field's extraction rule as "fenced ```mermaid extraction" (applies to `arch.c4Diagrams` and `arch.diagrams` in AI-ADLC, `ux.flows[].mermaid` in AI-UXD, and any future package declaring diagram fields):

1. Read the file at the declared source path (workspace-root-relative).
2. Search for the FIRST occurrence of a line starting with ` ```mermaid `.
3. Capture all content from the line AFTER ` ```mermaid ` up to (but not including) the closing ` ``` `.
4. Trim leading/trailing whitespace from the captured block.
5. Assign the result as a **string** to the target `mermaid` field.
6. If the file exists but contains NO ` ```mermaid ` block → field = `null` (graceful degradation).
7. If the file does NOT exist → field = `null` (graceful degradation).

**Multi-block selection:** When a source file contains multiple mermaid blocks, or when multiple diagram keys reference different files, match by diagram-type keyword in the block's first line:

| Target field | Match keyword | Source file pattern |
|---|---|---|
| `c4Diagrams.l1` | `C4Context` | `*System_Context*` / `*02_*` |
| `c4Diagrams.l2` | `C4Container` | `*Container*` / `*03_*` |
| `c4Diagrams.l3` | `C4Component` | `*Component*` / `*11_*` |
| `diagrams.security` | `sequenceDiagram` or `flowchart` | Security / Identity doc |
| `diagrams.data` | `erDiagram` or `classDiagram` | Data Architecture doc |
| `diagrams.api` | `sequenceDiagram` or `graph` | API Architecture doc |
| `diagrams.infrastructure` | `graph` or `flowchart` | Integration / Infrastructure doc |
| `ux.flows[].mermaid` | `flowchart`, `graph`, `stateDiagram`, or `sequenceDiagram` | `05_User_Flows/Flow_NN_*.md` (one file per flow) |

If no block matches the expected keyword, fall back to the FIRST ` ```mermaid ` block in the file.

**Per-file extraction (folder scan + mermaid):** When the SOURCE_MAP declares a folder scan that also extracts mermaid (e.g. AI-UXD's `05_User_Flows/`), apply the extraction per-file:
- For each file in the scanned folder, read it and extract the FIRST ` ```mermaid ` block using the 7-step procedure above.
- Assign to the `mermaid` field of that file's object in the output array.
- A file with no mermaid block → `mermaid: null` for that entry (graceful per-item, not per-array).

**Non-negotiable rule:** A `null` mermaid value is acceptable ONLY when:
- The source file does not exist (package not run), OR
- The source file genuinely contains no ` ```mermaid ` fenced block.

If the source file exists AND contains a ` ```mermaid ` block, the `mermaid` field MUST be populated. A `null` in this scenario is a **gather bug**, not graceful degradation.

## Output

One `{pkg}-data.json` per package, staged for distribution (2.3).

## Notes

- Gather reads raw sources ONLY. It never reads other `{pkg}-data.json` files (that's Layer 2's job).
- `$generatedOn` is the basis for monitoring (2.4) — set it to the time of this gather.
