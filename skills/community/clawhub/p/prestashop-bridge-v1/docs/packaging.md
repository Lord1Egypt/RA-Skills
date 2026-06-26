# Packaging

A publishable PrestaShop Bridge skill pack must include at minimum:
- `SKILL.md`
- `_meta.json`
- `README.md`

A production-grade publishable pack should include:
- `openapi.yaml`
- `examples.http`
- `examples/`
- `references/`
- `schemas/`
- `validators/`
- `evals/`

## Packaging rules
1. Endpoints must match exactly across all files.
2. Headers must match exactly across all files.
3. OAuth and HMAC rules must match exactly across all files.
4. JSON schemas must use `additionalProperties: false`.
5. `202 Accepted` must always be described as job acceptance only.
6. MySQL must always be documented as the source of truth for job status.
