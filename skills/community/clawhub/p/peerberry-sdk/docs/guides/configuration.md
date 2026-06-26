# Configuration

`peerberry_sdk` runtime behavior is configured through `SDKConfig`, which groups transport, auth, observability, and lifecycle settings.

## Configuration Map

- `SDKConfig.transport` -> `TransportConfig`
- `SDKConfig.auth` -> `AuthConfig`
- `SDKConfig.observability` -> `ObservabilityConfig`
- `SDKConfig.lifecycle` -> `LifecycleConfig`

## Full Example

```python
import logging
from peerberry_sdk import (
    PeerberryClient,
    AuthConfig,
    InMemoryTokenStore,
    LifecycleConfig,
    ObservabilityConfig,
    RetryConfig,
    SDKConfig,
    TransportConfig,
)

config = SDKConfig(
    transport=TransportConfig(
        timeout=20.0,
        retry=RetryConfig(
            max_retries=3,
            backoff_factor=0.5,
            max_backoff=8.0,
            retry_status_codes=(429, 500, 502, 503, 504),
            retry_on_network_errors=True,
        ),
        header_profile={"x-app-system": "Linux x86_64"},
        user_agent="Chrome 145.0.0.0",
        app_system="Linux x86_64",
        sec_ch_ua_platform='"Linux"',
    ),
    auth=AuthConfig(
        auto_refresh_on_auth_error=True,
        max_refresh_attempts=1,
        proactive_refresh=True,
        proactive_refresh_skew_seconds=60,
        token_store=InMemoryTokenStore(),
        load_tokens_on_init=True,
    ),
    observability=ObservabilityConfig(
        event_hook=lambda event: print(event["event_type"]),
        logger=logging.getLogger("peerberry-sdk"),
        verbose_events=False,
        redactor=None,
    ),
    lifecycle=LifecycleConfig(
        logout_on_close=False,
        swallow_logout_errors=True,
    ),
)

api = PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD", config=config)
```

## `RetryConfig`

Controls retry behavior in HTTP transport.

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `max_retries` | `int` | `2` | Number of retry attempts after first failure. |
| `backoff_factor` | `float` | `0.5` | Exponential backoff base (`factor * 2**attempt`). |
| `max_backoff` | `float` | `8.0` | Upper bound for delay. |
| `retry_status_codes` | `tuple[int, ...]` | `(429, 500, 502, 503, 504)` | HTTP statuses treated as retryable. |
| `retry_on_network_errors` | `bool` | `True` | Retries transport/network exceptions. |

Notes:

- `Retry-After` header is honored when present (capped by `max_backoff`).
- Exhausted retries raise typed exceptions with context.

## `TransportConfig`

Controls request-level transport settings.

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `timeout` | `float | None` | `30.0` | Request timeout in seconds (if set). |
| `retry` | `RetryConfig` | defaults | Retry policy object. |
| `header_profile` | `dict[str, str] | None` | `None` | Inline static header overrides. |
| `header_profile_path` | `str | None` | `None` | Path to JSON header profile. |
| `user_agent` | `str | None` | `None` | Convenience override for `x-app-user-agent`. |
| `app_system` | `str | None` | `None` | Convenience override for `x-app-system`. |
| `sec_ch_ua_platform` | `str | None` | `None` | Convenience override for `sec-ch-ua-platform`. |

Header source precedence (lowest to highest):

1. SDK defaults
2. profile file (`header_profile_path` or env)
3. inline `header_profile`
4. convenience fields (`user_agent`, etc.) merged into request opts
5. per-request headers

## Header Profiles

Three ways to supply profile headers:

```python
# 1) Inline
PeerberryClient(..., request_opts={"header_profile": {"x-app-system": "Linux x86_64"}})

# 2) File path
PeerberryClient(..., request_opts={"header_profile_path": "/path/to/profile.json"})
```

```bash
# 3) Environment variable
export peerberry_sdk_HEADER_PROFILE=/path/to/profile.json
```

Accepted profile JSON formats:

```json
{ "x-app-system": "Linux x86_64", "x-app-user-agent": "Chrome 145.0.0.0" }
```

or:

```json
{ "headers": { "x-app-system": "Linux x86_64" } }
```

## `AuthConfig`

Controls login/refresh/token persistence behavior.

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `auto_refresh_on_auth_error` | `bool` | `True` | Retry request after auth failure by refreshing token. |
| `max_refresh_attempts` | `int` | `1` | Number of refresh attempts per failing request. |
| `proactive_refresh` | `bool` | `True` | Refresh before request if token near expiry. |
| `proactive_refresh_skew_seconds` | `int` | `60` | Expiry lead time window for proactive refresh. |
| `token_store` | `TokenStore` | `InMemoryTokenStore()` | Store for load/save/clear token pair. |
| `load_tokens_on_init` | `bool` | `True` | Load tokens from store when constructor tokens missing. |

## `ObservabilityConfig`

Controls event emission and logging hooks.

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `event_hook` | `Callable[[dict], None] | None` | `None` | Callback for each emitted event. |
| `logger` | `logging.Logger | None` | `None` | Logger integration for emitted events. |
| `verbose_events` | `bool` | `False` | Enables `request_start` and `request_end` events. |
| `redactor` | `Callable[[dict], dict] | None` | `None` | Custom redaction pass for event payloads. |

Always-emitted event families:

- `error`
- `retry`
- `token_refresh`

Verbose-only event families:

- `request_start`
- `request_end`

Sensitive keys are redacted by default (`authorization`, `access_token`, `refresh_token`, `password`, etc.).

## `LifecycleConfig`

Controls behavior at `PeerberryClient.close()`.

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `logout_on_close` | `bool` | `False` | Attempt remote logout during close. |
| `swallow_logout_errors` | `bool` | `True` | Suppress logout errors during close. |

## Common Configuration Profiles

## Conservative Production Profile

```python
from peerberry_sdk import SDKConfig, TransportConfig, RetryConfig, AuthConfig

config = SDKConfig(
    transport=TransportConfig(
        timeout=20.0,
        retry=RetryConfig(max_retries=2, backoff_factor=0.5),
    ),
    auth=AuthConfig(
        auto_refresh_on_auth_error=True,
        max_refresh_attempts=1,
        proactive_refresh=True,
    ),
)
```

## Low-Latency Profile

```python
from peerberry_sdk import SDKConfig, TransportConfig, RetryConfig

config = SDKConfig(
    transport=TransportConfig(
        timeout=10.0,
        retry=RetryConfig(max_retries=1, backoff_factor=0.2, max_backoff=1.0),
    )
)
```

## Debug/Trace Profile

```python
import logging
from peerberry_sdk import SDKConfig, ObservabilityConfig

config = SDKConfig(
    observability=ObservabilityConfig(
        logger=logging.getLogger("peerberry-sdk"),
        verbose_events=True,
    )
)
```

## Related Docs

- [Authentication](authentication.md)
- [Error Handling](error-handling.md)
- [Client API Reference](../api/client.md)
