---
name: cluster-management
description: Manage OceanBase cluster lifecycle using obd. Deploy, start, stop, restart, destroy, redeploy, upgrade, scale out, and configure clusters. Includes OCP CE takeover and monitoring setup. Use when creating, operating, or maintaining OceanBase CE clusters via obd, or when users mention obd, OceanBase deployment, cluster management, OCP, or monitoring.
compatibility: Requires obd CLI installed on the control machine.
metadata:
  author: oceanbase
  version: "1.0"
---

# OceanBase Cluster Management (obd)

Manage OceanBase CE cluster lifecycle using the `obd` command-line tool.

Official quick-start guide: [https://www.oceanbase.com/docs/common-obd-cn-1000000005246289](https://www.oceanbase.com/docs/common-obd-cn-1000000005246289)

## When to Use This Skill

- Deploying a new OceanBase CE cluster (demo, config file, or interactive)
- Starting, stopping, restarting, or destroying clusters
- Upgrading cluster components or scaling out
- Preparing clusters for OCP CE takeover
- Setting up monitoring (Prometheus + Grafana)
- Managing mirrors and repositories

**For tenant operations (create, drop, backup, restore):** Use [tenant-management](../tenant-management/SKILL.md).
**For seekdb:** Use [seekdb](../seekdb/SKILL.md).
**For benchmarks and testing:** Use [testing-and-benchmark](../testing-and-benchmark/SKILL.md).
**Overview & routing:** See [oceanbase-deploy](../SKILL.md).

---

## OCP Terminology Convention

- When users say "deploy OCP", "OCP", or similar without further qualification, always use **OCP CE** (`ocp-ce` component in obd config).
- **`ocp-express`** is a legacy lightweight web console. When users explicitly ask for "OCP Express" / "ocp-express" / "lightweight OCP", do NOT deploy it. Explain: **`ocp-express` has been replaced by `obshell dashboard` — deploy OceanBase CE directly and access the dashboard on port `2886`.**
- Never default "deploy OCP" to `ocp-express`.
- `obd cluster check4ocp` / `export-to-ocp` target a running **OCP CE** (or enterprise OCP) control plane, not `ocp-express`.

See [references/ocp-ce.md](references/ocp-ce.md) for OCP CE deployment and takeover details.

---

## Critical Safety Rules

**WARNING**: These commands are destructive and require explicit user confirmation:

1. `obd cluster destroy` — Destroys a cluster and deletes data.
2. `obd cluster redeploy` — Destroys and redeploys a cluster, deleting data.
3. `obd cluster prune-config` — Deletes configuration files of destroyed clusters.

**Always ask the user for confirmation before running these commands.**

---

## Installation

If `obd` is not installed, download the RPM from the OceanBase mirror:
[https://mirrors.oceanbase.com/community/stable/el/](https://mirrors.oceanbase.com/community/stable/el/)

---

## Quick Start

```bash
obd demo
```

- Use `-c` to specify components (e.g., `oceanbase-ce`, `obproxy-ce`, `obagent`). For OCP use `ocp-ce` by default.
- Example: `obd demo -c oceanbase-ce,obproxy-ce`
- Default ports: 2881 (MySQL), 2882 (RPC), 2886 (obshell). If ports are in use, deploy with a config file using alternate ports.

---

## Cluster Lifecycle Commands

| Command | Description |
|---------|-------------|
| `obd cluster deploy <name> -c <config>` | Register config and deploy cluster |
| `obd cluster deploy <name> -i` | Interactive deploy (guided config) |
| `obd cluster start <name>` | Start a deployed cluster |
| `obd cluster stop <name>` | Stop a running cluster |
| `obd cluster restart <name>` | Restart a running cluster |
| `obd cluster list` | List all registered clusters |
| `obd cluster display <name>` | Show cluster status |
| `obd cluster edit-config <name>` | Edit cluster configuration |
| `obd cluster reload <name>` | Reload config on running cluster |
| `obd cluster upgrade <name> -c <component> -V <version>` | Upgrade a component |
| `obd cluster scale_out <name> -c <config>` | Scale out a component |
| `obd cluster component add <name> -c <config>` | Add a new component |
| `obd cluster component del <name> <component>` | Delete a component |

See [references/config-deployment.md](references/config-deployment.md) for detailed deployment steps and config file examples.

---

## OS & Environment Requirements

- **GLIBC**: OceanBase CE 4.3+ el8 packages require GLIBC 2.27+ (RHEL/CentOS 8+). AliOS 7 / CentOS 7 ship GLIBC 2.17 — use the **el7 package of OceanBase CE ≤4.3.x** (e.g., `4.3.5.5`).
- OBD only needs to run on the control machine; it SSHes to remote nodes.
- **OCP CE packages**: `ocp-ce` is not in the public mirror by default. Use `obd mirror list` to verify availability.
- **Port isolation on same host**: When co-deploying multiple OB stacks, ensure distinct ports for MySQL (2881), RPC (2882), and obshell (2886). Pass `obshell_port` in config to override.

---

## Monitoring

Add GUI-based monitoring with OBAgent, Prometheus, and Grafana.

- **Without OBAgent**: Add `obagent`, `prometheus`, and `grafana` to config and redeploy/start.
- **With OBAgent already deployed**: Add `prometheus` and `grafana`, configure Prometheus to scrape OBAgent.
- OBD enables HTTP basic auth for Prometheus. Credentials are shown in `obd cluster display <name>`.
- **Deletion order**: Delete `grafana` and `prometheus` before `obagent` (dependency order).

See [references/monitoring.md](references/monitoring.md) for setup details.

---

## Mirror & Repository Management

| Command | Description |
|---------|-------------|
| `obd mirror list [repo]` | List mirrors |
| `obd mirror update` | Update mirrors |
| `obd mirror clone <rpm> [-f]` | Clone RPM to local |
| `obd mirror create -n <name> -p <path> -V <version>` | Create mirror |
| `obd mirror enable <repo>` / `disable <repo>` | Enable/disable mirror |
| `obd mirror clean` | Clean mirrors |

See [references/mirror-management.md](references/mirror-management.md) for details.

---

## OCP CE Takeover

Prepare an OBD-deployed cluster to be managed by OCP CE (or enterprise OCP).

1. **Check**: `obd cluster check4ocp <name> -V <ocp_version>`
2. **Export**: `obd cluster export-to-ocp <name> -a <ocp_address> -u <user> -p <password>`

See [references/ocp-ce.md](references/ocp-ce.md) for complete OCP CE deployment and takeover procedures.

---

## Usage Examples

### Quick Demo
```bash
obd demo
```

### Deploy with Config File
```bash
obd cluster deploy my-cluster -c config.yaml
obd cluster start my-cluster
```

### Interactive Deploy
```bash
obd cluster deploy demo-cluster -i
```

### Explicitly Requesting OCP Express
User: "Help me deploy ocp-express."
Agent: "`ocp-express` has been replaced by `obshell dashboard`. Deploy OceanBase CE directly and access the dashboard on port `2886`."

### Destroying a Cluster (Requires Confirmation)
User: "Destroy my-cluster."
Agent: "This will destroy 'my-cluster' and all its data. Are you sure?"
User: "Yes."
```bash
obd cluster destroy my-cluster
```

---

## Related Skills

- [tenant-management](../tenant-management/SKILL.md) — Tenant CRUD, backup, restore
- [seekdb](../seekdb/SKILL.md) — seekdb lifecycle and HA
- [testing-and-benchmark](../testing-and-benchmark/SKILL.md) — Sysbench, TPC-H, TPC-C benchmarks; mysqltest functional tests
