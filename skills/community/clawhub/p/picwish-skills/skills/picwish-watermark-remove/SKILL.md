---
name: picwish-watermark-remove
description: >-
  Auto-detect and remove watermarks from images. No mask needed — AI auto-detects watermark regions.
  Use when user wants automatic watermark removal without manual marking.
  Input: image URL or file (jpg/png/bmp only, 20–10000px resolution, max 50MB).
  Output: watermark-free image URL (returned as data.file).
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
  - URL in message → `url` | path in message → `file` | file attachment → use temp path/URL from platform | none → ask user
  - ⚠️ This skill uses field names `url`/`file`, NOT `image_url`/`image_file`
  - See root skill "Image Input Resolution" for full priority
- ⚠️ Format restriction: jpg/png/bmp only, 20–10000px, max 50MB
- Resolve context:
  ```bash
  node $OC_SCRIPT resolve
  ```
  - Script not found → check cwd for `openclaw.yaml` → determine mode; check `$VISUAL` dir → determine capabilities
- Resolve output directory:
  ```bash
  node $OC_SCRIPT route-output --skill picwish-watermark-remove --name tmp --ext tmp
  ```
  - Script not found → 3-level fallback:
    1. cwd has `openclaw.yaml` → `./output/`
    2. `$VISUAL` exists → `$VISUAL/output/picwish-watermark-remove/`
    3. None → `~/Downloads/`
  - `mkdir -p {output_dir}`

> Path aliases: `$VISUAL` = `{OPENCLAW_HOME}/workspace/visual/`, `$OC_SCRIPT` = `{OPENCLAW_HOME}/workspace/scripts/oc-workspace.mjs`

### 2. Build Parameters

- ⚠️ Special field names: use `url` (not image_url) or `file` (not image_file) — resolved from URL, path, or attachment (see root skill)
- No mask needed — fully automatic watermark detection

### 3. Execute

```bash
node scripts/run_task.mjs --skill picwish-watermark-remove --input-json '{...}' --output-dir '{output_dir}'
```

### 4. Deliver

- ⚠️ Result field is data.file (not data.image)
- Rename via workspace helper:
  ```bash
  node $OC_SCRIPT rename --file {path} --name watermark-remove
  ```
  - Script not found → file already named `{output_dir}/{date}_{skill}.{ext}` by run_task.mjs
- Show `saved_path` as primary result; `result_url` as backup (valid ~1 hour)
- ⚠️ Always copy the **complete** `result_url` verbatim from script output — never strip query parameters (they contain required auth tokens)
