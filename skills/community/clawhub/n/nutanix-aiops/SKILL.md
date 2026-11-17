---
name: nutanix-aiops
slug: nutanix-aiops
displayName: "Nutanix AIops"
summary: "Governed Nutanix Prism Central v4 ops: clusters/VMs/storage/DR/LCM/RCA, ETag-safe, 51 tools."
license: MIT
homepage: https://github.com/AIops-tools/Nutanix-AIops
tags: [aiops, mcp, governance, nutanix]
description: >
  Use this skill whenever the user needs to operate a Nutanix estate through Prism Central (v4 REST API) — an estate/cluster health overview, cluster & host inventory and utilization, VM lifecycle across AHV and ESXi (list/get/power/create/update/clone/delete/migrate), storage containers, subnets/network, images & categories, data protection / DR (snapshots, recovery points, protection domains, VM protect, failover), alerts & events with alert RCA (analyze_alert), LCM firmware/software upgrades, capacity runway forecasting, and read-only diagnostics/RCA over the whole estate (cluster_health_rca, alert_triage_rca).
  Always use this skill for "Nutanix", "Prism Central", "AHV", "cluster health", "list VMs", "power on/off a VM", "clone/migrate a VM", "delete a VM", "snapshot", "recovery point", "protection domain", "failover", "why did this alert fire" / "root cause this alert", "LCM upgrade / firmware", "days until storage is full" / "capacity runway", "what's wrong with my cluster" / "diagnose the estate", "triage my alerts", when the context is a Nutanix cluster or Prism Central.
  Do NOT use when the target is a non-Nutanix platform — those belong to their own AIops-tools sibling; this skill is Prism Central v4 only.
  Governed Nutanix Prism Central operations with a built-in governance harness (audit, token budget, undo, descriptive risk-tier labels).
installer:
  kind: uv
  package: nutanix-aiops
argument-hint: "[VM/cluster extId or describe your Nutanix task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["nutanix-aiops","uvx"]},"optional":{"env":["NUTANIX_AIOPS_CONFIG","NUTANIX_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Nutanix-AIops","emoji":"🧊","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed Nutanix Prism Central operations. The governance harness (audit, token/runaway budget, undo, descriptive risk-tier labels) is bundled in the package — no external skill-family dependency.
  Connects to Prism Central on HTTPS :9440 with HTTP Basic auth (username + password). The v4 REST API requires an ETag/If-Match on every mutation; nutanix-aiops fetches and sends it automatically. All list tools paginate automatically; vm_list returns both AHV and ESXi VMs.
  All write operations are audited to a local SQLite DB under ~/.nutanix-aiops/ (relocatable via NUTANIX_AIOPS_HOME).
  Credentials: the Prism Central password is stored ENCRYPTED in ~/.nutanix-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'nutanix-aiops init' to onboard, or 'nutanix-aiops secret set <target>' to add one. The store is unlocked by a master password from NUTANIX_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var NUTANIX_<TARGET_NAME_UPPER>_PASSWORD is still honoured as a fallback with a deprecation warning (migrate with 'nutanix-aiops secret migrate'). The account needs REST API rights, not just Web UI access.
  State-changing operations require the @governed_tool decorator (budget guard + audit + risk-tier tagging). The skill does not decide whether a write is permitted — that is the agent's judgement or the connecting account's permissions. High-risk ops (vm_delete, vm_migrate, storage_container_delete, subnet_delete, snapshot_delete, snapshot_restore, pd_failover, image_delete, lcm_update) support dry_run and, at the CLI, double confirmation; reversible writes record an undo descriptor (vm_update → prior CPU/memory, vm_migrate → prior host).
  NUTANIX_AUDIT_APPROVED_BY and NUTANIX_AUDIT_RATIONALE are optional annotations recorded on the audit row (who/why); they are never required and never block a call.
  SSL: verify_ssl defaults to true; disable only for self-signed lab / Community Edition certificates.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Validation status: behaviour is currently validated against mocked v4 REST responses; the LCM update, PD failover, and ESXi-VM listing paths in particular still need live verification (self-testable free on Nutanix Community Edition + X-Small Prism Central). See docs/VERIFICATION.md in the repo for the live-verification checklist.
