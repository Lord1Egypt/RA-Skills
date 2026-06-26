# Output Contracts

This file defines the folder layout and file contracts.

## Default folder layout

```text
artifacts/<document_stem>/
├── parsed.json
├── parsed.md
├── traceability.json
├── tables/
├── figures/
└── task_output/
```

If the user passes `out=...`, use that directory instead.

## Parse outputs

### `parsed.json`
Required for every successful run.

### `parsed.md`
Required for every successful run.
Purpose:
- human-readable rendering of the parse result

### `tables/`
Optional.
Write extracted CSVs or table assets here.

### `figures/`
Optional.
Write extracted figures here.

---

## Downstream outputs

### `task_output/`
Required for non-parse modes.

Examples:
- `task_output/app.jsx`
- `task_output/index.html`
- `task_output/entities.json`
- `task_output/slide_outline.md`

### `traceability.json`
Required for non-parse modes.

Purpose:
- map generated artifacts back to source page/block IDs
- record assumptions or low-confidence derivations

Example:
```json
{
  "artifact": "task_output/app.jsx",
  "mappings": [
    {
      "generated_unit_id": "component.signup_email_field",
      "generated_text": "Email input field with label and helper text",
      "source_refs": [
        {"page_id": "page_1", "block_id": "p1_b12"},
        {"page_id": "page_1", "block_id": "p1_b13"}
      ],
      "assumption": "Validation rule was not explicit in source."
    }
  ]
}
```

## Failure contract

If a run fails:
- do not create empty success artifacts
- optionally write `error.json` with:
  - stage
  - message
  - input file
  - mode
  - timestamp

Example:
```json
{
  "stage": "parse",
  "message": "Unsupported file type",
  "input_file": "./docs/foo.xyz",
  "mode": "parse",
  "timestamp": "2026-04-08T16:00:00Z"
}
```

## Naming conventions

- use lowercase snake_case for filenames
- use stable IDs for pages, blocks, tables, and figures
- use relative paths inside JSON when files live inside the same artifact folder

## Quality notes

- prefer explicit omission over silent loss
- if tables or formulas are detected but not reconstructed, note that in `parse_info.warnings`
- if output is partially inferred, record it in `traceability.json`
