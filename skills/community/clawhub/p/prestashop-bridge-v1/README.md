# PrestaShop Bridge V1

PrestaShop Bridge V1 is a publishable skill pack and API contract for operating a PrestaShop 9 integration through a secure intermediary service built with Symfony 6.4 and API Platform 3.

Version: **1.0.3**

The Bridge provides a stable, explicit interface for AI agents and Python handlers. Reads are synchronous. Writes are asynchronous and tracked as durable jobs. Authentication, request signing, idempotency, replay protection, and rate limits are mandatory.

## Why this project exists

Direct integration against evolving native APIs is not enough for high-trust automation. Production automation needs:

- a stable contract
- strict authentication
- replay-resistant signed requests
- durable job status tracking
- idempotent write operations
- auditable behavior
- a clear policy boundary between native capabilities and exposed agent operations

PrestaShop Bridge V1 exists to provide that contract.

## Core design choices

- Symfony 6.4 for the Bridge runtime
- API Platform 3 for endpoint exposure
- OAuth2 Client Credentials with JWT RS256
- HMAC-SHA256 request signing
- Redis single node for Messenger transport and temporary HTTP idempotency cache
- MySQL as the source of truth for jobs, failed jobs, and business idempotency
- reads synchronous, writes asynchronous
- strict JSON schemas with `additionalProperties: false`
- structured JSON audit logs in rotating files
- `.env.bridge` for MVP secret management

## Exposed contract

### Synchronous reads
- `GET /v1/products/{id}`
- `GET /v1/orders/{id}`
- `GET /v1/jobs/{jobId}`

### Asynchronous writes
- `POST /v1/jobs/products/update`
- `POST /v1/jobs/products/import`
- `POST /v1/jobs/orders/status`

## Repository structure

- `SKILL.md`: operational skill instructions
- `_meta.json`: publication metadata
- `openapi.yaml`: machine-readable contract
- `examples.http`: end-to-end request examples
- `examples/`: split request and response samples
- `schemas/`: strict JSON Schemas
- `references/`: bridge policies and operational doctrine
- `docs/`: project-level documentation and packaging guidance
- `validators/`: lightweight local verification tools
- `evals/`: evaluation scenarios for regression checks

## How to verify this pack

1. Read `docs/quickstart.md`.
2. Configure variables from `.env.bridge.example`.
3. Check contract consistency in `openapi.yaml`.
4. Validate local examples with `validators/validate_examples.py`.
5. Review replay and idempotency rules in `references/idempotency-policy.md`.
6. Review trust boundaries in `docs/trust-and-safety.md`.

## Known MVP limits

- Redis is single node in MVP.
- Secrets are stored in `.env.bridge` and rotated manually.
- Elasticsearch and Vault are intentionally excluded from MVP.
- Job writes are at-least-once and rely on handler idempotency for safety.

## Publication readiness

This repository is ready to publish as a ClawHub/OpenClaw skill pack and to use as a development reference for the Symfony / PrestaShop implementation.

## License

See `LICENSE`.
