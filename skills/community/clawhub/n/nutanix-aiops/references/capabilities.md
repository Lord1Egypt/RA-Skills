# nutanix-aiops capabilities

> **51 MCP tools** (24 read, 27 write) over the Nutanix
> **Prism Central v4 REST API** (HTTPS :9440, HTTP Basic auth). Every mutation
> handles **ETag / If-Match** automatically; every list is **paginated**
> automatically. Paths below are the v4 API prefixes actually called; validate
> against a live Prism Central / Community Edition before production use.

## Clusters (4 read)

| Tool | API path | Returns |
|------|----------|---------|
| `cluster_list` | `GET /api/clustermgmt/v4.0/config/clusters` | extId, name, AOS version, hypervisors, node count |
| `cluster_health` | `GET /api/clustermgmt/v4.0/config/clusters/{extId}` | services, resiliency / fault-tolerance, upgrade state |
| `host_list` | `GET /api/clustermgmt/v4.0/config/hosts` | host extId, cluster, hypervisor, CPU / memory |
| `cluster_utilization` | `GET /api/clustermgmt/v4.0/config/clusters/{extId}` | point-in-time CPU / memory / storage / IOPS |

## VMs (2 read, 9 write) — base `GET /api/vmm/v4.0/ahv/config/vms`

| Tool | Risk | API path | Returns / undo |
|------|------|----------|----------------|
| `vm_list` | read | `GET …/vms` (paginated) | VMs across **AHV + ESXi** (extId, name, cluster, power, vCPU, mem, hypervisor) |
| `vm_get` | read | `GET …/vms/{extId}` | one VM, **surfaces its ETag** for downstream mutations |
| `vm_power_on` | write · low | `POST …/vms/{extId}/$actions/power-on` | task ref |
| `vm_guest_shutdown` | write · med | `POST …/vms/{extId}/$actions/shutdown` | graceful guest shutdown |
| `vm_power_off` | write · med | `POST …/vms/{extId}/$actions/power-off` | hard power off |
| `vm_reboot` | write · med | `POST …/vms/{extId}/$actions/reboot` | task ref |
| `vm_create` | write · med | `POST …/vms` | new VM extId |
| `vm_update` | write · med | `PUT …/vms/{extId}` (If-Match) | **undo captures prior CPU / memory** |
| `vm_clone` | write · med | `POST …/vms/{extId}/$actions/clone` | clone extId |
| `vm_delete` | write · **HIGH** | `DELETE …/vms/{extId}` | **dry_run**; double-confirm at CLI |
| `vm_migrate` | write · **HIGH** | `POST …/vms/{extId}/$actions/migrate` | **dry_run**; **undo → prior host** |

## Storage (1 read, 3 write) — base `GET /api/clustermgmt/v4.0/config/storage-containers`

| Tool | Risk | API path | Returns / undo |
|------|------|----------|----------------|
| `storage_container_list` | read | `GET …/storage-containers` | extId, name, cluster, capacity, usage |
| `storage_container_create` | write · med | `POST …/storage-containers` | new container extId |
| `storage_container_update` | write · med | `PUT …/storage-containers/{extId}` (If-Match) | **undo captures prior config** |
| `storage_container_delete` | write · **HIGH** | `DELETE …/storage-containers/{extId}` | **dry_run** |

## Network (2 read, 2 write) — base `GET /api/networking/v4.0/config/subnets`

| Tool | Risk | API path | Returns / undo |
|------|------|----------|----------------|
| `subnet_list` | read | `GET …/subnets` | extId, name, type, VLAN, IP config |
| `subnet_get` | read | `GET …/subnets/{extId}` | one subnet, **surfaces ETag** |
| `subnet_create` | write · med | `POST …/subnets` | new subnet extId |
| `subnet_delete` | write · **HIGH** | `DELETE …/subnets/{extId}` | **dry_run** |

## Catalog (2 read, 3 write)

| Tool | Risk | API path | Returns / undo |
|------|------|----------|----------------|
| `image_list` | read | `GET /api/vmm/v4.0/content/images` | image extId, name, type, size |
| `image_delete` | write · **HIGH** | `DELETE /api/vmm/v4.0/content/images/{extId}` | **dry_run** |
| `category_list` | read | `GET /api/prism/v4.0/config/categories` | key, value, extId |
| `category_create` | write · low | `POST /api/prism/v4.0/config/categories` | new category extId |
| `category_assign` | write · med | `POST …/categories/{extId}/$actions/associate` | **bulk-assign** a category to many VMs |

## Data protection / DR (3 read, 5 write)

