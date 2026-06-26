---
name: ppt-task-orchestrator
description: "Production orchestration for pptx page task extraction and batch image delivery by reusing main-image-editor + psd-automator."
command-dispatch: tool
command-tool: ppt_task_orchestrator
command-arg-mode: raw
metadata:
  openclaw:
    userInvocable: true
    commandDispatch: tool
    commandTool: ppt_task_orchestrator
    commandArgMode: raw
---

# ppt-task-orchestrator

Orchestration layer for customer PPT workflows:

1. Parse `pptx` into per-page tasks (structured fields first).
2. Fallback to OCR for pages missing required fields.
3. Convert page tasks into `main-image-editor` batch tasks.
4. Execute with transaction rollback by reusing `main-image-editor` and `psd-automator`.
5. Aggregate delivery artifacts: result directory + `all-images.zip`.

## Usage

```bash
node skills/ppt-task-orchestrator/scripts/run-ppt-task-orchestrator.js \
  --request skills/ppt-task-orchestrator/examples/request.sample.json \
  --index ~/.openclaw/psd-index.json
```

Dry-run:

```bash
node skills/ppt-task-orchestrator/scripts/run-ppt-task-orchestrator.js \
  --request skills/ppt-task-orchestrator/examples/request.sample.json \
  --dry-run
```

## Request payload

`request` JSON supports:

- `pptPath`: absolute or `~/` path to `.pptx` file (required)
- `requestId`: optional tracking id
- `confidenceThreshold`: low-confidence gate threshold (default `0.8`)
- `fallbackPolicy`: `structured_only` or `structured_first_with_ocr` (default)
- `execution`: `dryRun`, `force`, `indexPath`, `bundleZip`
- `delivery`: `outputDir`, `zipName`, `copySelectedOnly`

## Failure policy

- Default policy is `rollback_all` inherited from `main-image-editor`.
- Any single PSD failure restores all touched PSD files from transaction backups.
- Delivery artifacts are produced only for success/dry-run outputs.
