# Config Reference (env-first)

## Bridge

- `BRIDGE_SHARED_SECRET`: bearer auth secret for sidecar/admin routes.
- `AUTH_WINDOW_SEC`: timestamp drift window for `x-bridge-ts` (also used for optional nonce replay window).
- `SQLITE_PATH`: sqlite database path.
- `SWEEP_INTERVAL_SEC`: interval for expired watch sweep.
- `STALE_CLAIM_SEC`: age threshold to requeue stale claimed outbound commands.
- `DEDUPE_RETENTION_HOURS`: retention window for dedupe keys.
- `JOB_RETENTION_HOURS`: retention window for completed/failed operational rows.
- `SIDECAR_STALE_SEC`: threshold to mark sidecar heartbeat as stale.

## WeChat parser/trigger

- `ALLOW_GROUPS`: comma-separated group ids/names.
- `TRIGGER_PREFIXES`: comma-separated prefixes (default includes `/mail`, `查邮箱`, `/watch`, `/mail-watch`, `监控`).
- `PASSIVE_SINGLE_EMAIL_MODE`: allow passive one-email triggers.
- `DEFAULT_WAIT_TIMEOUT_SEC`: fallback timeout for watch mode.

## Mail backend

- `MAIL_BACKEND`: `mock` or `bhmailer-http`.
- `MAIL_QUERY_MODE`: `direct-api` or `push-webhook`.
- `MAIL_PREFER_PUSH_WEBHOOK`: if true, `/watch` creates subscription + waits for webhook.
- `BHMAILER_API_BASE`
- `BHMAILER_UID`
- `BHMAILER_SIGN`
- `BHMAILER_WEBHOOK_SECRET`
- `BHMAILER_DEFAULT_TIMEOUT_SEC`
- `BHMAILER_EXTRACTION_PROFILE`: `default`, `otp`, `full-preview`, or custom provider-side shape.

## Reply format

- `REPLY_MAX_BODY_PREVIEW_CHARS`
- `REPLY_INCLUDE_SUBJECT`
- `REPLY_INCLUDE_FROM`
- `REPLY_INCLUDE_RECEIVED_AT`
