# seekdb HA Operations

Primary-standby switchover, failover, and decouple procedures.

## Display Topology

```bash
obd seekdb display <name> -g
```

Shows the cluster topology graph (primary, standbys, cascading relationships).

## Switchover (Planned)

```bash
obd seekdb switchover <name>
```

- **Purpose**: Planned primary-standby swap during maintenance.
- **Requirement**: The primary cluster must be **online and running**.
- Promotes the specified standby to primary; the original primary becomes standby.
- Use for rolling maintenance, planned migrations, or load rebalancing.

## Failover (Emergency)

```bash
obd seekdb failover <name>
```

- **Purpose**: Emergency promotion when the primary is down or unreachable.
- **Requirement**: The primary must be **stopped or unreachable**. If the primary is still running, failover will error — use `switchover` instead.
- Promotes the specified standby to primary.
- After failover, the old primary (once recovered) needs manual intervention to rejoin as standby.

## Decision Guide

| Scenario | Primary Status | Use |
|----------|---------------|-----|
| Planned maintenance window | Running | `switchover` |
| Primary crashed / unreachable | Stopped / unreachable | `failover` |
| Primary still running but slow | Running | `switchover` (NOT failover) |
| Want to test HA | Stop primary first, then | `failover` |

## Decouple

```bash
obd seekdb decouple <name>
```

- Removes the specified standby from the primary-standby relationship.
- The decoupled standby becomes an **independent primary** and continues running.
- Use when you want to permanently split a standby into its own independent database.

## Destroy with Standby

```bash
obd seekdb destroy <name> --ignore-standby
```

- Destroying a primary that has active standbys requires `--ignore-standby`.
- Without this flag, OBD refuses and warns about orphaned standbys.
- **Always confirm with the user** before destroying a primary with active standbys.
