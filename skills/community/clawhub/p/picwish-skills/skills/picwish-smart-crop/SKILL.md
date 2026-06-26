---
name: picwish-smart-crop
description: >-
  Auto-correct perspective and crop document or object images. Supports correction-only, enhancement, or both.
  Use when user has tilted document photo, wants to straighten/crop scanned doc, correct perspective, or extract object.
  Input: image URL or file + optional correction type.
  Output: corrected/cropped image URL.
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

- Resolve image input (document or object image):
  - URL in message → `image_url` | path in message → `image_file` | file attachment → use temp path/URL from platform | none → ask user
  - See root skill "Image Input Resolution" for full priority
- Resolve context:
  ```bash
  node $OC_SCRIPT resolve
  ```
  - Script not found → check cwd for `openclaw.yaml` → determine mode; check `$VISUAL` dir → determine capabilities
- Resolve output directory:
  ```bash
  node $OC_SCRIPT route-output --skill picwish-smart-crop --name tmp --ext tmp
  ```
  - Script not found → 3-level fallback:
    1. cwd has `openclaw.yaml` → `./output/`
    2. `$VISUAL` exists → `$VISUAL/output/picwish-smart-crop/`
    3. None → `~/Downloads/`
  - `mkdir -p {output_dir}`

> Path aliases: `$VISUAL` = `{OPENCLAW_HOME}/workspace/visual/`, `$OC_SCRIPT` = `{OPENCLAW_HOME}/workspace/scripts/oc-workspace.mjs`

### 2. Build Parameters

- Required: `image_url` or `image_file` (from URL, path, or attachment — see root skill)
- type inference:
  - "document correction" → type=0
  - "document enhance" / "clearer" → type=1
  - "document correction + enhance" → type=2
  - "object correction" → type=3
  - "object correction + remove background" → type=4
  - Not specified → leave empty (document correction)

### 3. Execute

```bash
node scripts/run_task.mjs --skill picwish-smart-crop --input-json '{...}' --output-dir '{output_dir}'
```

### 4. Deliver

- Rename via workspace helper:
  ```bash
  node $OC_SCRIPT rename --file {path} --name smart-crop
  ```
  - Script not found → file already named `{output_dir}/{date}_{skill}.{ext}` by run_task.mjs
- Show `saved_path` as primary result; `result_url` as backup (valid ~1 hour)
- ⚠️ Always copy the **complete** `result_url` verbatim from script output — never strip query parameters (they contain required auth tokens)
