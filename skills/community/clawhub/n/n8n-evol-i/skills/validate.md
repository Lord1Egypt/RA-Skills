---
description: Structural REST validation for a template or generated JSON.
---

# validate

## When

Before any deploy. Catches structural breakage early.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/validate.py --workflow-key <key> [--env <env>] [--source built|template]
```

Default source is `built` if `--env` given, else `template`.

## Side effects

Prints a JSON report `{valid, source, path, errors}`. Exit 0 if valid, 1 otherwise.

Checks:

- top-level `nodes` (list) + `connections` (object keyed by node name)
- every node has `name` / `type` / `parameters`
- no `pinData` in templates
- no residual `{{@...}}` placeholders in built JSON
