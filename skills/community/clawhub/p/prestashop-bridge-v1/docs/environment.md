# Environment Guide

## Minimum required variables
- `APP_ENV`
- `BRIDGE_BASE_URL`
- `OAUTH_CLIENT_ID`
- `OAUTH_CLIENT_SECRET`
- `OAUTH_TOKEN_TTL`
- `JWT_PRIVATE_KEY_PATH`
- `JWT_PUBLIC_KEY_PATH`
- `HMAC_SECRET_CURRENT`
- `HMAC_SECRET_PREVIOUS`
- `REDIS_DSN`
- `DATABASE_URL`
- `RATE_LIMIT_READ`
- `RATE_LIMIT_WRITE`
- `JOB_MAX_ATTEMPTS`
- `JOB_TIMEOUT_SECONDS`
- `IDEMPOTENCY_HTTP_TTL_SECONDS`
- `IDEMPOTENCY_DB_RETENTION_DAYS`
- `FAILED_JOB_RETENTION_DAYS`
- `GZIP_RECOMMENDED_ABOVE_BYTES`
- `GZIP_REQUIRED_ABOVE_BYTES`
- `MAX_PAYLOAD_BYTES`
- `ALLOWED_SOURCE_IPS`
- `LOG_PATH`

## File permissions
- `.env.bridge`: `chmod 600`
- `private.pem`: `chmod 600`
- `public.pem`: readable by the bridge runtime

## Production MVP expectations
- Redis reachable on low-latency private network
- MySQL persistent and backed up
- NTP synchronized on all nodes
- firewall allowlist configured
- TLS terminated before the application or at the reverse proxy

## Validation notes
- The package metadata explicitly declares `.env.bridge.example` as the environment contract.
- The local validator checks the presence of the environment file and the exact HMAC examples.
- Update `BRIDGE_BASE_URL` only if the deployment URL changes. Updating the base URL does not change the signed path examples because HMAC uses the path and query string only.
