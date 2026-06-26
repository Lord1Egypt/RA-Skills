# Publishing Checklist

## Before publishing version 1.0.3
- [x] `SKILL.md` front matter matches `_meta.json`.
- [x] `openapi.yaml` version matches `1.0.3`.
- [x] All schemas are strict and include `additionalProperties: false`.
- [x] `POST /v1/jobs/orders/status` is used consistently.
- [x] `202 Accepted` is documented as job acceptance only.
- [x] MySQL is documented as the source of truth for jobs.
- [x] Example HMAC values are exact, not illustrative.
- [x] Local validator is included.
- [x] Quickstart and environment docs are included.
- [x] Trust and safety rules are explicit.

- [x] environment file is declared in `_meta.json`.
- [x] validator path is declared in `_meta.json`.
- [x] no placeholder HMAC values remain in `examples.http` or `examples/*.http`.
