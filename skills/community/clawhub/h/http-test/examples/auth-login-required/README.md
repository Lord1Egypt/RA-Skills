# Auth Login Required Example

Use this example to verify that protected endpoints reject missing or invalid authentication.

## Best Fit

- profile endpoints
- admin-only endpoints
- any endpoint expected to force login

## Required Variables

- `HOST`
- `AUTH_TOKEN` for the invalid-token branch if needed

## Run

```bash
bash -n './auth-login-required.api-verify.sh'
HOST='https://api.example.test' AUTH_TOKEN='intentionally-invalid-token' bash './auth-login-required.api-verify.sh'
```

## What To Check

- whether unauthenticated access returns the expected status or marker
- whether invalid credentials fail differently from missing credentials
