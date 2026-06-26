---
name: local-document-ai-openvino
description: Private document AI for Intel hardware. Parse PDFs, invoices, screenshots, and diagrams locally with MinerU 2.5 on OpenVINO GenAI, then turn them into structured data or executable notebook/code scaffolds. Supports custom key-field extraction for invoice demos, with clear quick-start commands and example prompts.
---

# Private Document AI with OpenVINO

Turn local PDFs, invoices, screenshots, and diagrams into one of two useful outcomes:

1. `to-data`: classify the document and extract structured fields, tables, and JSON, including user-requested key fields.
2. `to-code`: turn screenshots, forms, and architecture diagrams into code or Jupyter notebook scaffolds.

Everything runs locally and is built for Intel CPU/GPU acceleration with OpenVINO GenAI.

The default runtime path in this release is:

- MinerU 2.5 Pro
- preconverted OpenVINO INT4 model bundle
- local PDF rendering with `pypdfium2`
- no local model export step

## Why install this skill

Install this when you want one local workflow for:

- invoice and receipt extraction
- private PDF understanding
- table and key-value extraction
- architecture diagram to notebook generation
- screenshot to HTML/React scaffold generation

This skill is especially good for demos because it already includes:

- medical invoice `to-data` flows
- restaurant invoice `to-data` flows
- custom invoice field extraction such as invoice number, date, seller, and amount due
- architecture diagram `to-code -> jupyter-notebook` flows
- local HTML reports for easy review and screenshots

## 30-second start

Check the environment:

```bash
python "{baseDir}/scripts/check_env.py"
```

Or run directly from the CLI:

```bash
python "{baseDir}/scripts/run_skill.py" --mode to-data --file "/absolute/path/to/invoice.pdf" --out "/absolute/path/to/artifacts/invoice_data" --extract "tables,entities,kv_pairs"
```

For invoice demos with custom key fields:

```bash
python "{baseDir}/scripts/run_skill.py" --mode to-data --file "/absolute/path/to/invoice.pdf" --out "/absolute/path/to/artifacts/invoice_data" --extract "tables,entities,kv_pairs" --fields "invoice_number,invoice_date,total_amount,vendor_name"
```

## Example prompts

Use prompts like these in OpenClaw:

```text
Use $local-document-ai-openvino to parse this local PDF and give me a structured report.
```

```text
Use $local-document-ai-openvino to extract invoice fields, tables, and key-value pairs from this medical invoice.
```

```text
Use $local-document-ai-openvino to classify this receipt and return normalized JSON.
```

```text
Use $local-document-ai-openvino to extract only these invoice fields from this file: invoice_number, invoice_date, total_amount, vendor_name. Return a structured JSON result with just those requested fields.
```

```text
Use $local-document-ai-openvino to extract these custom fields from this invoice: buyer_tax_id, seller_tax_id, amount_due, check_code. Save the full parse artifacts, but highlight the requested fields in the final structured output.
```

```text
Use $local-document-ai-openvino to turn this architecture diagram into a Jupyter notebook scaffold.
```

```text
Use $local-document-ai-openvino to convert this UI screenshot into an HTML scaffold.
```

## What you get

Typical outputs include:

- `parsed.json`
- `parsed.md`
- `result_report.html`
- `task_output/structured_record.json`
- `task_output/normalized.json`
- `task_output/requested_fields.json`
- `task_output/requested_fields_record.json`
- `task_output/notebook.ipynb`
- `code_preview.html`

## Best demo paths

If you are evaluating the skill for the first time, start here:

1. `to-data` on an invoice PDF
2. review `result_report.html`
3. inspect `structured_record.json`
4. rerun with `--fields` and inspect `requested_fields_record.json`
5. then try `to-code` with a diagram image and target `jupyter-notebook`

## Custom key-field extraction

After the skill is installed, users can ask for a custom field list at call time.
This is the recommended pattern for invoice demos.

Use the `fields` parameter with `to-data`:

- CLI: `--fields "invoice_number,invoice_date,total_amount,vendor_name"`
- config JSON: `"fields": "invoice_number,invoice_date,total_amount,vendor_name"`
- slash-command style: `fields=invoice_number,invoice_date,total_amount,vendor_name`

The skill will:

