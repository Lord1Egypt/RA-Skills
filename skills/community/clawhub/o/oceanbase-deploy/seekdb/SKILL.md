---
name: seekdb
description: Manage seekdb instances using obd seekdb commands. Install, deploy, start, stop, destroy, and takeover seekdb. Set up primary-standby replication, perform switchover, failover, and decouple operations. Use when users mention seekdb, obd seekdb, or need a lightweight OceanBase-based database with primary-standby HA capabilities.
compatibility: Requires obd CLI with seekdb support.
metadata:
  author: oceanbase
  version: "1.0"
---

# seekdb Management (obd seekdb)

seekdb is a lightweight database component managed by OBD. All `obd seekdb` commands only apply to deployments containing the seekdb component.

## When to Use This Skill

- Installing or deploying seekdb instances
- Managing seekdb lifecycle (start, stop, restart, destroy)
- Setting up primary-standby replication
- Performing switchover, failover, or decouple operations
- Taking over existing seekdb instances not deployed by OBD

**For OceanBase cluster management:** Use [cluster-management](../cluster-management/SKILL.md).
**For tenant operations:** Use [tenant-management](../tenant-management/SKILL.md).

---

## Command Reference

| Command | Description |
|---------|-------------|
| `obd seekdb install` | Interactive install (single node, requires TTY) |
| `obd seekdb install --primary` | Install as primary (enables RPC for standby sync) |
| `obd seekdb install --standby` | Install as standby (selects from running primaries) |
| `obd seekdb deploy <name> -c <config>` | Deploy with config file |
| `obd seekdb list` | List seekdb deployments only |
| `obd seekdb start <name>` | Start |
| `obd seekdb stop <name>` | Stop |
| `obd seekdb restart <name>` | Restart |
| `obd seekdb display <name>` | Show info |
| `obd seekdb display <name> -g` | Show topology graph |
| `obd seekdb destroy <name>` | Destroy (see safety rules below) |
| `obd seekdb takeover <name> --home-path <path>` | Takeover non-OBD instance |
| `obd seekdb switchover <name>` | Planned primary-standby swap |
| `obd seekdb failover <name>` | Emergency promote standby to primary |
| `obd seekdb decouple <name>` | Decouple standby into independent primary |

---

## Critical Safety Rules

### Destroy with Standby
Destroying a primary that still has standby clusters requires `--ignore-standby`:
```bash
obd seekdb destroy <name> --ignore-standby
```
Without this flag, OBD will refuse and warn about the risk.

### Failover vs Switchover

| Operation | When to Use | Primary Must Be |
|-----------|-------------|-----------------|
| `switchover` | Planned maintenance | **Online** (running) |
| `failover` | Primary is down/unreachable | **Stopped or unreachable** |

**`failover` will error if the primary is still running.** Use `switchover` for planned swaps.

### Same-Host Restriction
Primary and standby **must be on different IPs**. If deployed on the same IP, OBD suppresses `--role=STANDBY`, causing the standby to start as a primary — log sync will not work.

---

## Install Modes

See [references/install-modes.md](references/install-modes.md) for detailed install mode behavior, TTY requirements, and non-interactive deployment limitations.

## HA Operations

See [references/ha-operations.md](references/ha-operations.md) for detailed switchover, failover, and decouple procedures.

---

## Usage Examples

### Deploy and Start seekdb
```bash
obd seekdb deploy my-seekdb -c seekdb-config.yaml
obd seekdb start my-seekdb
```

### View Topology
```bash
obd seekdb display my-seekdb -g
```

### Takeover Existing Instance
```bash
obd seekdb takeover my-seekdb --home-path /home/admin/seekdb
```

---

## Related Skills

- [cluster-management](../cluster-management/SKILL.md) — OceanBase cluster lifecycle
- [tenant-management](../tenant-management/SKILL.md) — Tenant operations
- [testing-and-benchmark](../testing-and-benchmark/SKILL.md) — Performance testing
