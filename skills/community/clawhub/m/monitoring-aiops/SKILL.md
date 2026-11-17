---
name: monitoring-aiops
slug: monitoring-aiops
displayName: "SolarWinds / PRTG / Zabbix Operations"
summary: "Governed SolarWinds Orion + PRTG + Zabbix ops: SWQL, alert rollup, health, 42 tools."
license: MIT
homepage: https://github.com/AIops-tools/Monitoring-AIops
tags: [aiops, mcp, governance, monitoring]
description: >
  Use this skill whenever the user needs to operate a network / infrastructure monitoring NOC on SolarWinds Orion (SWIS REST + SWQL), Paessler PRTG (web API), or Zabbix 6.x/7.x (JSON-RPC) — a one-shot NOC overview, canned SWQL answers (nodes down, flapping interfaces, muted, high-CPU nodes, full volumes, unmanaged/scheduled), a validated read-only SWQL passthrough, deduped/rolled-up active alerts, SolarWinds node/interface/volume/application health and top-N, PRTG sensors/devices/groups/history/alarms, Zabbix problems/hosts/host-groups/triggers/events/item-history/maintenances, and guarded writes (acknowledge, mute/unmute, schedule maintenance, unmanage/remanage, remove node, pause/resume sensor, create/delete Zabbix maintenance window).
  Always use this skill for "SolarWinds", "Orion", "SWQL", "THWACK question", "PRTG", "Paessler", "Zabbix", "Zabbix problem", "Zabbix trigger", "Zabbix maintenance", "NOC overview", "which nodes are down", "flapping interfaces", "interface flap storm", "alert storm", "acknowledge this alert", "worst CPU nodes", "top-N by latency/packet loss", "which volumes are full", "muted alerts report", "unmanaged nodes", "schedule a maintenance window", "unmanage / remanage a node", "pause a PRTG sensor" when the context is monitoring.
  Do NOT use when the target is something other than a SolarWinds/PRTG/Zabbix monitoring platform (a hypervisor, storage appliance, backup product, Kubernetes cluster, network device config, or OT/industrial equipment) — route those to the appropriate other AIops-tools skill.
  Governed monitoring operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). PRTG's free Freeware edition and an open-source Zabbix appliance are the easiest live checks; SolarWinds is trial-only past 30 days.
installer:
  kind: uv
  package: monitoring-aiops
