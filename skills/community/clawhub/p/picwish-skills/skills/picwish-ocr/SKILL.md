---
name: picwish-ocr
description: >-
  Extract text from images using OCR. Supports output as txt, pdf, docx, xlsx, or pptx.
  Use when user wants to recognize text, extract text from screenshot/document/receipt, or perform OCR.
  Input: image + output format (txt/pdf/docx/xlsx/pptx).
  Output: OCR result file URL (returned as data.file, poll timeout 120s).
  Requires env PICWISH_API_KEY or openclaw config skills.entries.picwish.apiKey.
  China mainland users set PICWISH_REGION=cn via env or openclaw config.
requirements:
  credentials:
    - name: PICWISH_API_KEY
      source: env | openclaw-config:skills.entries.picwish.apiKey
    - name: PICWISH_REGION
      source: env | openclaw-config:skills.entries.picwish.region
      required: false
      default: global
  permissions:
    - type: file_read
      paths:
        - ~/.openclaw/config.json
        - ~/.openclaw/workspace/scripts/
        - ~/.openclaw/workspace/visual/
        - ./
    - type: file_write
      paths:
        - ~/.openclaw/workspace/visual/output/
        - ./output/
    - type: exec
      commands:
        - node
---

## Workflow

### 1. Preflight

- Resolve image input:
  - URL in message → `image_url` | path in message → `image_file` | file attachment → use temp path/URL from platform | none → ask user
  - See root skill "Image Input Resolution" for full priority
- Resolve context:
  ```bash
  node $OC_SCRIPT resolve
  ```
  - Script not found → check cwd for `openclaw.yaml` → determine mode; check `$VISUAL` dir → determine capabilities
- Resolve output directory:
  ```bash
  node $OC_SCRIPT route-output --skill picwish-ocr --name tmp --ext tmp
  ```
  - Script not found → 3-level fallback:
    1. cwd has `openclaw.yaml` → `./output/`
    2. `$VISUAL` exists → `$VISUAL/output/picwish-ocr/`
    3. None → `~/Downloads/`
  - `mkdir -p {output_dir}`

> Path aliases: `$VISUAL` = `{OPENCLAW_HOME}/workspace/visual/`, `$OC_SCRIPT` = `{OPENCLAW_HOME}/workspace/scripts/oc-workspace.mjs`

### 2. Build Parameters

- Required: `image_url` or `image_file` (from URL, path, or attachment — see root skill)
- Required: format — output format
  - Plain text → format=txt
  - Editable document → format=docx
  - Spreadsheet → format=xlsx
  - Presentation → format=pptx
  - PDF → format=pdf
  - Not specified → default txt
- language: optional (comma-separated, max 10)
  - Default: ChinesePRC,English,Digits
- password: optional (max 32 chars, for encrypted files)

### 3. Execute

```bash
node scripts/run_task.mjs --skill picwish-ocr --input-json '{...}' --output-dir '{output_dir}'
```

⚠️ Poll timeout set to 120 seconds (OCR takes longer)

### 4. Deliver

- ⚠️ Result field is data.file (not data.image)
- Rename via workspace helper:
  ```bash
  node $OC_SCRIPT rename --file {path} --name ocr
  ```
  - Script not found → file already named `{output_dir}/{date}_{skill}.{ext}` by run_task.mjs
- Show `saved_path` as primary result; `result_url` as backup (valid ~1 hour)
- ⚠️ Always copy the **complete** `result_url` verbatim from script output — never strip query parameters (they contain required auth tokens)
- If format=txt → can also show recognized text directly