1. parse the full document locally with MinerU on OpenVINO
2. keep the standard `kv_pairs`, `entities`, `tables`, and traceability artifacts
3. resolve the requested field names to canonical keys when possible
4. write a focused structured output for only those requested fields

The two demo-friendly outputs are:

- `task_output/requested_fields.json`
  This includes each requested field, the matched canonical key, whether it was found, the primary match, and all matches.
- `task_output/requested_fields_record.json`
  This is the compact final record keyed by the user-requested field names.

Recommended invoice demo field names:

- `invoice_number`
- `invoice_code`
- `check_code`
- `invoice_date`
- `buyer_tax_id`
- `seller_tax_id`
- `vendor_name`
- `customer_name`
- `subtotal`
- `tax_amount`
- `total_amount`
- `amount_due`

Common aliases are also supported when they can be normalized to canonical keys, for example:

- `seller`
- `buyer`
- `invoice no`
- `invoice date`
- `total`
- `amount due`

## Core pipeline

Use this skill as a local document-to-action pipeline:

1. Parse the document into a canonical structured representation.
2. Optionally continue into `to-data` or `to-code`.
3. Save outputs into a predictable artifact folder with traceability.

## Read only if needed

Load these references when you need the schema or output contracts:

- `{baseDir}/references/schema.md`
- `{baseDir}/references/mode_guide.md`
- `{baseDir}/references/output_contracts.md`

## Primary entrypoint

Use this published entrypoint:

- CLI orchestrator: `{baseDir}/scripts/run_skill.py`

Do not call these implementation scripts directly from the skill:

- `parse_document.py`
- `transform_doc_to_data.py`
- `transform_doc_to_code.py`

## Local readiness

Check the environment before processing real documents:

```bash
python "{baseDir}/scripts/check_env.py"
```

For workshops, the simplest setup is installing into a skill-local `.vendor` directory.
The entry scripts auto-detect it, so you do not need to edit `PYTHONPATH`:

```bash
python "{baseDir}/scripts/install_local_runtime.py"
```

If you prefer, a normal virtual environment also works:

```bash
python -m pip install -r "{baseDir}/requirements.txt"
```

Download the preconverted MinerU OpenVINO model bundle into the skill-local `models/` folder, or point the skill at it with an environment variable:

```bash
set MINERU_OPENVINO_MODEL_DIR=C:\absolute\path\to\MinerU2.5-Pro-2604-1.2B-int4-ov
```

Recommended model bundle:

- `https://www.modelscope.cn/models/snake7gun/MinerU2.5-Pro-2604-1.2B-int4-ov`

Workshop-friendly download example:

```bash
git clone --depth 1 https://www.modelscope.cn/snake7gun/MinerU2.5-Pro-2604-1.2B-int4-ov.git "{baseDir}/models/MinerU2.5-Pro-2604-1.2B-int4-ov"
```

Run a quick orchestration smoke test:

```bash
python "{baseDir}/scripts/smoke_test.py"
```

Model assets are discovered from:

- `MINERU_OPENVINO_MODEL_DIR`
- `MINERU_MODEL_DIR`
- `{baseDir}/models/MinerU2.5-Pro-2604-1.2B-int4-ov/`
- `{baseDir}/models/mineru2.5-int4-ov/`

Prefer using a predownloaded model bundle for workshops. This skill does not require local export or automatic model download.

## Supported modes

### `parse`

Use when the user wants the structured parse only.

Outputs:

- `parsed.json`
- `parsed.md`
- `result_report.html`
- extracted layout, tables, or figures when available

### `to-data`

Use when the user wants structured extraction, normalization, or document classification.

Typical outputs under `task_output/`:

- `entities.json`
- `kv_pairs.json`
- `table_index.json`
- `normalized.json`
- `structured_record.json`
- `requested_fields.json`
- `requested_fields_record.json`
- `traceability.json`

### `to-code`

Use when the user wants implementation-oriented output from the parse result.

Supported targets:

- `react`
- `html-css`
- `json-schema`
- `jupyter-notebook`

Typical outputs under `task_output/`:

- `component_map.json`
- `field_schema.json`
- `ui_blueprint.json`
- `notes.md`
- `traceability.json`
- target-specific artifacts such as `app.jsx`, `index.html`, `styles.css`, `schema.json`, `notebook.ipynb`, or `notebook_plan.json`

Treat all generated code and notebooks as drafts. Review them before running, publishing, or connecting them to real systems.

## Published package scope

