# Mode Guide

This file defines how each implemented mode should behave.

## Shared Rules

Always:

1. Parse first.
2. Write `parsed.json`.
3. Read from `parsed.json` for downstream work.
4. Save final outputs under `task_output/`.
5. Save a source map or traceability file for downstream modes.

Do not:

- generate directly from raw OCR text when `parsed.json` is available
- invent facts not supported by the document
- hide uncertainty or warnings that MinerU OpenVINO inference was not used

## Mode: `parse`

### Goal

Create the canonical structured representation only.

### Inputs

- `file`
- optional `out`

### Outputs

- `parsed.json`
- `parsed.md`
- `tables/`
- `figures/`

### Return Summary

Include:

- file processed
- page count
- counts of headings, paragraphs, tables, formulas, figures, charts if available
- output folder path
- warnings if any

## Mode: `to-code`

### Goal

Turn a document into code-oriented artifacts.

### Best-Fit Inputs

- UI mockups
- screenshots
- forms
- product specs
- brochures
- workflow documents

### Allowed Outputs

- `component_map.json`
- `field_schema.json`
- `app.jsx`
- `index.html`
- `styles.css`
- `notes.md`
- `traceability.json`

### Behavior

- infer sections and components from parsed structure
- preserve labels, fields, buttons, lists, and tables
- use placeholders when business rules are not explicit
- record assumptions in `notes.md` and `traceability.json`

### Good Examples

- brochure image to landing page scaffold
- form screenshot to React form skeleton
- admin spec PDF to HTML + JSON field schema

## Mode: `to-data`

### Goal

Extract machine-readable data for automation.

### Best-Fit Inputs

- invoices
- reports
- forms
- schedules
- tables
- structured business documents

### Allowed Outputs

- `entities.json`
- `kv_pairs.json`
- `normalized.json`
- `requested_fields.json`
- `requested_fields_record.json`
- `tables.csv`
- `table_index.json`
- `traceability.json`

### Behavior

- keep original text and normalized values when useful
- preserve source block references for each record
- separate extraction from interpretation
- when the user provides a custom field list, generate a focused structured output for only those requested fields

### Good Examples

- invoice PDF to normalized invoice JSON
- invoice PDF to a custom JSON record containing only `invoice_number`, `invoice_date`, `total_amount`, and `vendor_name`
- annual report to CSV tables + entity summary
- application form to field-value JSON

## Mode Selection Hints

Prefer:

- `parse` when the user mainly wants structured OCR output
- `to-code` when the user wants implementation artifacts
- `to-data` when the user wants extraction/normalization

If unsure:

- default to `parse`
- then explain which downstream modes are available next
