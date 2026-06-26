# seekdb Install Modes

Detailed behavior of seekdb installation modes and their constraints.

## Interactive Install (Default)

```bash
obd seekdb install
```

- Installs a single-node seekdb interactively.
- **Requires a real TTY terminal** — cannot be automated via pipe input.
- For scripted/CI deployment, use `obd seekdb deploy <name> -c <config>` instead.

## Primary Mode

```bash
obd seekdb install --primary
```

- Installs as a primary cluster with RPC enabled for standby sync.
- **Requires TTY.**
- Must be installed before any standby can connect.

## Standby Mode

```bash
obd seekdb install --standby
```

- Installs as a standby cluster.
- Interactively selects from deployed and RUNNING seekdb primaries.
- **Requires TTY.**
- The standby's available disk for redo logs must be **no less than** the primary's configured `log_disk_size`.
- `--standby` and `--primary` cannot be used together.
- Standby mode validates that the primary has `enable_rpc_service` enabled. If not, restart the primary first.

## Same-Host Restriction

**Primary and standby must be on different IPs.**

If both are on the same IP, OBD's same-host conflict avoidance logic sets `mock_primary_rpc_info` to None, which prevents the `--role=STANDBY` startup parameter from being passed. The standby process starts as a primary (`ACCESS_MODE=APPEND`), and log sync fails silently.

## Non-Interactive Deploy Limitation

```bash
obd seekdb deploy <name> -c config.yaml
```

Even if `log_restore_source` is set in the YAML config, OBD does **not** pass `--role=STANDBY` to the seekdb process in non-interactive mode. The standby starts as a primary, and log sync does not work.

**To establish real primary-standby sync, you must use `obd seekdb install --standby` (requires TTY) with primary and standby on different IPs.**

## Takeover

```bash
obd seekdb takeover <name> --home-path <path>
```

Takes over a seekdb instance **not deployed by OBD**:
- `--home-path` is required.
- Also needs host, `mysql_port`, `root` password, and SSH information (via config or interactive input).
- OBD generates configuration and brings the instance under management.
