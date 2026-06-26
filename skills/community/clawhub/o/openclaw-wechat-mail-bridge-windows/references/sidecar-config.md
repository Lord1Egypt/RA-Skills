# Sidecar config reference (TOML)

Top-level:

- `sidecar_id`
- `adapter`: `mock` | `pywinauto` | `uiautomation`
- `allow_groups`
- `watch_poll_interval_sec`

`[bridge]`:

- `base_url`
- `shared_secret`
- `auth_mode`: `bearer` or `hmac`
- `request_timeout_sec`
- `claim_batch_size`
- `send_poll_interval_sec`
- `heartbeat_interval_sec`

`[webhook_proxy]` (optional):

- `enabled`
- `host`
- `port`
- `shared_secret`
- `inbound_secret` (optional; default `local-webhook-secret`; set empty to disable inbound secret checks)

`[diagnostics]`:

- `enabled`
- `host`
- `port`