| Tool | Risk | API path | Returns / undo |
|------|------|----------|----------------|
| `snapshot_list` | read | `GET …/vms/{extId}` recovery points | per-VM snapshots (extId, name, created) |
| `recovery_point_list` | read | `GET /api/dataprotection/v4.0/config/recovery-points` | recovery points across estate |
| `protection_domain_list` | read | `GET /api/dataprotection/v4.0/config/protection-policies` | protection policies / domains |
| `snapshot_create` | write · low | `POST …/vms/{extId}` recovery point | new snapshot extId |
| `snapshot_delete` | write · **HIGH** | `DELETE …/recovery-points/{extId}` | **dry_run** |
| `snapshot_restore` | write · **HIGH** | `POST …/$actions/restore` | **dry_run** |
| `vm_protect` | write · med | `POST …/protection-policies` associate | attach a VM to a protection policy |
| `pd_failover` | write · **HIGH** | `POST …/$actions/failover` | **dry_run** |

## Alerts (4 read, 2 write)

| Tool | Risk | API path | Returns |
|------|------|----------|---------|
| `alert_list` | read | `GET /api/monitoring/v4.0/serviceability/alerts` | active alerts (severity, impact, source) |
| `event_list` | read | `GET /api/monitoring/v4.0/serviceability/events` | recent events |
| `audit_list` | read | `GET /api/prism/v4.0/config/audits` | Prism audit records |
| `analyze_alert` | read | correlates alert + related events | **RCA (flagship read)** — probable cause + suggested actions |
| `alert_acknowledge` | write · low | `POST …/alerts/{extId}/$actions/acknowledge` | ack a live alert |
| `alert_resolve` | write · low | `POST …/alerts/{extId}/$actions/resolve` | resolve a live alert |

## LCM — upgrades (1 read, 2 write)

| Tool | Risk | API path | Returns |
|------|------|----------|---------|
| `lcm_inventory` | read | `GET /api/lifecycle/v4.0/resources/entities` | firmware / software entities + available versions |
| `lcm_precheck` | write · medium | `POST /api/lifecycle/v4.0/resources/$actions/perform-precheck` | precheck task ref |
| `lcm_update` | write · **HIGH** | `POST /api/lifecycle/v4.0/resources/$actions/perform-update` | **firmware/software update**; **dry_run**; **refused unless `precheck_task_ext_id` names a precheck task that reached SUCCEEDED** |

## Capacity (2 read)

| Tool | API path | Returns |
|------|----------|---------|
| `task_list` | `GET /api/prism/v4.0/config/tasks` | recent Prism tasks (status, entity, progress) |
| `capacity_runway` | derived from cluster utilization | **days-to-full forecast** per resource |

## Diagnostics / RCA (2 read)

Read-only signature analyses (`risk_level="low"`). Both are **pure and
deterministic** — no clock, no randomness — and every finding carries the
measured number or raw Prism state that tripped it, alongside a probable cause
and a concrete action. Findings are returned worst-first
(critical → warning → info) with the shape
`{severity, resource, signal, detail, cause, action}`.

| Tool | API paths read | Returns |
|------|----------------|---------|
| `cluster_health_rca` | `clusters` + `clusters/{extId}` + `hosts` + `storage-containers` | findings for degraded `faultToleranceState`, cluster storage pool and storage containers over **80% (warning) / 90% (critical)**, hosts whose `nodeStatus` is unhealthy, and clusters with fewer visible hosts than their `nodeCount`; plus a `summary` of every measured percentage |
| `alert_triage_rca` | `serviceability/alerts` | active (unresolved) alerts grouped by severity with a per-level count, unacknowledged criticals called out, and `oldestUnresolved` (title, severity, `ageDays`) — an alert open **≥ 7 days** is flagged stale |

`alert_triage_rca` is the fleet-level lens; `analyze_alert` is the per-alert
lens (event correlation on one alert's affected entity). They compose: triage
first to pick the extId, then analyze it.

## Undo (1 read, 1 write)

| Tool | Risk | Returns / effect |
|------|:----:|------------------|
| `undo_list` | low | recorded, not-yet-applied reversible writes — `undoId`, original tool, inverse tool, note |
| `undo_apply` | medium | executes a recorded inverse descriptor; itself governed and audited, single-use, supports `dry_run` |

## ETag / pagination / mixed hypervisor

- **ETag / If-Match** — the v4 API rejects an update or delete without the
  current entity's ETag. Every mutation here fetches the ETag and sends
  `If-Match` for you (the common v4 footgun); `vm_get` / `subnet_get` surface it
  for inspection.
- **Pagination** — all list tools follow `$page` / `$limit` and return the full
  set, not just page one.
- **Mixed hypervisor** — `vm_list` returns both **AHV** and **ESXi** VMs managed
  by the same Prism Central (relevant to hypervisor-migration estates).

## Out of scope (by design, this release)

- IAM / users / roles / SAML, Files / Objects / Volumes services
- Report generation, X-Play / playbooks, calm / self-service
- Anything outside Prism Central v4 (direct Prism Element, ncli/acli)

Want one of these? Open an issue or PR — feedback and contributions welcome.
</content>
</invoke>
