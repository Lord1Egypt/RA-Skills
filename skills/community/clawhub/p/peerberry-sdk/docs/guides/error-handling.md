# Error Handling

`peerberry_sdk` raises structured exceptions with context to support predictable production handling.

## Exception Hierarchy

All SDK exceptions derive from:

- `PeerberryException`

Main subclasses:

- `PeerberryAPIError`
  - `AuthenticationError`
    - `InvalidCredentials`
    - `TokenRefreshError`
  - `AuthorizationError`
  - `RateLimitError`
  - `ValidationError`
    - `InsufficientFunds`
  - `ServerError`
- `NetworkError`
- `InvalidPeriodicity`
- `InvalidSort`
- `InvalidType`

## Exception Context Fields

Most runtime exceptions include rich metadata:

| Field | Meaning |
| --- | --- |
| `status_code` | HTTP status from API response, when available |
| `error_code` | API-specific error code if present |
| `errors` | Parsed API `errors` payload |
| `payload` | Parsed API response payload |
| `url` | Request URL |
| `method` | HTTP method |
| `retry_after` | Parsed `Retry-After` seconds, if present |
| `is_retryable` | SDK hint based on retry policy/status |
| `request_id` | SDK-generated request correlation ID |
| `original_exception` | Underlying exception, when wrapping |

## Typical Failure Classes

## Network Failures

Raised as `NetworkError` when transport fails and retries are exhausted.

```python
from peerberry_sdk import NetworkError

try:
    api.get_overview()
except NetworkError as exc:
    print(exc.request_id, exc.is_retryable)
```

## Rate Limiting (`429`)

Raised as `RateLimitError`.

`retry_after` is populated when response includes a valid `Retry-After` header.

```python
from peerberry_sdk import RateLimitError

try:
    api.get_loans(quantity=10)
except RateLimitError as exc:
    wait_seconds = exc.retry_after or 5
    print("retry in", wait_seconds)
```

## Authentication Failures (`401`)

Raised as `AuthenticationError` (or `InvalidCredentials` for login-specific flows).

If auto-refresh is enabled, SDK may attempt token refresh first.

## Token Refresh Failures

Raised as `TokenRefreshError` when:

- refresh token is missing
- refresh request fails
- refresh response lacks `access_token`

## Validation Failures (`4xx`)

Raised as `ValidationError` for general client-side request problems.

Domain-specific local validation may also raise:

- `InvalidPeriodicity`
- `InvalidSort`
- `InvalidType`
- `ValueError` / `TypeError` for invalid argument shapes

## Server Failures (`5xx`)

Raised as `ServerError` after configured retries are exhausted.

## Recommended Catch Pattern

```python
from peerberry_sdk import (
    PeerberryException,
    RateLimitError,
    ValidationError,
    TokenRefreshError,
    NetworkError,
    ServerError,
)

try:
    result = api.get_transactions(quantity=50)
except RateLimitError as exc:
    # sleep + retry strategy
    raise
except ValidationError as exc:
    # fix caller inputs
    raise
except TokenRefreshError as exc:
    # trigger re-authentication path
    raise
except (NetworkError, ServerError) as exc:
    # transient upstream issue path
    raise
except PeerberryException as exc:
    # SDK fallback boundary
    raise
```

## Operational Logging Pattern

Use `request_id` for log correlation:

```python
try:
    api.get_overview()
except Exception as exc:
    request_id = getattr(exc, "request_id", None)
    print("request_id=", request_id, "error=", exc)
```

## Observability + Errors

Enable `ObservabilityConfig` to emit:

- `error`
- `retry`
- `token_refresh`
- `request_start`/`request_end` (if `verbose_events=True`)

This gives a useful trail without needing HTTP debug dumps.

## Retriable vs Non-Retriable Decisions

Use `is_retryable` as hint only.

Suggested approach:

- prefer explicit handling for `RateLimitError` (`retry_after`)
- treat `NetworkError` and `ServerError` as transient
- treat `ValidationError` and local argument validation errors as hard failures
- treat `TokenRefreshError` as auth-state recovery requirement

## Input Validation Errors Before HTTP Call

Several methods validate arguments locally and raise fast:

- invalid periodicity -> `InvalidPeriodicity`
- invalid sort -> `InvalidSort`
- invalid transaction type -> `InvalidType`
- non-list filters where lists are required -> `TypeError`
- impossible quantity bounds -> `ValueError`

This is intentional and helps catch bugs early.

## Related Docs

- [Authentication](authentication.md)
- [Configuration](configuration.md)
- [Client API Reference](../api/client.md)
