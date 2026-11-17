# Configuration reference

hearth is configured by a single YAML file: `~/.hearth/devices.yaml` (or wherever `$HEARTH_CONFIG` points).

## File structure

```yaml
defaults:    # optional — applied to every device unless overridden
  ssh_connect_timeout: 4
  device_timeout: 18
  ping_count: 1
  ping_timeout: 2

devices:     # required — list of one or more devices to probe
  - name: ...
    address: ...
    ...

groups:      # optional — named groups for partial sweeps
  cluster: [head-node, compute-01, compute-02]
  iot: [pi-zero, esp32-bridge]
```

## Defaults

| Key | Type | Default | Notes |
|-----|------|---------|-------|
| `ssh_connect_timeout` | int (seconds) | 4 | Increase for mobile/slow Wi-Fi |
| `device_timeout` | int (seconds) | 18 | Hard upper bound per device |
| `ping_count` | int | 1 | ICMP packets sent at L1 |
| `ping_timeout` | int (seconds) | 2 | Per-packet timeout at L1 |
| `disk_warn_pct` | int (%) | 90 | DEGRADED when `/` usage ≥ this |
| `mem_warn_pct` | int (%) | 90 | DEGRADED when memory used ≥ this |
| `load_warn_per_cpu` | number | 2 | DEGRADED when 1-min load > (cores × this) |
| `temp_warn_c` | number (°C) | 75 | DEGRADED when CPU temp ≥ this (Pi / thermal-zone hosts) |

### Health status and exit codes

Every probe resolves to one of three states, shown as a coloured tag in the
output header and reflected in the process exit code:

| State | Meaning | check-device exit | sweep exit (worst of all devices) |
|-------|---------|-------------------|-----------------------------------|
| `[OK]` | healthy | 0 | 0 |
| `[DEGRADED]` | a measured threshold/service/app check failed | 1 | 1 |
| `[DOWN]` | unreachable at L1 | 2 | 2 |

Thresholds are only applied to layers that were actually measured — an
`http-only` host or a chroot is never marked degraded for a layer it can't
report (honest reporting). This makes `sweep.sh` safe to use as a cron/CI
health gate: a non-zero exit means something genuinely needs attention.

## Device fields

### Required for every device

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Short identifier shown in output. Lowercase, hyphens. Must be unique. |
| `address` | string | IP or hostname reachable from the bridgehead |
| `auth` | enum | One of: `local`, `ssh-pass`, `ssh-key`, `http-only` |

### Conditional fields by auth type

For `auth: ssh-pass`:
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `user` | string | yes | SSH username |
| `password_env` | string | yes | Name of env var holding the password |

For `auth: ssh-key`:
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `user` | string | yes | SSH username |
| `key_path` | string | yes | Path to private key, `~` is expanded |

For `auth: local`:
No additional auth fields. Probes run as the user invoking hearth.

For `auth: http-only`:
No SSH fields. L2-L4 are reported as `unmanaged-host (no SSH)`. Use `apps:` for L5 health.

### Optional fields (any auth type)

| Field | Type | Notes |
|-------|------|-------|
| `services` | list of strings | systemd units checked at L4 |
| `apps` | list of app probes | L5 health probes (see below) |
| `no_systemd` | bool | If true, L4 reports "no-systemd (chroot — N/A)" instead of probing |
| `expected_failed_units` | list | systemd units expected to be failed; not flagged in output |
| `ssh_connect_timeout` | int | Override default per-device |
| `device_timeout` | int | Override default per-device |
| `ssh_warmup` | bool | Do a throwaway SSH first; useful for mobile/chroot devices |
| `role` | string | Description shown in output header in parentheses |
| `notes` | string | Free-form, ignored by hearth — for your benefit |

## App probes (`apps:` list)

Each app is one of two types: `http` or `command`.

### Type: `http`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | yes | Shown in L5 output |
| `type` | `http` | yes | |
| `url` | string | yes | Full URL with scheme |
| `expect_code` | int | no, default 200 | HTTP status code to expect |
| `expect_match` | regex | no | Regex match against response body |
| `auth_header_env` | string | no | Env var name holding bearer token |
| `verify_tls` | bool | no, default true | Set false for self-signed certs |
| `resolve` | string | no | Format: `hostname:port:ip` — forces SNI bypass |
| `json_extract` | string | no | Dotted path to extract from JSON response (planned, not yet implemented) |

### Type: `command`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | yes | Shown in L5 output |
| `type` | `command` | yes | |
| `command` | string | yes | User-defined read-only command run on the device (or locally if auth=local). Sourced verbatim from your own config — hearth does not generate, fetch, or modify commands. |
| `expect_match` | regex | no | Regex against command stdout — output is OK if matches |
| `expect_no_match` | regex | no | Inverse — output is OK if doesn't match |

For `auth: http-only` devices, `command` probes are skipped with `<name>=skipped (http-only host)`.

## Groups

A simple way to scope sweeps. Each group is a list of device names.

```yaml
groups:
  cluster: [head-node, compute-01, compute-02]
  web: [main-server, web-stack]
  iot: [pi-zero, esp32-bridge]
```

Run a group: `./scripts/sweep.sh --group cluster`

## Environment variables hearth reads

| Var | Purpose |
|-----|---------|
| `HEARTH_CONFIG` | Override config path (default: `~/.hearth/devices.yaml`) |
| `HEARTH_PASS_<NAME>` | SSH passwords, referenced by `password_env:` |
| `HEARTH_<APP>_TOKEN` | HTTP bearer tokens, referenced by `auth_header_env:` |

The naming convention `HEARTH_PASS_<NAME>` is recommended but not enforced. The actual env var name comes from your config's `password_env:` field.

## A complete worked example

See `examples/devices.example.yaml` for a fully-commented sample covering all 8 device archetypes.

## Validation

`./scripts/sweep.sh --dry-run` parses your config and lists devices that would be probed without contacting any of them. Use this to sanity-check after editing.

## What hearth WON'T read from config

For security, the following are NEVER stored in `devices.yaml`:

- Passwords or tokens (use env vars)
- SSH private keys (use `key_path` to point at the file in `~/.ssh/`)
- API secrets

If your YAML contains literal credential values, you've made a mistake — move them to env vars before committing the file anywhere.