The published ClawHub bundle is intentionally CLI-first.

- main workflow: `scripts/run_skill.py`
- diagnostics: `scripts/check_env.py`
- smoke verification: `scripts/smoke_test.py`

Developer-only local UI helpers are kept out of the public release bundle.

## Pipeline rules

Always follow these rules:

1. Prefer local execution.
2. Always parse first into `parsed.json`.
3. Generate downstream artifacts from `parsed.json`, not raw OCR text alone.
4. Preserve page numbers, reading order, block types, and source anchors when possible.
5. Write traceability for downstream outputs.
6. Mark low-confidence regions or assumptions explicitly.
7. Do not silently drop tables, figures, formulas, charts, or key-value regions.
8. Save outputs into one artifact folder per run.
9. For confidential documents, prefer an explicit private `--out` directory and remove artifacts after review.

## Output contract

Default output folder:

`./artifacts/<document_stem>/`

Expected top-level outputs:

- `effective_config.json`
- `run_report.json`
- `parsed.json`
- `parsed.md`
- `result_report.html`
- `task_output/`

`to-code` runs may also emit:

- `code_preview.html`

## CLI examples

### Parse

```bash
python "{baseDir}/scripts/run_skill.py" \
  --mode parse \
  --file "/absolute/path/to/report.pdf" \
  --out "/absolute/path/to/artifacts/report_parse"
```

### To-data

```bash
python "{baseDir}/scripts/run_skill.py" \
  --mode to-data \
  --file "/absolute/path/to/invoice.pdf" \
  --out "/absolute/path/to/artifacts/invoice_data" \
  --extract "tables,entities,kv_pairs"
```

### To-data with custom fields

```bash
python "{baseDir}/scripts/run_skill.py" \
  --mode to-data \
  --file "/absolute/path/to/invoice.pdf" \
  --out "/absolute/path/to/artifacts/invoice_data" \
  --extract "tables,entities,kv_pairs" \
  --fields "invoice_number,invoice_date,total_amount,vendor_name"
```

### To-code

```bash
python "{baseDir}/scripts/run_skill.py" \
  --mode to-code \
  --file "/absolute/path/to/ui_mockup.png" \
  --out "/absolute/path/to/artifacts/ui_code" \
  --target "react" \
  --title "Generated App"
```

### To-code notebook target

```bash
python "{baseDir}/scripts/run_skill.py" \
  --mode to-code \
  --file "/absolute/path/to/architecture_diagram.png" \
  --out "/absolute/path/to/artifacts/notebook_code" \
  --target "jupyter-notebook" \
  --title "OpenVINO Notebook"
```

## Slash-command examples

```text
/skill local-document-ai-openvino parse file=./docs/report.pdf
```

```text
/skill local-document-ai-openvino to-data file=./docs/invoice.pdf extract=tables,entities,kv_pairs
```

```text
/skill local-document-ai-openvino to-data file=./docs/invoice.pdf extract=tables,entities,kv_pairs fields=invoice_number,invoice_date,total_amount,vendor_name
```

```text
/skill local-document-ai-openvino to-code file=./mockups/architecture.png target=jupyter-notebook
```

## Optional local demo UI

Start the local UI when the user wants an interactive demo page:

```bash
python "{baseDir}/scripts/serve_skill_ui.py"
```

The UI lets the user:

- preview a local file
- choose `parse`, `to-data`, or `to-code`
- choose the `to-code` target
- run the pipeline and inspect the generated local HTML reports

The bundled UI only allows preview/run access for local files under the skill directory and common user content folders such as Downloads, Documents, Desktop, and Pictures.

## Failure behavior

If a run fails:

- state which stage failed
- do not claim outputs were created if they were not
- prefer writing `error.json` with failure details
- recommend `parse` first when the downstream request is ambiguous
- surface stderr or a concise failure summary when available

## Safety notes

- Use a virtual environment for dependency installation.
- Review and approve model downloads only when you explicitly intend to.
- Keep outputs in a private local folder when documents are sensitive.
- Review generated code and notebooks before execution.
- Delete artifacts when they are no longer needed.
- The wrapper always uses the bundled local scripts and the current Python interpreter. It does not allow custom interpreter or script-directory overrides.

## Short reminder

Present this skill as a local document-understanding workflow with downstream actions and customizable field extraction, not as a plain OCR wrapper.
