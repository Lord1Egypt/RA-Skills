---
description: Health check — workspace tree, env YAMLs, templates, n8n API reachability.
---

# doctor

## When

Anything goes wrong, or before an important deploy.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/doctor.py [--env <name>] [--with-audit] [--audit-only]
```

## Side effects

Prints a 3-state (✓/⚠/✗) report:

- workspace tree presence
- per-env YAML parses + workflow-IDs not placeholder
- per-env n8n API reachable
- every `*.template.json` parses
- (only with `--with-audit`) per-env `POST /api/v1/audit` — one row per non-empty risk category (credentials / database / nodes / filesystem / instance), each WARN with the finding count. 404 from older n8n instances → graceful WARN row.

`--audit-only` skips workspace / env / template checks and runs only the audit phase. Implies `--with-audit`.

Audit is OFF by default because it can be slow on large instances (per R-10).

Exit 0 unless any `✗ fail` row.

## See also

- [`skills/patterns/agent-api-discipline.md`](patterns/agent-api-discipline.md) — verify `POST /audit` body and category-section shape via Context7 before relying on training-data recall (especially when `--with-audit` enabled).
