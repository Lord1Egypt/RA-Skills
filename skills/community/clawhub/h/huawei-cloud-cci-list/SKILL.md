---
name: huawei-cloud-cci-list
description: |
  1. List Huawei Cloud Cloud Container Instance (CCI) resources in a tenant
     region through KooCLI (hcloud CCI List* — read-only Kubernetes-style GET
     operations): namespaces (ListCoreV1Namespace, GET /api/v1/namespaces),
     pods / instances (ListCoreV1PodForAllNamespaces, GET /api/v1/pods;
     ListCoreV1NamespacedPod, GET /api/v1/namespaces/{namespace}/pods) and
     workloads (ListAppsV1DeploymentForAllNamespaces,
     GET /apis/apps/v1/deployments; ListAppsV1NamespacedDeployment,
     GET /apis/apps/v1/namespaces/{namespace}/deployments).
  2. Three output modes: key-field table (default, 名称/命名空间/状态/副本/创建时间
     等关键字段), --json (raw Kubernetes objects) and --names-only (compact
     namespace/name inventory).
  3. Supports --resource namespace|pod|deployment, --namespace scoping,
     --name (client-side substring), --label-selector / --field-selector
     (real Kubernetes server-side query parameters), a region override and
     automatic continue-token paging.
  4. Explicit error hints for empty resource lists (「当前区域无 CCI 资源」),
     403 / insufficient IAM permission (「无权限访问云容器实例（CCI）」), missing or
     invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / patch /
     replace / apply / scale / restart / pod exec / ...) or any operation other
     than the five read-only List operations is rejected before execution —
     this skill is strictly read-only.
  6. Triggers include: "list CCI namespaces", "CCI 命名空间列表", "CCI Pod 列表",
     "CCI 实例列表", "query CCI resources", "CCI 日常巡检", "CCI 盘点",
     "list cci pods", "cloud container instance inventory", "华为云CCI列表".
  7. Offline unit tests (mocked hcloud subprocess) cover routing, output modes,
     filters, paging, error scenarios and the write-intent guard.
tags: [huawei-cloud, cci, compute, readonly, koo-cli]
---

# Huawei Cloud CCI (Cloud Container Instance) Resource List

## Overview

Query the read-only resource lists of Huawei Cloud Cloud Container Instance
(CCI) in a tenant region through KooCLI, selecting the resource family with
`--resource`:

| `--resource` | KooCLI operation | REST path | Scope |
| ------------ | ---------------- | --------- | ----- |
| `namespace` | `CCI ListCoreV1Namespace` | `GET /api/v1/namespaces` | cluster-wide |
| `pod` | `CCI ListCoreV1PodForAllNamespaces` | `GET /api/v1/pods` | cluster-wide |
| `pod` (with `--namespace`) | `CCI ListCoreV1NamespacedPod` | `GET /api/v1/namespaces/{namespace}/pods` | namespace |
| `deployment` | `CCI ListAppsV1DeploymentForAllNamespaces` | `GET /apis/apps/v1/deployments` | cluster-wide |
| `deployment` (with `--namespace`) | `CCI ListAppsV1NamespacedDeployment` | `GET /apis/apps/v1/namespaces/{namespace}/deployments` | namespace |

The skill is aimed at CCI inventory inspection, daily operations patrol, and as a
pre-query step for other CCI skills that need a namespace, pod or deployment
name.

Architecture:

```text
agent → python3 scripts/list_cci.py --resource <ns|pod|deployment>
      → hcloud CCI List* --cli-region=<region> [--namespace=<ns>]
      → Huawei Cloud CCI OpenAPI (Kubernetes-style REST) → parsed JSON → table / --json / --names-only
```

Key properties:

- **Read-only by design** — only the five `List*` (GET) operations are ever
  constructed. A write-intent guard scans user arguments and validates the
  operation name; mutating intents (create / delete / patch / replace / apply /
  scale / restart / pod exec ...) are rejected with an explicit message before
  any command runs.
- **KooCLI only** — CCI exposes a Kubernetes-style OpenAPI and ships **no public
  Python SDK package** (`huaweicloudsdkcci` is not published on PyPI), so there
  is no SDK fallback path; KooCLI is the single execution backend. Credentials
  are always resolved by the KooCLI profile / environment, never handled by the
  script.
- **Key-field table default** — the default table renders the union of the
  flattened Kubernetes key fields (name / namespace / status / replicas / pod
  IP / node / creation timestamp / labels).
- **Server-side filters & automatic paging** — `--label-selector` /
  `--field-selector` are real Kubernetes list query parameters; paging follows
  the response `metadata.continue` token automatically.
- **Offline-testable** — every code path (routing, filters, paging, error
  classification, guard) is covered by unit tests that mock the hcloud
  subprocess.

**Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

Out of scope: every mutating CCI action (create / delete a namespace, create /
delete / update a pod or deployment, pod exec, scaling). Those require a
dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   CCI has no public Python SDK, so KooCLI is the only supported backend.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or set credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes, or
   stores secrets itself — authentication is delegated entirely to the hcloud
   profile.
3. **IAM permission** — read-only `cci:namespace:list` and `cci:pod:list`;
   least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to the region CCI endpoint
   (`cci.<region>.myhuaweicloud.com`).
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **Confirm the target region** (default `cn-north-4`); the CCI resource list is
   region-scoped.
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired `--resource`, output mode and
   filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Error Handling table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-cci-list -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Key-field table (default): namespaces
python3 scripts/list_cci.py --region cn-north-4

# Pods / instances across all namespaces
python3 scripts/list_cci.py --resource pod --region cn-north-4

