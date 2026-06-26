# Quickstart

## 1. Configure environment
Copy values from `.env.bridge.example` into your deployment-specific `.env.bridge`.

## 2. Obtain a token
Send a `POST /oauth/token` request using HTTP Basic authentication and `grant_type=client_credentials`.

## 3. Perform a read
Call `GET /v1/products/123` with:
- Bearer token
- `X-Request-ID`
- `X-Timestamp`
- `X-Signature`

## 4. Create an async job
Call `POST /v1/jobs/products/update` with a valid request body and matching HMAC signature.

## 5. Poll the job
Use the returned `tracking_url` and read status from `GET /v1/jobs/{jobId}`.

## 6. Validate locally
Run:

```bash
python3 validators/validate_examples.py
```

The script checks required files, key endpoints, and example/schema coherence.