argument-hint: "[node/sensor id, a SWQL question, or describe your NOC task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["monitoring-aiops","uvx"]},"optional":{"env":["MONITORING_AIOPS_CONFIG","MONITORING_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Monitoring-AIops","emoji":"📡","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed monitoring operations across SolarWinds Orion (SWIS REST + SWQL, port 17774 on Orion 2023.1+ with an automatic one-shot fallback to the legacy 17778, HTTP Basic auth), Paessler PRTG (web API, port 443/8080, API token), and Zabbix 6.x/7.x (JSON-RPC 2.0 at /api_jsonrpc.php, API token as Bearer header on 6.4+/7.x with a legacy auth-field fallback for 6.0). Each target in the config names its own platform, so one config can span all NOCs. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.monitoring-aiops/ (relocatable via MONITORING_AIOPS_HOME).
  Credentials: the Orion account password (SolarWinds), the PRTG API token, or the Zabbix API token is stored ENCRYPTED in ~/.monitoring-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'monitoring-aiops init' to onboard (it asks for the platform), or 'monitoring-aiops secret set <target>' to add one. The store is unlocked by a master password from MONITORING_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var MONITORING_<TARGET_NAME_UPPER>_SECRET is still honoured as a fallback with a deprecation warning (migrate with 'monitoring-aiops secret migrate'). The secret is used for HTTP Basic auth (SolarWinds) or as the PRTG/Zabbix API token at request time and held only in memory; secrets are never logged or echoed.
  Read-only SWQL passthrough (swql_query) is validated to accept SELECT statements only. State-changing operations pass through the @governed_tool decorator (budget guard + audit + undo recording; each tool's risk_level is recorded as a descriptive tier, not a gate). Destructive writes (unmanage_node, remove_node, zabbix_delete_maintenance) are high-risk with dry_run + double confirmation; unmanage_node records an inverse remanage undo descriptor, zabbix_delete_maintenance captures the window's FULL definition into priorState first. Suppression/maintenance writes are TIME-BOXED (mute_alerts, schedule_maintenance, schedule_maintenance_prtg, zabbix_create_maintenance require an end time / duration). mute_alerts→unmute, pause_sensor→resume, zabbix_create_maintenance→delete-that-maintenance-id record inverse undo descriptors. Zabbix item history is BOUNDED (capped window + point count).
  Webhooks: none — no outbound network calls beyond the configured SolarWinds SWIS / PRTG web API / Zabbix JSON-RPC endpoint.
  SSL: verify_ssl defaults to false-friendly for self-signed lab certs; enable for production.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Validation status: behaviour is exercised against mocked SWIS/PRTG/Zabbix responses; not yet run against a live NOC (see docs/VERIFICATION.md). PRTG has a free perpetual 100-sensor Freeware edition with the API, and Zabbix is fully open source (a Docker-compose appliance is a 10-minute live check) — the easiest live checks; SolarWinds is a 30-day trial (mock-only past that — largest verification debt).
---

# Monitoring AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by SolarWinds, Paessler, Zabbix, or any monitoring vendor.** SolarWinds, Orion, SWQL, THWACK, PRTG, Paessler and Zabbix are trademarks of their respective owners. Source at [github.com/AIops-tools/Monitoring-AIops](https://github.com/AIops-tools/Monitoring-AIops) under the MIT license.

Governed network / infrastructure monitoring operations — **42 MCP tools**
across **SolarWinds Orion** (SWIS REST + SWQL), **Paessler PRTG** (web API),
and **Zabbix 6.x/7.x** (JSON-RPC 2.0),
every one wrapped with the bundled `@governed_tool` harness: a local unified
audit log under `~/.monitoring-aiops/`, policy engine, token/runaway budget
guard, undo-token recording, and risk-tier labelling on the audit trail. One
config can span all NOCs. The Orion password / PRTG API token / Zabbix API token is stored
**encrypted** (`~/.monitoring-aiops/secrets.enc`, Fernet + scrypt) — never
plaintext on disk.

> **Standalone**: the governance harness is bundled in the package
> (`monitoring_aiops.governance`) — no external skill-family dependency.
> PRTG's free Freeware edition and an open-source Zabbix appliance are the
> easiest live checks; SolarWinds is trial-only past 30 days (largest
> verification debt — see `docs/VERIFICATION.md`).

## What This Skill Does

| Group | Platform | Tools | Count | R/W |
|-------|----------|-------|:-----:|:---:|
| **SWQL** | SolarWinds | library, canned, query (SELECT-only passthrough) | 3 | read |
| **Alerts** | all | active_alerts (dedup/rollup), alert_acknowledge | 2 | 1 read, 1 write |
| **SolarWinds health** | SolarWinds | node/nodes/interface/volume/application status, topn, noc_rollup | 7 | read |
| **SolarWinds writes** | SolarWinds | list_events/unmanaged/muted | 3 | read |
| | SolarWinds | mute/unmute, schedule_maintenance, remanage_node | 4 | write (med) |
| | SolarWinds | unmanage_node, remove_node | 2 | write (**high**) |
| **PRTG** | PRTG | sensors/sensor_details/devices/groups/history/system_status/alarms | 7 | read |
| **PRTG writes** | PRTG | pause_sensor, resume_sensor, schedule_maintenance_prtg | 3 | write (med) |
| **Zabbix** | Zabbix | zabbix_problems/hosts/hostgroups/triggers/events/item_history/maintenances | 7 | read |
| **Zabbix writes** | Zabbix | zabbix_create_maintenance (time-boxed; undo = delete that id) | 1 | write (med) |
| | Zabbix | zabbix_delete_maintenance (priorState = full definition) | 1 | write (**high**) |
| **Undo** | all | undo_list, undo_apply | 2 | undo |

The canned SWQL library (`swql_library` lists them) answers the most-repeated
THWACK questions directly: `nodes_down`, `flapping_interfaces`, `muted_report`,
`high_cpu_nodes`, `volumes_full`, `unmanaged_scheduled`. For anything else,
`swql_query` is a validated read-only (SELECT-only) SWQL passthrough.

## Quick Install

```bash
uv tool install monitoring-aiops
monitoring-aiops init       # wizard: pick platform (solarwinds/prtg/zabbix) + encrypted secret
monitoring-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/monitoring-aiops
openclaw skills info monitoring-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Get a NOC snapshot (`overview` / `noc_rollup`): active/unacked alert counts,
  down/warning nodes, worst CPU
- Answer a repeated SWQL question (`swql_library` → `swql_canned nodes_down`), or
  run an ad-hoc read-only SWQL SELECT (`swql_query`)
- Triage an alert storm (`active_alerts` dedup/rollup collapses flap/down
  storms), then `alert_acknowledge`
- SolarWinds health: `node_status`, `interface_status` (top-N by util),
  `volume_status`, `application_status` (SAM), `topn` (cpu/mem/latency/loss)
- PRTG: list `prtg_sensors` / `prtg_devices` / `prtg_groups`, drill with
  `prtg_sensor_details` / `prtg_history`, check `prtg_alarms` / `prtg_system_status`
- Zabbix: triage `zabbix_problems` (0-5 severity mapped to levels) /
  `zabbix_triggers`, inventory `zabbix_hosts` / `zabbix_hostgroups`, drill with
  `zabbix_item_history` (bounded), review `zabbix_events` / `zabbix_maintenances`
- Safely take a node out for maintenance (`schedule_maintenance` /
  `unmanage_node` with dry_run + double-confirm), pause a PRTG sensor
  (`pause_sensor`), or create a time-boxed Zabbix maintenance window
  (`zabbix_create_maintenance` — undo deletes exactly that window)

**Do NOT use when** the target is not a SolarWinds/PRTG/Zabbix monitoring
platform — route hypervisor, storage, backup, cluster, network-device-config,
or OT/industrial work to the appropriate other AIops-tools skill.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| SolarWinds Orion / SWQL, PRTG, or Zabbix monitoring ops | **monitoring-aiops** (this skill) |
| A non-monitoring platform (hypervisor, storage, backup, cluster, network config, OT edge) | the appropriate **other AIops-tools** skill |
| Other monitoring stacks (not SolarWinds/PRTG/Zabbix) | out of scope for this tool |

## Common Workflows

> **No authorization gate**: the skill runs the operations you ask for and audits every one; it does not decide whether a write is permitted — that is the agent's judgement or the permissions of the SolarWinds/PRTG/Zabbix account it connects with (a read-only monitoring account makes writes fail at the server). There is no read-only switch, policy file, or approval gate. `MONITORING_AUDIT_APPROVED_BY` / `MONITORING_AUDIT_RATIONALE` are optional audit annotations, recorded when set.

### 1. The 3 a.m. alert storm — collapse it, then acknowledge what matters

1. `monitoring-aiops doctor` → confirm the NOC platform is actually reachable
   (a "storm" is sometimes just a poller that lost the target)
2. `monitoring-aiops overview` → the one-screen picture: down/warning counts
   across the configured targets
3. `monitoring-aiops alert list` (MCP: `active_alerts`) → deduped / rolled-up
   entries; an interface-flap or node-down storm collapses into **one** entry
   with a count instead of a wall of alerts
4. `noc_rollup` → confirm whether the storm has a single upstream cause (one
   node down taking its children with it) rather than N independent faults
5. Acknowledge only the rolled-up entry that matters:
   `monitoring-aiops alert ack <alert-id>` (SolarWinds `AlertActive.Acknowledge`
   / PRTG `acknowledgealarm` / Zabbix `event.acknowledge`) — the prior ack state
   is captured into priorState, and the ack is double-confirmed
6. **Failure branch**: if `doctor` fails, do **not** acknowledge anything — you
   would be silencing alerts you cannot currently see. Fix credentials with
   `monitoring-aiops secret set <target>` first. If you acknowledged the wrong
   alert, `monitoring-aiops undo list` → `undo apply <id>` restores the prior
   ack state.

### 2. "Which nodes are down and what's saturated?" (read-only)

1. `noc_rollup` → down / warning counts plus the worst-CPU nodes in a single
   call, so you do not page through a dashboard
2. `topn cpu` (also `memory`, `latency`, `packetloss`) → the worst offenders
   with the measured number
3. `node_status <node>` → drill into one node; `interface_status` for a
   suspected link problem, `volume_status` for a filling disk,
   `application_status` for an app-layer fault
4. `list_events` → what changed around the time things went bad
5. `list_unmanaged` → check whether a "missing" node is simply unmanaged from a
   previous maintenance window that was never reverted
6. **Failure branch**: if a node shows down but is reachable from your shell,
   the fault is in polling, not the node — check `list_muted` and
   `list_unmanaged` before escalating to the network team.

### 3. Planned maintenance: suppress noise time-boxed, then restore

1. `node_status <node>` / `swql_canned nodes_down` → confirm you have the right
   node and that it is currently healthy (so you can tell the difference
   afterwards)
2. Prefer the **time-boxed** path — it expires on its own:
   `schedule_maintenance <node> --end ...` (SolarWinds),
   `schedule_maintenance_prtg` (PRTG), or `zabbix_create_maintenance` (Zabbix,
   undo → delete that maintenance id)
3. If you genuinely need to unmanage instead:
   `unmanage_node <node> --dry-run`, then re-run without `--dry-run` →
   **high** risk, double confirmation; it records an inverse `remanage_node`
   undo descriptor
4. For a single noisy sensor rather than a whole node: `pause_sensor` (PRTG,
   undo → `resume_sensor`) or `mute_alerts` (undo → `unmute_alerts`)
5. When maintenance ends: `remanage_node <node>` / `resume_sensor` /
   `unmute_alerts`, or simply `monitoring-aiops undo apply <id>` to replay the
   recorded inverse
6. **Failure branch**: the classic failure here is *forgetting to restore* —
   run `list_unmanaged` and `list_muted` at the end of every maintenance window;
   anything still listed is silently unmonitored. Time-boxed maintenance windows
   are preferred precisely because they fail safe.

### 4. Answer a bespoke NOC question with SWQL

1. `monitoring-aiops swql library` (MCP: `swql_library`) → the canned queries,
   so you do not hand-write what already exists
2. `monitoring-aiops swql canned nodes_down` → run a canned one directly
   (also `high_cpu_nodes` and the rest of the library)
3. Not canned? `monitoring-aiops swql query "SELECT ..."` → the passthrough
   **validates the statement is a read-only SELECT** before it runs; anything
   else is refused
4. Feed the result into an action — e.g. a node the query surfaced goes into
   workflow 3 for a maintenance window
5. **Failure branch**: a rejected query is almost always a non-SELECT statement
   or a SWQL/SQL dialect slip (SWQL has no `*` expansion on some entities).
   Start from the nearest canned query in `swql library` and modify it rather
   than writing from scratch. The passthrough will not be talked into a write —
   writes go through the governed tools, where they are audited.

## Governance & Safety

- Every tool is audited to `~/.monitoring-aiops/audit.db` (relocatable via
  `MONITORING_AIOPS_HOME`).
- Each tool's `risk_level` is carried into the audit row as a descriptive tier
  (a label, not a gate). `MONITORING_AUDIT_APPROVED_BY` /
  `MONITORING_AUDIT_RATIONALE` are optional audit annotations, recorded when set.
- Destructive writes support `--dry-run` and double confirmation at the CLI.
- Suppression / maintenance writes are **time-boxed** (require an end time /
  duration). Reversible writes record an inverse descriptor (mute→unmute,
  unmanage→remanage, pause→resume, zabbix_create_maintenance→delete that
  maintenance id). `zabbix_delete_maintenance` captures the window's full
  definition into priorState before deleting.

## References

- `references/capabilities.md` — full tool + platform + SWQL/API-path reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