# Pods in one namespace
python3 scripts/list_cci.py --resource pod --namespace default

# Deployments (all namespaces / one namespace)
python3 scripts/list_cci.py --resource deployment
python3 scripts/list_cci.py --resource deployment --namespace default

# Raw Kubernetes objects
python3 scripts/list_cci.py --resource pod --json

# Compact namespace/name inventory
python3 scripts/list_cci.py --resource pod --names-only

# Client-side name filter (substring) and server-side selectors
python3 scripts/list_cci.py --resource pod --name web
python3 scripts/list_cci.py --resource pod --label-selector app=web
python3 scripts/list_cci.py --resource pod --field-selector status.phase=Running

# Equivalent direct KooCLI commands (the script wraps exactly these calls)
skill-quality-cli run --skill-name huawei-cloud-cci-list -- hcloud CCI ListCoreV1Namespace --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-cci-list -- hcloud CCI ListCoreV1PodForAllNamespaces --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-cci-list -- hcloud CCI ListCoreV1NamespacedPod --cli-region=cn-north-4 --namespace=default --limit=100
skill-quality-cli run --skill-name huawei-cloud-cci-list -- hcloud CCI ListCoreV1NamespacedDeployment --cli-region=cn-north-4 --namespace=default --limit=100
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--resource` | No | Resource family to list (default `namespace`) | `pod` |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-north-4` |
| `--namespace` / `-n` | No | Namespace; scopes `pod` / `deployment` to that namespace (omitted → cluster-wide) | `default` |
| `--name` | No | Filter by object name (client-side, case-insensitive substring; the list APIs expose no name query parameter) | `web` |
| `--label-selector` | No | Kubernetes label selector (real server-side query parameter) | `app=web` |
| `--field-selector` | No | Kubernetes field selector (real server-side query parameter) | `status.phase=Running` |
| `--json` | No | Output the raw Kubernetes objects as JSON | — |
| `--names-only` | No | Output a compact name inventory (`namespace/name` for namespaced resources) | — |
| `--page-size` | No | Page size for the list call (default 100, range 1–1000; pages fetched automatically) | `500` |
| `--operation` | No | hcloud CCI operation name; only the five read-only `List*` operations are allowed | `ListCoreV1PodForAllNamespaces` |

Output-mode precedence: `--names-only` → `--json` → key-field table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `deletecollection`, `update`, `patch`,
  `replace`, `apply`, `connect`, `exec`, `scale`, `resize`, `restart`, `rollout`,
  `drain`, `evict`, `cordon`, `taint`, `annotate`, `label`, `stop`, `terminate`,
  and the concrete CCI operations `CreateCoreV1Namespace`,
  `DeleteCoreV1NamespacedPod`, `PatchCoreV1NamespacedPod`,
  `ConnectCoreV1PostNamespacedPodExec`, `CreateAppsV1NamespacedDeployment`, ...).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only the five read-only `List*` (GET) operations are ever constructed by
  `build_command()`; there is no code path that can issue a mutating CCI API
  call.
- Filter/selector values are read data and are deliberately not scanned, so a
  legitimate filter such as `--name restart-me` still works.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `CCI`.
- **Operation name** — PascalCase Kubernetes operation id: `ListCoreV1Namespace`,
  `ListCoreV1PodForAllNamespaces`, `ListCoreV1NamespacedPod`,
  `ListAppsV1DeploymentForAllNamespaces`, `ListAppsV1NamespacedDeployment`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete CCI call).
- **Simple parameter** — `--key=value`, e.g. `--namespace=default`,
  `--limit=100`, `--labelSelector=app=web`, `--fieldSelector=status.phase=Running`.
- **REST paths (official CCI API reference)** —
  `GET /api/v1/namespaces`, `GET /api/v1/pods`,
  `GET /api/v1/namespaces/{namespace}/pods`,
  `GET /apis/apps/v1/deployments`,
  `GET /apis/apps/v1/namespaces/{namespace}/deployments`.
- **Paging** — `--limit` + `--continue` (the script follows the response
  `metadata.continue` token until the list is exhausted).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty resource list | Exit 0, prints `当前区域（<x>）无 CCI 资源（resource=<x>）` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问云容器实例（CCI），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1, hint to install KooCLI (CCI has no Python SDK fallback) |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud CCI <Operation> --help` |
| `--page-size` out of range (not 1–1000) | Exit 1, explicit range error before any call |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`Running` pods / non-`Active` namespaces | Reported with their phase (`Pending`, `Creating`, ...), not treated as failure |
| `--name` | Applied client-side (case-insensitive substring) — the list APIs have no name query parameter |
| `--label-selector` / `--field-selector` | Forwarded as real Kubernetes server-side query parameters |
| Large resource count | Automatic continue-token paging driven by `metadata.continue` (max 100 pages) |
| Pod / Deployment without `--namespace` | Uses the cluster-wide `...ForAllNamespaces` operation |
| Extra response fields | The table renders the union of the normalized key fields — new fields appear automatically |
| Field missing on an object | Rendered as `-` in the table |
| Container images / labels | Flattened into comma-joined cells for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| User asks to create/delete/exec | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / patch / replace /
exec / scale / drain / normalized variants / operation whitelist / resource
mismatch / filter-value stripping), command construction (cluster-wide vs
namespaced routing, region, limit, continue token, no write flags ever), JSON
extraction, continue-token paging, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc=0, hcloud not installed), client-side name
filter, normalization (namespace / pod / deployment), rendering (table / names /
fallbacks) and all main() output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential and skill-quality-cli configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |