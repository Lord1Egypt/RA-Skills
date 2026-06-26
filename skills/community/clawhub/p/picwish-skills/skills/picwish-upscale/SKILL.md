---
name: picwish-upscale
description: >-
  Enhance image resolution and sharpness (super-resolution). Supports general and face-specific enhancement.
  Use when user says image is blurry, low-res, wants to enlarge, sharpen, enhance, or upscale.
  Input: image (max 4096×4096, 20MB; 4x requires long edge ≤512, 2x requires ≤1024).
  Output: enhanced high-res image URL.
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
  node $OC_SCRIPT route-output --skill picwish-upscale --name tmp --ext tmp
  ```
  - Script not found → 3-level fallback:
    1. cwd has `openclaw.yaml` → `./output/`
    2. `$VISUAL` exists → `$VISUAL/output/picwish-upscale/`
    3. None → `~/Downloads/`
  - `mkdir -p {output_dir}`

> Path aliases: `$VISUAL` = `{OPENCLAW_HOME}/workspace/visual/`, `$OC_SCRIPT` = `{OPENCLAW_HOME}/workspace/scripts/oc-workspace.mjs`

### 2. Build Parameters

- Required: `image_url` or `image_file` (from URL, path, or attachment — see root skill)
- Infer type: mentions "face"/"portrait" → type=face; otherwise → type=clean
- scale_factor: user specifies → use (1/2/4); otherwise → leave empty (auto)
- ⚠️ If user specifies 4x but long edge >512, warn about limit

### 3. Execute

```bash
node scripts/run_task.mjs --skill picwish-upscale --input-json '{...}' --output-dir '{output_dir}'
```

### 4. Deliver

- Rename via workspace helper:
  ```bash
  node $OC_SCRIPT rename --file {path} --name upscale
  ```
  - Script not found → file already named `{output_dir}/{date}_{skill}.{ext}` by run_task.mjs
- Show `saved_path` as primary result; `result_url` as backup (valid ~1 hour)
- ⚠️ Always copy the **complete** `result_url` verbatim from script output — never strip query parameters (they contain required auth tokens)
