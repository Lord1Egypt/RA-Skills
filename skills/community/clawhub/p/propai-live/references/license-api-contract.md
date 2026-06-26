# PropAI Live License API Contract

Use this contract to back `scripts/license-activate.mjs`, `scripts/license-guard.mjs`, and
`scripts/license-deactivate.mjs`.

## Base URL

- Production: `https://license.propaiclive.com`
- Development: `http://localhost:8787`

The client passes the base URL via `--api` or `PROPAI_LIVE_LICENSE_API_URL`.

## Authentication Model

- Activation: authenticate by `license key`.
- Validation/deactivation: authenticate by `licenseToken` returned by activation.
- Optional hardening: include HMAC request signatures for `validate` and `deactivate`.

## Endpoint: Activate

- `POST /v1/licenses/activate`

Request:

```json
{
  "key": "plive_xxxx",
  "product": "propai-live",
  "machineId": "mid_abc123",
  "clientVersion": "1.0.1",
  "runtime": "node-v25.8.0"
}
```

Success response:

```json
{
  "licenseId": "lic_123",
  "licenseToken": "ltok_123",
  "status": "active",
  "plan": "pro",
  "entitlements": ["read", "write", "social", "lead-storage"],
  "expiresAt": "2026-12-31T23:59:59Z",
  "offlineGraceHours": 72,
  "nextCheckHours": 6
}
```

Failure response:

```json
{
  "error": "license_not_found"
}
```

## Endpoint: Validate

- `POST /v1/licenses/validate`

Request:

```json
{
  "product": "propai-live",
  "machineId": "mid_abc123",
  "licenseToken": "ltok_123",
  "licenseId": "lic_123"
}
```

Success response:

```json
{
  "valid": true,
  "status": "active",
  "plan": "pro",
  "entitlements": ["read", "write", "social", "lead-storage"],
  "expiresAt": "2026-12-31T23:59:59Z",
  "offlineGraceHours": 72,
  "nextCheckHours": 6
}
```

Revoked/invalid response:

```json
{
  "valid": false,
  "status": "revoked",
  "error": "license_revoked"
}
```

## Endpoint: Deactivate

- `POST /v1/licenses/deactivate`

Request:

```json
{
  "product": "propai-live",
  "machineId": "mid_abc123",
  "licenseToken": "ltok_123",
  "licenseId": "lic_123"
}
```

Success response:

```json
{
  "ok": true
}
```

## Suggested Data Model

`licenses`
- `id` (pk)
- `license_key_hash` (unique)
- `product_slug`
- `plan`
- `status` (`active`, `trial`, `suspended`, `revoked`, `expired`)
- `seat_limit`
- `expires_at`
- `created_at`
- `updated_at`

`activations`
- `id` (pk)
- `license_id` (fk -> licenses.id)
- `machine_id`
- `machine_label`
- `last_seen_at`
- `revoked_at`

`entitlements`
- `id` (pk)
- `license_id` (fk -> licenses.id)
- `name` (for example `write`, `social`, `lead-storage`)

`license_audit_log`
- `id` (pk)
- `license_id`
- `event_type` (`activate`, `validate`, `deactivate`, `revoke`)
- `payload_json`
- `created_at`

## Enforcement Points

- Guard all write flows with `scripts/license-guard.mjs --mode write`.
- Guard feature-specific flows with entitlement checks:
  - lead persistence: `--require-entitlement lead-storage`
  - social publishing: `--require-entitlement social`

## Billing Integration

- Stripe/LemonSqueezy webhook -> create/update license records.
- On successful payment:
  - issue or extend license
  - set entitlements by plan
- On cancellation/refund:
  - mark `status = revoked` or `status = expired` depending on policy.

