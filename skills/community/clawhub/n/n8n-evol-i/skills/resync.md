---
description: Pull live state of one workflow back into its template.
---

# resync

## When

After someone edits a workflow in the n8n UI and you want the template to reflect those changes.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/resync.py --env <env> --workflow-key <key>
```

## Side effects

- `GET /api/v1/workflows/<id>` from env's n8n.
- Runs the dehydrate pipeline:
  - Strips volatile metadata (id, active, versionId, createdAt, updatedAt, tags, pinData).
  - Restores UUID placeholders by node-name lookup against the existing template.
  - Reverse-substitutes env values back into `{{@env:...}}` placeholders.
  - Restores JS / Python code blocks by collapsing the round-trip markers (`#:js:` / `MATCH:js:` for JS, `MATCH:py:` for Python; legacy `DEHYDRATE` markers also accepted on read for rollforward).
- Writes `<workspace>/n8n-workflows-template/<key>.template.json`.
