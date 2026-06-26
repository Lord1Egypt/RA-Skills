# Test Checklist

Use this checklist before treating the skill as publish-ready.

## Goal

Confirm that:

1. `run_skill.py` is the only required orchestration entrypoint.
2. `parse`, `to-data`, and `to-code` all work end to end.
3. Result reports are generated consistently.
4. Optional local UI works for interactive demos.
5. The skill metadata and folder structure are valid.

## Recommended sample files

- `test_inputs/ov_invoice.png`
  - Fast image sample for `parse`
- `test_inputs/invoice.pdf`
  - PDF sample for `to-data`
- `test_inputs/openvino_notebook_architecture.png`
  - Diagram sample for `to-code`

Avoid `test_inputs/signup_form.png` for release validation. It is only a placeholder fixture.

## 1. Validate skill metadata

```bash
python "C:/Users/intel/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .
```

Expected result:

- validation exits with code `0`
- `SKILL.md` frontmatter is accepted
- `agents/openai.yaml` is accepted

## 2. Environment check

Create and activate a virtual environment first when preparing a clean machine.

```bash
python scripts/check_env.py
```

Expected result:

- Python dependencies detected
- OpenVINO runtime detected
- PaddleOCR-VL OpenVINO package detected
- model directories discovered or clearly reported as missing

## 3. Parse mode

```bash
python scripts/run_skill.py \
  --mode parse \
  --file ./test_inputs/ov_invoice.png \
  --out ./artifacts/release_parse_test
```

Expected files:

- `artifacts/release_parse_test/effective_config.json`
- `artifacts/release_parse_test/run_report.json`
- `artifacts/release_parse_test/parsed.json`
- `artifacts/release_parse_test/parsed.md`
- `artifacts/release_parse_test/result_report.html`

Inspect:

- `parsed.json` contains pages and blocks
- `parsed.md` is readable
- `result_report.html` opens locally
- if the document is sensitive, verify the output location is a private local folder

## 4. To-data mode

```bash
python scripts/run_skill.py \
  --mode to-data \
  --file ./test_inputs/invoice.pdf \
  --out ./artifacts/release_todata_test \
  --extract tables,entities,kv_pairs
```

Expected files:

- `artifacts/release_todata_test/result_report.html`
- `artifacts/release_todata_test/task_output/normalized.json`
- `artifacts/release_todata_test/task_output/traceability.json`
- one or more of:
  - `entities.json`
  - `kv_pairs.json`
  - `table_index.json`
  - `structured_record.json`

Inspect:

- document classification exists in normalized output
- invoice-like inputs produce invoice-oriented fields
- report shows layout, text, structured output, and table view when tables exist
- review persisted artifacts before sharing them outside the machine

## 5. To-code mode

```bash
python scripts/run_skill.py \
  --mode to-code \
  --file ./test_inputs/openvino_notebook_architecture.png \
  --out ./artifacts/release_tocode_test \
  --target jupyter-notebook \
  --title "OpenVINO Notebook"
```

Expected files:

- `artifacts/release_tocode_test/result_report.html`
- `artifacts/release_tocode_test/code_preview.html`
- `artifacts/release_tocode_test/task_output/notebook.ipynb`
- `artifacts/release_tocode_test/task_output/notebook_plan.json`
- `artifacts/release_tocode_test/task_output/traceability.json`

Inspect:

- notebook file opens in Jupyter
- `result_report.html` shows source, parse, generated app/code, and JSON views
- `code_preview.html` renders notebook cells in a browser-friendly way
- review generated code and notebook cells before running them

## 6. Config-file flow

```bash
python scripts/run_skill.py --config-file ./configs/parse_test.json
python scripts/run_skill.py --config-file ./configs/to_data_test.json
python scripts/run_skill.py --config-file ./configs/to_code_notebook_test.json
```

Expected result:

- each manifest resolves correctly
- artifact folder matches config file output path

## 7. Local UI flow

Start the UI:

```bash
python scripts/serve_skill_ui.py
```

Open:

```text
http://127.0.0.1:8765
```

Check:

- file preview works for images and PDFs
- mode picker shows `parse`, `to-data`, and `to-code`
- `to-code` exposes target selection
- successful runs load `result_report.html` in the embedded viewer
- `Open Code Preview` is enabled only for `to-code` runs that generated `code_preview.html`
- files outside the approved local content folders are rejected by the UI

## 8. Failure behavior

Missing input:

```bash
python scripts/run_skill.py --mode parse --file ./test_inputs/does_not_exist.pdf
```

Expected result:

- non-zero exit code
- stderr contains JSON with `"ok": false`
- fallback error artifact contains `error.json`

## 9. Publish readiness

Treat the skill as ready for ClawHub-style publishing when all of these are true:

- `quick_validate.py` passes
- core sample runs pass for `parse`, `to-data`, and `to-code`
- `result_report.html` renders for all modes
- `code_preview.html` renders for `to-code`
- `agents/openai.yaml` exists and matches the skill purpose
- `SKILL.md` examples match the actual supported targets and scripts
