---
name: olvm-aiops
slug: olvm-aiops
displayName: "OLVM AIops"
summary: "Governed OLVM / oVirt 4.5 ops — 18 MCP tools: inventory, health, capacity, diagnosis; audited."
license: MIT
homepage: https://github.com/AIops-tools/OLVM-AIops
tags: [aiops, mcp, governance, olvm, ovirt]
description: >
  Use this skill whenever the user needs to inspect or troubleshoot an Oracle Linux Virtualization Manager (OLVM) or oVirt 4.5 environment through its engine — data centers, clusters, KVM hosts, storage domains, VMs, events and jobs; and one-call diagnoses that rank what needs attention in the engine itself — health check, clock, certificates, backups (engine_health_rca) — on hosts (host_health_rca), storage domains (storage_capacity_rca) and VMs (vm_health_rca).
  Always use this skill for "olvm", "oracle linux virtualization manager", "ovirt engine", "rhv manager", "host non operational", "storage domain inactive", "storage domain low space", "vm paused", "vm not responding", "engine certificate expiring", "engine backup", or "what failed in olvm" when the context is an OLVM / oVirt engine.
  Do NOT use for XCP-ng — use xcpng-aiops. Do NOT use for Proxmox VE — use proxmox-aiops. Other hypervisors, NAS appliances, backup suites and container clusters are out of scope (negative routing hints only).
  Read-only in this release, with a built-in governance harness (audit, token budget, risk tiers).
installer:
  kind: uv
  package: olvm-aiops
