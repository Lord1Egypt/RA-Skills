# monitoring-aiops capabilities

> **42 MCP tools** (30 read, 10 write, 2 undo) across SolarWinds
> Orion (SWIS REST + SWQL, port 17774 with a legacy-17778 fallback, HTTP
> Basic auth), Paessler PRTG (web
> API, port 443/8080, API token), and Zabbix 6.x/7.x (JSON-RPC 2.0 at
> `/api_jsonrpc.php`, API token — Bearer header on 6.4+/7.x, legacy `auth`
> field fallback for 6.0). Each config target names its own `platform`.
> SWIS/PRTG/Zabbix responses are mocked and need live verification.

## SWQL — SolarWinds (read)

| Tool | SWQL / path | Returns |
|------|-------------|---------|
| `swql_library` | (local) | the catalogue of canned queries: `nodes_down`, `flapping_interfaces`, `muted_report`, `high_cpu_nodes`, `volumes_full`, `unmanaged_scheduled` |
| `swql_canned` | named SWQL → SWIS `/Query` | rows for the named canned query |
| `swql_query` | validated read-only SWQL → SWIS `/Query` | rows for a caller SELECT (SELECT-only; rejected otherwise) |

## Alerts — all platforms

| Tool | Risk | Path | Returns / effect |
|------|------|------|------------------|
| `active_alerts` | read | SWIS `AlertActive`/`AlertObjects`, PRTG `/api/table.json?content=messages`, or Zabbix `problem.get` | active alerts **deduped/rolled up by message** — flap/down storms collapse into one counted entry |
| `alert_acknowledge` | write **medium** | SW `AlertActive.Acknowledge` verb / PRTG `acknowledgealarm.htm` / Zabbix `event.acknowledge` (action 6; prior ack state → priorState) | acknowledges an alert / alarm / problem event |

## SolarWinds health (read)

| Tool | SWQL / path | Returns |
|------|-------------|---------|
| `node_status` | `Orion.Nodes` | one node's status, CPU/mem, response time |
| `nodes_list` | `Orion.Nodes` | node inventory (status, vendor, IP, last boot) |
| `interface_status` | `Orion.NPM.Interfaces` | top-N interfaces by utilisation (in/out, errors, oper status) |
| `volume_status` | `Orion.Volumes` | volumes by % used (node, volume, percentUsed), worst first; unreported usage listed in `unreadableVolumes` with `percentUsed: null` |
| `application_status` | `Orion.APM.Application` (SAM) | SAM application/component status |
| `topn` | `Orion.Nodes` metrics | top-N nodes by `cpu` / `memory` / `latency` / `packetloss` |
| `noc_rollup` | folds `Orion.Nodes` | down/warning counts + worst-CPU nodes in one call; a failed count is `null` with the reason in `countErrors` |

## SolarWinds writes

| Tool | Risk | Path / verb | Undo / safety |
|------|------|-------------|---------------|
| `list_events` | read | `Orion.Events` | recent events (read) |
| `list_unmanaged` | read | `Orion.Nodes` where Unmanaged | currently-unmanaged nodes (read) |
| `list_muted` | read | `Orion.AlertSuppression` | currently-muted objects (read) |
| `mute_alerts` | write **med** | `AlertSuppression` (SuppressAlerts) | **time-boxed** (requires end time); records inverse **unmute** undo |
| `unmute_alerts` | write **med** | `AlertSuppression` (ResumeAlerts) | un-suppresses alerting |
| `schedule_maintenance` | write **med** | `AlertSuppression` window | **requires an end time** (time-boxed maintenance window) |
| `unmanage_node` | write **HIGH** | `Orion.Nodes.Unmanage` verb | `dry_run` + double-confirm; captures prior managed state; records inverse **remanage** undo |
| `remanage_node` | write **med** | `Orion.Nodes.Remanage` verb | brings a node back under management |
| `remove_node` | write **HIGH** | SWIS `DELETE` on the node URI | `dry_run` + double-confirm; no undo (deletion is not reversible) |

## PRTG (read)

| Tool | Path | Returns |
|------|------|---------|
| `prtg_sensors` | `/api/table.json?content=sensors` | sensors (status, last value, message) |
| `prtg_sensor_details` | `/api/getsensordetails.json` | one sensor's detail (channels, uptime, last check) |
| `prtg_devices` | `/api/table.json?content=devices` | devices (host, group, status) |
| `prtg_groups` | `/api/table.json?content=groups` | probe/group tree with status rollups |
| `prtg_history` | `/api/historicdata.json` | historic values for a sensor over a window |
| `prtg_system_status` | `/api/status.json` | server/system status (also the PRTG `doctor` check) |
| `prtg_alarms` | `/api/table.json?content=messages` (alarms) | active PRTG alarms |

## PRTG writes

| Tool | Risk | Path | Undo / safety |
|------|------|------|---------------|
| `pause_sensor` | write **med** | `/api/pause.htm?action=0` | records inverse **resume** undo |
| `resume_sensor` | write **med** | `/api/pause.htm?action=1` | resumes a paused sensor |
| `schedule_maintenance_prtg` | write **med** | `/api/pauseobjectfor.htm?duration=` | **time-boxed** (requires minutes) |

## Zabbix (read)

| Tool | JSON-RPC method | Returns |
|------|-----------------|---------|
| `zabbix_problems` | `problem.get` | current problems; severity 0-5 mapped to names + canonical levels (`info`/`warning`/`high`/`critical`) |
| `zabbix_hosts` | `host.get` (+interfaces, +host groups) | host inventory: monitored flag, interfaces (ip/dns/availability), groups |
| `zabbix_hostgroups` | `hostgroup.get` | host groups (ids + names) |
| `zabbix_triggers` | `trigger.get` | triggers, by default only those currently firing (PROBLEM) |
| `zabbix_events` | `event.get` | recent trigger events (newest first, capped) |
| `zabbix_item_history` | `item.get` + `history.get` | **bounded** metric detail: item meta + history points (window ≤ 168 h, ≤ 500 points) |
| `zabbix_maintenances` | `maintenance.get` | maintenance windows with hosts/groups + periods |

## Zabbix writes

| Tool | Risk | JSON-RPC method | Undo / safety |
|------|------|-----------------|---------------|
| `zabbix_create_maintenance` | write **med** | `maintenance.create` | **time-boxed** (minutes > 0) + must name hosts/groups; records a **replayable undo** = delete exactly the created maintenance id |
| `zabbix_delete_maintenance` | write **HIGH** | `maintenance.delete` | `dry_run` + double-confirm; the window's **full definition** is captured into priorState first (no undo — re-create manually from it) |

## Out of scope (by design)

- Monitoring stacks other than SolarWinds Orion, PRTG, and Zabbix
- Zabbix template / discovery / user CRUD, `trend.get`, and host **onboarding**
- Creating alerts / thresholds / SWQL-view CRUD, and node/interface **onboarding**
- Anything outside monitoring (hypervisor, storage, backup, cluster, network
  device config, OT/industrial) — route to the appropriate other AIops-tools skill

Want one of these? Open an issue or PR — feedback and contributions welcome.
