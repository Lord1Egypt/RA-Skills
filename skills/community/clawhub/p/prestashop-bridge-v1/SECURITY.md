# Security Policy

## Model
This pack documents a Bridge that secures machine-to-machine communication for PrestaShop 9.

## Required controls
- OAuth2 Client Credentials
- JWT RS256 only
- HMAC-SHA256 on every protected request
- timestamp validation within ±30 seconds
- replay detection through request idempotency and short-lived signature observation
- rate limits by token
- firewall IP allowlist
- structured JSON audit logs
- MySQL as job status authority

## Secret handling
Secrets are loaded from `.env.bridge` in MVP. They must never be committed to source control.

## Rotation
- HMAC secrets: support current and previous values during controlled rotation
- JWT keys: rotate manually with deployment coordination


## Environment contract

The canonical deployment variables are defined in `.env.bridge.example` and summarized in `docs/environment.md`. These variables are also declared in `_meta.json` so a reviewer can identify the required runtime inputs without unpacking the whole repository manually.

## Exact verification material

- `examples.http` contains exact HMAC signatures for the documented sample requests.
- `validators/validate_examples.py` recomputes those signatures and fails if any example drifts.
- `schemas/examples/` contains one valid example payload for every main schema.