argument-hint: "[host / storage domain / VM name or describe your OLVM task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["olvm-aiops","uvx"]},"optional":{"env":["OLVM_AIOPS_CONFIG","OLVM_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/OLVM-AIops","emoji":"🖥️","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed operations for Oracle Linux Virtualization Manager 4.5 and upstream oVirt 4.5 engines over the engine REST API (/ovirt-engine/api). Talks to the engine only; no direct host (vdsm) access. The official Python SDK is not used (it needs pycurl built from source); runtime dependencies are httpx, the MCP SDK, typer, rich, pyyaml and cryptography. The governance harness (audit, token/runaway budget, risk tiers) is bundled in the package — no external skill-family dependency.
  Every call is audited to a local SQLite DB under ~/.olvm-aiops/ (relocatable via OLVM_AIOPS_HOME).
  Credentials: each engine target's account password is stored ENCRYPTED in ~/.olvm-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'olvm-aiops init' to onboard, or 'olvm-aiops secret set <target>' to add one. The store is unlocked by a master password from OLVM_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt. The password is exchanged for an SSO token held only in memory and revoked when the connection closes. A legacy plaintext env var OLVM_<TARGET_NAME_UPPER>_PASSWORD is still honoured as a fallback with a deprecation warning.
  The username must include its profile: admin@internal on an engine without Keycloak, admin@ovirt@internalsso where engine-setup enabled Keycloak (the default since 4.5.1). For least privilege, connect a user holding a read-only role such as ReadOnlyAdmin.
  Writes: none in this release. Every tool is a read or a diagnosis.
  Webhooks: none — no outbound network calls beyond the configured engine URL.
  SSL: verify_ssl defaults to true; set ca_file to the engine CA (https://<engine>/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA) and use the engine's FQDN, whose certificate does not cover its IP.
  Verification status: every read and all four diagnoses were run against a live Oracle Linux Virtualization Manager 4.5.5-1.73.el9 engine (Keycloak enabled) with one KVM host, an NFS data domain and a VM; tests use payloads captured from it. A user has since run the read-only tools against a small production engine with 8 hosts and an FC data domain, matching the engine's own API, and repeated it under a ReadOnlyAdmin account with every read and all four diagnoses working. Not yet verified on iSCSI/Gluster domains, on self-hosted engine deployments, on engines without Keycloak, or past the scan limits (1000 objects). See docs/VERIFICATION.md.
---

# OLVM AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by Oracle or the oVirt project.** "Oracle", "Oracle Linux" and "oVirt" are trademarks of their owners. Source code is publicly auditable at [github.com/AIops-tools/OLVM-AIops](https://github.com/AIops-tools/OLVM-AIops) under the MIT license.

Governed operations for **Oracle Linux Virtualization Manager (OLVM)** and **oVirt 4.5** through the engine REST API — **18 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local audit log under `~/.olvm-aiops/`, a token/runaway budget guard, and descriptive risk tiers. The engine password is stored **encrypted** (`~/.olvm-aiops/secrets.enc`) — never plaintext on disk.

> **Read-only in this release.** Inventory, health, capacity and diagnosis. Engine actions are asynchronous — the engine answers `complete` long before a VM or host reaches its target state — so write tools are held back until each can confirm its own outcome.

## What This Skill Does

| Area | Tools |
|---|---|
| Diagnosis (start here) | `engine_health_rca`, `host_health_rca`, `storage_capacity_rca`, `vm_health_rca` |
| Inventory | `datacenter_list`, `cluster_list`, `host_list`, `host_get`, `storage_domain_list`, `storage_domain_get`, `vm_list`, `vm_get`, `vm_stats` |
| Activity | `event_list`, `job_list` |
| Governance | `undo_list`, `undo_apply` (nothing records an undo in this read-only release) |

Each diagnosis returns findings ranked worst first. Every finding carries `signal` (what was measured, quoted from the engine), `cause`, `action` and `rank`.

## Quick Install

```bash
uv tool install olvm-aiops
olvm-aiops init       # interactive wizard: engine URL, username with profile, CA, encrypted password
olvm-aiops doctor     # login + engine product version
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/olvm-aiops
openclaw skills info olvm-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- "Is anything wrong with my OLVM / oVirt environment?"
- A host is non-operational, non-responsive or stuck installing.
- A storage domain is inactive, low on space, or the engine refuses to create disks.
- A VM is paused, not responding, or will not start.
- "What happened in the last hour?" / "Follow new events."
- Capacity questions: how full each storage domain is, what is over-committed.

## Related Skills — Skill Routing

| The target is… | Use |
|---|---|
| An OLVM or oVirt 4.5 engine | **olvm-aiops** (this skill) |
| An XCP-ng pool | xcpng-aiops |
| A Proxmox VE cluster | proxmox-aiops |

## Common Workflows

### 1. "Is anything wrong right now?"

1. `engine_health_rca`, then `host_health_rca`, then `storage_capacity_rca`, then `vm_health_rca`.
2. Report findings in `rank` order and quote each `signal`. Severity `info` means in progress or superseded — a host the engine is rebooting after deployment, an old event the host or VM has since recovered from — and `low` means it is not a fault of the object the finding is on — alert 9000 on a host without fencing hardware, or a guest-agent call that failed on a healthy host. A `low` finding can still carry work: read its `action`.
3. For context on a finding, `event_list` with `min_severity="warning"`, and `job_list` with `status="failed"`.

### 2. "Storage is filling up" / "the engine won't create a disk"

1. `storage_capacity_rca` — `critical` means free space is below the domain's critical blocker, and the engine refuses new disks and snapshots there.
2. `storage_domain_list` for free %, used and committed bytes of every domain.
3. `vm_list` to see which VMs live in the cluster that uses the domain.

### 3. "This VM is paused / not responding"

1. `vm_health_rca` — paused VMs point at storage first; an event is superseded when the VM started or was reported back up after it; events older than `events_window_hours` (default 24) are ignored.
2. `vm_get` and `vm_stats` for the VM's host, memory and CPU.
3. `event_list` with `since_minutes=60` for what the engine logged around it.
4. `storage_capacity_rca` if the VM is paused.

### 4. "Tell me what changes from now on"

1. `event_list` once and note the highest `index`.
2. Next time, `event_list` with `after_index` set to that number — the events after it come back oldest first; repeat with the highest index returned while `truncated` is true.

### 5. "Will certificates or backups bite us?"

1. `engine_health_rca` — engine and CA certificate expiry, missing or failed engine backups, clock skew, the engine's own health check.
2. `host_health_rca` — host certificate expiry and time drift, per host.

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models | **CLI** | fewer tokens than MCP |
| Cloud models (Claude, GPT) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | type-safe parameters, audited |

## MCP Tools (18 — 16 read, 2 undo)

| Tool | What it answers |
|---|---|
| `engine_health_rca` | Engine problems ranked: health check, clock skew, engine/CA certificate expiry, engine backups, cluster HA reservation, data-center status |
| `host_health_rca` | Host problems ranked: broken states with status detail, reinstall/update flags, host certificate expiry, host events. A failed guest-agent call (event 10802, a `VmLogon`/`VmLogoff` command) is a guest condition, not a host fault: `low`, with `vmCandidates` — the VMs the engine reports on that host. Every 10802 finding reports one vdsm command (its `cause` names it, and only the guest-agent one is downgraded) and carries `relatedVmEvents`, the VM-level failures the engine logged beside it. Both lists are candidates to check, never the affected VM |
| `storage_capacity_rca` | Storage problems ranked: critical blocker, low space, over-commit, inactive attached domains, storage events |
| `vm_health_rca` | VM problems ranked: stuck, paused, image locked, HA VMs down, pending config restarts, VM events |
| `datacenter_list` | Data centers, status, compatibility version |
| `cluster_list` | Clusters, compatibility version, CPU type, memory over-commit |
| `host_list` / `host_get` | Hosts: status, SPM role, memory, VM counts (engine search supported) |
| `storage_domain_list` / `storage_domain_get` | Domains: data-center-scoped status, free/used/committed bytes and % |
| `vm_list` / `vm_get` | VMs: status, host, vCPUs, memory, HA, start/stop time; `vm_list` supports engine search and `page`/`nextPage` |
| `vm_capacity_summary` | Compact engine-wide VM/vCPU count and vCPU-to-host-core assignment; `complete` and `snapshotConsistent` state the limits |
| `vm_stats` | A VM's current memory, CPU %, network and disk statistics with units |
| `event_list` | Events newest first: severity threshold, `page`, `after_index` cursor (oldest first), `since_minutes` |
| `job_list` | Jobs newest first, optional status filter |
| `undo_list` / `undo_apply` | Harness undo log (empty in this read-only release) |

Any listing with a `limit` returns `returned`, `limit` and a measured `truncated`. A field the engine did not report is `null`, never an invented 0.
For a full VM walk, call `vm_list` with `limit=20` and the same `search` while
following `nextPage` to `null`. Do not ask for one giant page: an MCP client may
clip the response before the model sees all VMs or `nextPage`. If any page or its
continuation metadata is clipped or missing, do not calculate a fleet total or
ranking from the visible subset. `total` is `null`; the engine's stateless pages
cannot prove a single consistent snapshot if VMs change during the walk.
For fleet counts or assignment ratio, prefer `vm_capacity_summary` so the VM
rows do not enter the model context. Quote its totals only when `complete` is
true; even then, `snapshotConsistent=false` means it is not an atomic snapshot.

## CLI Quick Reference

```bash
olvm-aiops engine health                   # engine findings: health check, clock, certificates, backups
olvm-aiops host health                     # host findings, worst first
olvm-aiops storage capacity                # storage findings, worst first
olvm-aiops vm health                       # VM findings, worst first
olvm-aiops host list --search 'status!=up'
olvm-aiops storage list
olvm-aiops vm list --search 'status=up'
olvm-aiops vm list --limit 100 --page 2 --json
olvm-aiops vm capacity --json
olvm-aiops vm stats <vm-id>
olvm-aiops event list --min-severity warning --since-minutes 60
olvm-aiops event list --after-index 1234
olvm-aiops job list --status failed
olvm-aiops datacenter list
olvm-aiops cluster list
olvm-aiops doctor
```

Add `--json` to any list or diagnosis for the full payload. See `references/cli-reference.md`.

## Troubleshooting

### "Config file not found"
Run `olvm-aiops init`, or create `~/.olvm-aiops/config.yaml` with a `targets` list.

### "No password for target '<name>'"
Store it with `olvm-aiops secret set <name>`.

### "Master password not set" / "Wrong master password"
Export `OLVM_AIOPS_MASTER_PASSWORD` for non-interactive use, or run the CLI on a terminal to be prompted.

### "Engine SSO login failed … Cannot authenticate user"
The username must include its profile. On an engine where setup enabled Keycloak (the default since 4.5.1) the admin is `admin@ovirt@internalsso`; without Keycloak it is `admin@internal`.

### "TLS verification failed … IP address mismatch"
The engine answered, but its certificate names the engine's FQDN, not its IP. Use the FQDN in `url` and point `ca_file` at the engine CA — this is not a connectivity fault.

### "… timed out after 30s"
The engine accepted the connection but did not answer in time. Raise `timeout` for the target in `config.yaml`.

### "Could not connect to … within 30s"
Nothing answered the connection attempt: the engine is down, a firewall drops the port, or `url` names the wrong host. A longer `timeout` will not help.

### "Not retried: the last login failed …"
A login was refused less than 60 s ago, so the tool waits instead of trying again — repeated attempts with a wrong password can lock the engine account. Fix the stored password (`olvm-aiops secret set <target>`) and retry after the wait.

### "Not authorized (403)"
The account is valid but its role does not cover the object. Grant a role (for read-only use, `ReadOnlyAdmin`) in the Administration Portal.

### "Not found (404)"
The id is stale — list the parent collection again.

## Audit & Safety

The skill reads and records; it does **not** decide what an agent may change. That belongs to the engine account you connect it with — give it a read-only role and the engine itself refuses anything else.

- **Audit is the guarantee, and it is not bypassable.** Every call — MCP and CLI alike — is logged to `~/.olvm-aiops/audit.db` (relocatable via `OLVM_AIOPS_HOME`): params (secrets redacted), outcome summary, status, duration, and the risk tier.
- The engine password is stored **encrypted** in `~/.olvm-aiops/secrets.enc` (Fernet/AES-128 + scrypt key derivation; chmod 600); the master password is never stored. The SSO token is held only in memory and revoked when the connection closes.
- SSO session ids that the engine prints in login events are redacted before any event text is returned.
- **Budget / runaway guard** — a safety backstop, not authorization: caps cumulative tool calls and wall-time, and trips on tight polling loops.
- **Risk tier** is a descriptive label on the audit row derived from `risk_level`; it gates nothing.

The harness is bundled in the package — no external dependency, no manual setup. See `references/setup-guide.md` for security details.

## Contributing & feature requests

Coverage is intentionally focused. **Missing a capability you need, or seeing an engine answer differently from what this tool expects?** Open an issue or pull request at [github.com/AIops-tools/OLVM-AIops](https://github.com/AIops-tools/OLVM-AIops/issues) — feature requests, contributions, and comments are all welcome.

## License

MIT — [github.com/AIops-tools/OLVM-AIops](https://github.com/AIops-tools/OLVM-AIops)