---

# Nutanix AIops

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by Nutanix.** Product and trademark names belong to their owners. Source at [github.com/AIops-tools/Nutanix-AIops](https://github.com/AIops-tools/Nutanix-AIops) under the MIT license.

Governed Nutanix **Prism Central (v4 REST API)** operations — **51 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.nutanix-aiops/`, token/runaway budget guard, undo-token recording, and descriptive risk-tier labels. The Prism Central password is stored **encrypted** (`~/.nutanix-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

**What sets it apart** from read-only Nutanix MCPs: (1) automatic **ETag / If-Match** on every mutation — the v4 footgun handled for you; (2) automatic **pagination**; (3) **mixed-hypervisor** VM listing (AHV + ESXi, relevant to hypervisor-migration estates); and (4) the governance harness with **dry-run + double-confirm** on destructive writes.

> **Standalone**: the governance harness is bundled in the package (`nutanix_aiops.governance`) — no external skill-family dependency.

## What This Skill Does

| Group | Tools | Count | Read / Write |
|-------|-------|:-----:|:------------:|
| **Clusters** | cluster_list, cluster_health, host_list, cluster_utilization | 4 | 4 read |
| **VMs** | list, get, power_on, guest_shutdown, power_off, reboot, create, update, clone, delete, migrate | 11 | 2 read · 9 write |
| **Storage** | container list / create / update / delete | 4 | 1 read · 3 write |
| **Network** | subnet list / get / create / delete | 4 | 2 read · 2 write |
| **Catalog** | image list / delete, category list / create / assign | 5 | 2 read · 3 write |
| **Data protection / DR** | snapshot list/create/delete/restore, recovery_point_list, protection_domain_list, vm_protect, pd_failover | 8 | 3 read · 5 write |
| **Alerts** | alert_list, event_list, audit_list, **analyze_alert (RCA)**, alert_acknowledge, alert_resolve | 6 | 4 read · 2 write |
| **LCM (upgrades)** | lcm_inventory, lcm_precheck, lcm_update | 3 | 1 read · 2 write |
| **Capacity** | task_list, capacity_runway | 2 | 2 read |
| **Diagnostics / RCA** | **cluster_health_rca**, **alert_triage_rca** | 2 | 2 read |
| **Undo** | `undo_list`, `undo_apply` | 2 | 1 read · 1 write |
| **Total** | | **51** | 24 read · 27 write |

The CLI is a convenience subset; the full 51-tool surface is via the MCP server. See `references/capabilities.md` for the tool → API-path → returns map.

## Quick Install

```bash
uv tool install nutanix-aiops
nutanix-aiops init       # interactive wizard: PC host/port 9440/username + encrypted password
nutanix-aiops doctor     # connectivity + REST-RBAC preflight
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/nutanix-aiops
openclaw skills info nutanix-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Diagnose the estate in one shot (`diagnose cluster-health`): degraded resiliency, storage pools/containers over 80% / 90%, nodes down or missing — worst-first, each finding citing the measured number
- Triage the alert backlog (`diagnose alert-triage`): per-severity counts, unacknowledged criticals, the oldest unresolved alert and its age
- Inspect the estate (`overview`, `cluster health`, `cluster util`): clusters, hosts, resiliency, utilization
- VM lifecycle across **AHV + ESXi** (`vm list/get/power/create/update/clone`), and guarded destructive ops (`vm delete`, `vm migrate`) with dry-run + double-confirm
- Root-cause an alert (`analyze_alert`) — correlate it with related events into a probable-cause + suggested-actions summary
- Data protection: snapshots, recovery points, protection domains, `vm_protect`, `pd_failover`
- Upgrades (`lcm_inventory` → `lcm_precheck` → `lcm_update`) and capacity forecasting (`capacity_runway`)

**Do NOT use when** the target is a non-Nutanix platform — this skill is Prism Central v4 only. For other infrastructure, use the appropriate **other AIops-tools** sibling.

## Common Workflows

### "Something is wrong with the estate" → diagnose, then act

1. `nutanix-aiops diagnose cluster-health` → worst-first findings, e.g.
   `critical · prod-cluster · storage container near full · 93.0% used >= 90.0% threshold`
2. `storage_container_list` → confirm which container it is and what its
   `maxCapacityBytes` / `logicalUsageBytes` actually are
3. `recovery_point_list` / `snapshot_list <vm_ext_id>` → the usual culprit is
   snapshot sprawl in that container
4. `snapshot_delete <…> --dry-run` to preview, then re-run to reclaim space —
   optionally set `NUTANIX_AUDIT_APPROVED_BY` first to annotate who authorized
   it; each deletion is audited and records an undo descriptor
5. Re-run `diagnose cluster-health` → the finding should drop below the 80%
   warning threshold; the before/after percentages are your evidence

### Triage a cluster alert (RCA)

1. `nutanix-aiops diagnose alert-triage` (or `alert_list`) → per-severity counts and the oldest unresolved alert, so you know which extId to open first
2. `analyze_alert <alert_ext_id>` → probable cause + suggested actions, built by correlating the alert with related `event_list` records
3. Confirm blast radius with `cluster_health` / `cluster_utilization`, then `alert_acknowledge` (or `alert_resolve` once fixed)

### Safely delete a VM (high-risk, audited)

1. `vm_get <vm_ext_id>` → confirm it's the right VM (and see its ETag)
2. `nutanix-aiops vm delete <vm_ext_id> --dry-run` → preview the exact `DELETE` call
3. Optionally annotate who/why: `export NUTANIX_AUDIT_APPROVED_BY=… NUTANIX_AUDIT_RATIONALE=…`
4. Re-run without `--dry-run` (double-confirm at the CLI); the call is audited with
   tier and any approver/rationale supplied

### Snapshot sprawl cleanup

1. `recovery_point_list` (or per-VM `snapshot_list <vm_ext_id>`) → find stale / redundant snapshots
2. `snapshot_delete <…> --dry-run` on each candidate → preview
3. Re-run without dry-run (HIGH risk, double-confirm at the CLI) to reclaim space; each deletion is audited

### Capacity runway

1. `cluster_utilization <cluster_ext_id>` → current CPU / memory / storage / IOPS
2. `capacity_runway` → days-to-full forecast per resource; use it to schedule an `lcm` expansion or storage add before you hit the wall

### Migrate a VM to another host (reversible)

1. `host_list` → pick the destination host extId
2. `nutanix-aiops vm migrate <vm_ext_id> <target_host_ext_id> --dry-run` → preview
3. Re-run without dry-run (HIGH, double-confirm); the **prior host is captured as an undo descriptor** so a regression can be reversed

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide whether a write is
permitted. That is your agent's judgement, or the permission of the account you connect it with
(connect with a Prism Central account holding only a read-only (Viewer) role — writes then fail
at the server). There is no read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.nutanix-aiops/audit.db` (relocatable via `NUTANIX_AIOPS_HOME`): params, result, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `NUTANIX_AUDIT_APPROVED_BY` / `NUTANIX_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `NUTANIX_RUNAWAY_MAX=0`.
- Every mutation auto-handles **ETag / If-Match**; every list auto-paginates.
- Destructive writes support `dry_run` / `--dry-run` and, at the CLI, double confirmation.
- Reversible writes record an undo descriptor (`vm_update` → prior CPU/memory, `vm_migrate` → prior host).

## References

- `references/capabilities.md` — full 51-tool + API-path reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, REST-RBAC, CE self-test
- `references/agent-guardrails.md` — which guardrails the harness enforces for you, and a ready-to-paste system prompt for smaller / local models
</content>
