# Authentication

This guide explains all authentication paths supported by `peerberry_sdk.PeerberryClient` and how token lifecycle behavior is controlled.

## Supported Authentication Inputs

The client accepts three input patterns:

1. `email` + `password`
2. `email` + `password` + `tfa_secret` (2FA)
3. `access_token` + optional `refresh_token`

## Default Flow (`auto_login=True`)

By default, authentication runs during `PeerberryClient(...)` initialization.

```python
from peerberry_sdk import PeerberryClient

api = PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD")
```

Behavior:

- if access token is present, SDK validates it first
- if token is valid, session starts immediately
- if token is stale and credentials are available, SDK falls back to credential login

## Two-Factor Authentication (TOTP)

If account login requires TOTP, pass `tfa_secret`:

```python
from peerberry_sdk import PeerberryClient

api = PeerberryClient(
    email="YOUR_EMAIL",
    password="YOUR_PASSWORD",
    tfa_secret="BASE32_TOTP_SECRET",
)
```

Prerequisite:

```bash
pip install "peerberry-sdk[otp]"
```

Without `pyotp` installed, the 2FA login path cannot complete.

## Token-Based Startup

You can provide existing tokens directly:

```python
from peerberry_sdk import PeerberryClient

api = PeerberryClient(
    access_token="ACCESS_TOKEN",
    refresh_token="REFRESH_TOKEN",
)
```

If access token is stale:

- SDK can refresh automatically when configured to do so
- fallback to credentials is possible only if `email` and `password` are available

## Disabling Auto Login

Use deferred authentication when startup order matters:

```python
from peerberry_sdk import PeerberryClient

api = PeerberryClient(
    email="YOUR_EMAIL",
    password="YOUR_PASSWORD",
    auto_login=False,
)

# authenticate later
api.login()
```

## Token Refresh Behavior

Refresh logic is controlled by `AuthConfig`:

- `auto_refresh_on_auth_error` (default `True`)
- `max_refresh_attempts` (default `1`)
- `proactive_refresh` (default `True`)
- `proactive_refresh_skew_seconds` (default `60`)

### Reactive Refresh

Triggered when a request gets an auth error and auto refresh is enabled.

### Proactive Refresh

Triggered before requests when token expiry is near (`exp - skew_seconds`).

## Forcing a Refresh

You can trigger refresh explicitly:

```python
bearer = api.token()
print(bearer)  # "Bearer ..."
```

If refresh token is missing or refresh fails, `TokenRefreshError` is raised.

## Token Persistence With `TokenStore`

`AuthConfig.token_store` defines where tokens are loaded/saved.

Default store:

- `InMemoryTokenStore` (process memory only)

Standard behavior:

- load on init when `load_tokens_on_init=True`
- save on login/refresh
- clear on logout

## Custom Token Store

Implement `TokenStore` to persist tokens in your own backend.

```python
from peerberry_sdk import TokenStore, TokenPair

class EnvTokenStore(TokenStore):
    def load(self) -> TokenPair:
        return TokenPair(
            access_token=None,
            refresh_token=None,
        )

    def save(self, access_token, refresh_token) -> None:
        # persist to your secure storage
        pass

    def clear(self) -> None:
        # clear persisted tokens
        pass
```

Then plug into `AuthConfig(token_store=...)`.

## Login Method Details

`login()` returns a bearer token string:

```python
bearer = api.login()
```

Return format:

- `"Bearer <access_token>"`

Common failures:

- `InvalidCredentials`
- other `PeerberryException` subclasses

## Logout and Close

Preferred shutdown:

```python
api.close(logout=True)
```

Equivalent explicit sequence:

```python
api.logout()
api.close()
```

`logout()` clears active auth headers and token store data.

## Lifecycle Modes

You can enforce logout during close via config:

```python
from peerberry_sdk import PeerberryClient, LifecycleConfig, SDKConfig

cfg = SDKConfig(lifecycle=LifecycleConfig(logout_on_close=True))
api = PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD", config=cfg)
```

Control logout error behavior:

- `swallow_logout_errors=True` -> ignore logout failures during close
- `swallow_logout_errors=False` -> re-raise logout failure after close

## Recommended Production Pattern

```python
from peerberry_sdk import PeerberryClient, SDKConfig, AuthConfig, TokenRefreshError

config = SDKConfig(
    auth=AuthConfig(
        auto_refresh_on_auth_error=True,
        max_refresh_attempts=1,
        proactive_refresh=True,
    )
)

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD", config=config) as api:
    try:
        print(api.get_overview())
    except TokenRefreshError:
        # signal re-authentication path in your app
        raise
```

## Related Docs

- [Configuration](configuration.md)
- [Error Handling](error-handling.md)
- [Client API Reference](../api/client.md)
