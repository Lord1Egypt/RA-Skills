# network-aiops CLI Reference

All commands accept `-t/--target <name>` to select a configured device. When
omitted, the first device in `~/.network-aiops/config.yaml` is used.

## Onboarding & secrets

```bash
network-aiops init                              # interactive wizard: devices + encrypted passwords (+ NetBox)
network-aiops secret set <name>                 # store/replace a device password, or 'netbox-token' (hidden prompt)
network-aiops secret list                       # names only — values are never printed
network-aiops secret rm <name>                  # delete a stored secret
network-aiops secret migrate                    # import a legacy plaintext .env into the encrypted store
network-aiops secret rotate-password            # re-encrypt the store under a new master password
```

Secrets are stored encrypted in `~/.network-aiops/secrets.enc`. Unlock
non-interactively with `NETWORK_AIOPS_MASTER_PASSWORD`.

## Device facts & state (read-only)

```bash
network-aiops device facts [-t <device>]        # hostname, vendor, model, OS, serial, uptime
network-aiops device interfaces [-t <device>]   # up/down, enabled, speed, description
network-aiops device counters [-t <device>]     # per-interface traffic + error counters
network-aiops device bgp [-t <device>]          # BGP neighbors per VRF
network-aiops device lldp [-t <device>]         # LLDP neighbors
network-aiops device arp [-t <device>]          # ARP table
network-aiops device mac [-t <device>]          # MAC address table
network-aiops device vlans [-t <device>]        # VLANs (id, name, member count)
network-aiops device route <prefix> [-t <device>] [--protocol bgp]  # routing-table lookup
network-aiops device environment [-t <device>]  # fans, temperature, power, CPU, memory
network-aiops device health [-t <device>]       # aggregated health summary
```

Additional read getters are exposed as MCP tools (no dedicated CLI subcommand):
`get_bgp_neighbors_detail`, `get_lldp_neighbors_detail`, `get_optics`,
`get_ntp_servers`, `get_ntp_stats`, `get_users`, `get_snmp_information`,
`get_network_instances`. A getter a driver does not implement returns a teaching
"not supported by the `<driver>` driver" error.

## Configuration

```bash
network-aiops config backup [-t <device>] [-o <file>]      # running config (save with -o)
network-aiops config diff <file> [-t <device>] [--replace] # DRY-RUN: show the diff only
network-aiops config merge <file> [-t <device>] [--dry-run]    # commit; double confirm
network-aiops config replace <file> [-t <device>] [--dry-run]  # HIGH RISK; double confirm
network-aiops config rollback [-t <device>] [--dry-run]        # revert last commit; double confirm
```

- `config diff` stages a candidate, runs `compare_config()`, and discards it —
  nothing is committed. `--replace` diffs as a full-config replacement.
- `--dry-run` on `merge` / `replace` prints the same diff without committing.
- `merge` / `replace` capture the pre-change running config for the undo store.

## NetBox (optional source-of-truth)

```bash
network-aiops netbox list [--name <q>] [--limit N]   # name, role, site, status, primary IP
network-aiops netbox get <name>                      # single device by exact name
network-aiops netbox interfaces <device> [--limit N] # device interfaces from source-of-truth
```

Requires a `netbox:` block in config and an encrypted `netbox-token` secret
(`network-aiops secret set netbox-token`, or via `network-aiops init`).

## Diagnostics & MCP

```bash
network-aiops doctor [--skip-auth]   # check config + encrypted secret store + per-device password + reachability
network-aiops mcp                    # start the MCP server over stdio
```

## Flags summary

| Flag | Meaning |
|------|---------|
| `-t, --target` | Device name from `~/.network-aiops/config.yaml` |
| `-o, --output` | Write `config backup` output to a file |
| `--replace` | Diff/treat the config file as a full replacement (`config diff`) |
| `--dry-run` | Preview a destructive config op as a diff without committing |
| `--protocol` | Filter `device route` by routing protocol (bgp, ospf, …) |
| `--name` | NetBox name filter (`netbox list`) |
| `--limit` | NetBox page size (`netbox list` / `netbox interfaces`) |
| `--skip-auth` | Skip the connectivity check in `doctor` |
