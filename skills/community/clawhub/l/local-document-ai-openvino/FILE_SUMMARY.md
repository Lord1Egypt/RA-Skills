# File Summary

This skill package is organized around one orchestrator and three user-facing modes:

- `parse`
- `to-data`
- `to-code`

## Top level

- `SKILL.md`
  - Main skill definition and invocation guidance.

- `requirements.txt`
  - Base Python dependencies for the local parser and wrapper scripts.
  - Does not auto-install the third-party PaddleOCR-VL OpenVINO wheel.

- `FILE_SUMMARY.md`
  - This file.

- `TEST_CHECKLIST.md`
  - Validation checklist for publish readiness.

## Agents metadata

- `agents/openai.yaml`
  - UI metadata for skill chips, skill lists, and default invocation prompt.

## References

- `references/schema.md`
  - Canonical structured parse schema used between parse and downstream transforms.

- `references/mode_guide.md`
  - Mode behaviors and output expectations.

- `references/output_contracts.md`
  - Artifact folder layout and output file contracts.

## Example configs

- `configs/parse_test.json`
  - Example manifest for `parse`.

- `configs/to_data_test.json`
  - Example manifest for `to-data`.

- `configs/to_code_test.json`
  - Example manifest for `to-code` with `html-css`.

- `configs/to_code_notebook_test.json`
  - Example manifest for `to-code` with `jupyter-notebook`.

## Core scripts

- `scripts/run_skill.py`
  - Main orchestrator.
  - Parses first, then dispatches into `to-data` or `to-code`.
  - Writes `effective_config.json` and `run_report.json`.
  - Uses the current Python interpreter and bundled scripts only; interpreter/script path overrides are not supported.

- `scripts/parse_document.py`
  - Parse-stage CLI entry.
  - Handles PDF or image inputs and normalizes outputs into the canonical schema.

- `scripts/transform_doc_to_data.py`
  - Downstream structured extraction entrypoint for `to-data`.

- `scripts/data_enrichment.py`
  - Heuristics and normalization for invoice classification, field extraction, table grouping, and structured summaries.

- `scripts/transform_doc_to_code.py`
  - Downstream generation entrypoint for `to-code`.
  - Supports `react`, `html-css`, `json-schema`, and `jupyter-notebook`.

- `scripts/render_result_report.py`
  - Generates `result_report.html`.
  - Renders layout, text, tables, JSON, and code/notebook previews depending on mode.

- `scripts/serve_skill_ui.py`
  - Optional local demo UI.
  - Lets a user choose a file, select `parse` / `to-data` / `to-code`, and inspect generated reports.
  - Restricts preview/run access to approved local content folders instead of arbitrary filesystem paths.

## Validation and support scripts

- `scripts/check_env.py`
  - Checks Python dependencies, OpenVINO runtime, and model asset discovery.

- `scripts/smoke_test.py`
  - Runs wrapper-level smoke validation.

- `scripts/utils.py`
  - Shared helpers for JSON I/O, artifact layout, parsing subprocess output, slug generation, and error handling.

## Notes

- Verified sample artifacts live under `artifacts/`.
- `test_inputs/openvino_notebook_architecture.png` is the current recommended `to-code` sample.
- `test_inputs/ov_invoice.png`, `test_inputs/invoice.pdf`, and related invoice fixtures are the current recommended `parse` / `to-data` samples.
