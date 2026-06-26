---
name: dehydrate-workflow
description: Convert a raw exported workflow JSON into a template.
user-invocable: false
---

# dehydrate-workflow

## When

A user pastes a raw workflow JSON they exported from another instance, and wants it as a template.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/dehydrate.py --env <env> --input <path-to-raw.json> --output-key <key>
```

Like `resync` but with arbitrary input rather than fetched from the env.

## Side effects

Runs the same dehydrate pipeline as `resync` and writes `<workspace>/n8n-workflows-template/<key>.template.json`.
