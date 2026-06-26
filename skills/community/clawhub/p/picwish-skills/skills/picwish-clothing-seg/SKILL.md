---
name: picwish-clothing-seg
description: >-
  Segment clothing and body parts from fashion/person images into semantic masks (hair, face, clothes, shoes, etc.).
  Use when user needs clothing segmentation, fashion parsing, garment extraction, or body part masks.
  Input: image with person + optional segmentation mode/precision/class scope.
  Output: per-part mask image URLs (data.class_masks object), optional ZIP.
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

- Resolve image input (must contain person):
  - URL in message → `image_url` | path in message → `image_file` | file attachment → use temp path/URL from platform | none → ask user
  - See root skill "Image Input Resolution" for full priority
- Resolve context:
  ```bash
  node $OC_SCRIPT resolve
  ```
  - Script not found → check cwd for `openclaw.yaml` → determine mode; check `$VISUAL` dir → determine capabilities
- Resolve output directory:
  ```bash
  node $OC_SCRIPT route-output --skill picwish-clothing-seg --name tmp --ext tmp
  ```
  - Script not found → 3-level fallback:
    1. cwd has `openclaw.yaml` → `./output/`
    2. `$VISUAL` exists → `$VISUAL/output/picwish-clothing-seg/`
    3. None → `~/Downloads/`
  - `mkdir -p {output_dir}`

> Path aliases: `$VISUAL` = `{OPENCLAW_HOME}/workspace/visual/`, `$OC_SCRIPT` = `{OPENCLAW_HOME}/workspace/scripts/oc-workspace.mjs`

### 2. Build Parameters

- Required: `image_url` or `image_file` (from URL, path, or attachment — see root skill)
- class_type inference:
  - Clothing only → class_type=1 (default)
  - Clothing + shoes + bags → class_type=2
  - Body parts (hair/face) → class_type=3
  - Everything → class_type=4
- detail_mode: default 1 (normal); high precision → 2
- output_type: default 1 (merged grayscale mask); per-item → 2 (ZIP); both → 3
- quality: default 1 (normal); high precision → 2

### 3. Execute

```bash
node scripts/run_task.mjs --skill picwish-clothing-seg --input-json '{...}' --output-dir '{output_dir}'
```

### 4. Deliver

- ⚠️ Result field is data.class_masks (object, not single URL)
- Download each mask from class_masks
- Rename via workspace helper (repeat per saved file as needed):
  ```bash
  node $OC_SCRIPT rename --file {path} --name clothing-seg
  ```
  - Script not found → file already named `{output_dir}/{date}_{skill}.{ext}` by run_task.mjs
- If clothes_masks (ZIP) exists, download and save too
- Show all `saved_paths` and the **complete** mask URLs (do NOT strip query parameters — they contain auth tokens)
- Result URLs valid ~1 hour; local files are permanent
