---
name: oceanbase-deploy
description: Overview skill for OceanBase deployment and operations using obd. Routes to specialized skills for cluster management, tenant management, seekdb, and testing. Use as a starting point when the user's intent is not yet clear, or for general OceanBase obd questions. Also use when users mention OceanBase, obd, or want an overview of available OceanBase operations.
compatibility: Requires obd CLI installed on the control machine.
metadata:
  author: oceanbase
  version: "2.0"
---

# OceanBase Deploy & Operations (obd)

This is the entry point for OceanBase operations via `obd`. Use the specialized skills below for specific tasks.

## Skill Index

| Skill | Use When |
|-------|----------|
| [cluster-management](cluster-management/SKILL.md) | Deploy, start, stop, upgrade, scale out clusters. OCP CE takeover. Monitoring setup. |
| [tenant-management](tenant-management/SKILL.md) | Create/drop tenants, backup, restore, optimize workloads. |
| [seekdb](seekdb/SKILL.md) | seekdb install, deploy, HA (switchover/failover/decouple). |
| [testing-and-benchmark](testing-and-benchmark/SKILL.md) | Sysbench, TPC-H, TPC-C benchmarks; mysqltest functional tests. |

## Quick Start

```bash
obd demo
```

Deploys a local demo cluster with default ports (2881 MySQL, 2882 RPC, 2886 obshell).

## Installation

If `obd` is not installed, download from:
[https://mirrors.oceanbase.com/community/stable/el/](https://mirrors.oceanbase.com/community/stable/el/)

Official quick-start guide:
[https://www.oceanbase.com/docs/common-obd-cn-1000000005246289](https://www.oceanbase.com/docs/common-obd-cn-1000000005246289)

## OCP Terminology Convention

- "Deploy OCP" always means **OCP CE** (`ocp-ce`), never `ocp-express`.
- `ocp-express` has been replaced by `obshell dashboard` (port 2886). Do not deploy it.
- See [cluster-management/references/ocp-ce.md](cluster-management/references/ocp-ce.md) for details.

## Critical Safety Rules

These destructive commands always require explicit user confirmation:

1. `obd cluster destroy` — Destroys cluster and data
2. `obd cluster redeploy` — Destroys and redeploys, data loss
3. `obd cluster prune-config` — Deletes config files
