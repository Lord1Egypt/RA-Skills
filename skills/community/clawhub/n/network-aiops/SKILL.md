---
name: network-aiops
slug: network-aiops
displayName: "Network AIops"
summary: "Governed network device ops (NAPALM) — 33 MCP tools with audit/undo."
license: MIT
homepage: https://github.com/AIops-tools/Network-AIops
tags: [aiops, mcp, governance, network]
description: >
  Use this skill whenever the user needs to operate a network device — read device facts, interfaces (+ counters/IP), BGP/LLDP neighbors (summary and detail), ARP/MAC tables, VLANs, routes, hardware environment (fans/temp/power/CPU/mem), optics, NTP, users, SNMP info, VRFs, and an aggregated device-health summary; run read-only RCA diagnostics on interface health and BGP neighbors; back up a switch/router config, diff a candidate config (dry-run), and merge/replace/rollback config — across Cisco IOS/IOS-XE, Nexus NX-OS, IOS-XR, Arista EOS, and Juniper Junos via NAPALM. An optional NetBox block adds source-of-truth lookups.
  Always use this skill for "back up switch config", "show bgp neighbors", "diff network config", "push config to router", "show interfaces on the switch", or tasks mentioning "cisco", "arista", "juniper", "nexus", "ios-xr", or "napalm".
  Do NOT use when the target is not a NAPALM-supported network device (Kubernetes clusters, hypervisor VMs, and cloud consoles are out of scope — route those elsewhere).
  Common multi-vendor device operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers).
installer:
  kind: uv
  package: network-aiops
argument-hint: "[device name or describe your network task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["network-aiops","uvx"]},"optional":{"env":["NETWORK_AIOPS_CONFIG","NETWORK_AIOPS_HOME","NETWORK_AIOPS_MASTER_PASSWORD","NETWORK_NETBOX_TOKEN"]},"homepage":"https://github.com/AIops-tools/Network-AIops","emoji":"🛜","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed network device operations over NAPALM. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.network-aiops/ (relocatable via NETWORK_AIOPS_HOME).
  Credentials: device login passwords AND the optional NetBox API token live in an ENCRYPTED store at ~/.network-aiops/secrets.enc (Fernet/AES + scrypt-derived key; chmod 600), never in plaintext. Device passwords are keyed by the device name; the NetBox token uses the reserved name "netbox-token". Unlock with the NETWORK_AIOPS_MASTER_PASSWORD env var (for the MCP server / non-interactive use) or an interactive prompt. Run `network-aiops init` (wizard) or `network-aiops secret set <name>` to populate it, and `network-aiops secret migrate` to import a legacy plaintext .env (NETWORK_<TARGET_UPPER>_PASSWORD / NETWORK_NETBOX_TOKEN are still honoured as a deprecated fallback). config.yaml holds only device names, drivers, hosts, usernames, and NAPALM optional_args — never secrets. The state dir ~/.network-aiops should be chmod 700.
  Destructive operations (config merge, config replace, config rollback) require double confirmation at the CLI layer and support --dry-run (which prints the diff without committing). All write tools pass through the @governed_tool decorator (budget guard + audit + risk-tier tagging). config_merge and config_replace capture the pre-change running config and record an inverse config_replace-to-backup undo descriptor; config_rollback records none, and config_replace is risk_level=high.
  Webhooks: none — no outbound network calls beyond the configured device sessions and the optional NetBox API.
  TLS: NAPALM driver transports (eAPI/NX-API HTTPS, NETCONF/SSH) follow the device's own certificate/SSH host-key settings; the skill does not weaken them.
  Transitive dependencies: napalm (device drivers), pynetbox (optional source-of-truth), typer/rich (CLI), pyyaml/python-dotenv (config), and the MCP SDK. No post-install scripts or background services.
---

# Network AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by Cisco, Arista, Juniper, NetBox Labs, or any network vendor.** Vendor and product names are trademarks of their respective owners. Source code is publicly auditable at [github.com/AIops-tools/Network-AIops](https://github.com/AIops-tools/Network-AIops) under the MIT license.

Governed multi-vendor network device operations — **33 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.network-aiops/`, token/runaway budget guard, undo-token recording, and descriptive risk-tier labels. Devices are reached over NAPALM; an optional NetBox block adds source-of-truth lookups. Secrets (device passwords + NetBox token) are kept in an **encrypted store** (`secrets.enc`), unlocked by `NETWORK_AIOPS_MASTER_PASSWORD`.

> **Standalone**: the governance harness is bundled in the package (`network_aiops.governance`) — network-aiops has no external skill-family dependency. Coverage focuses on common operations and is not yet exhaustive.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|----------|-------|:-----:|:-------------:|
| **Device facts** | facts, interfaces, interface counters, interface IPs, BGP (+detail), LLDP (+detail), ARP | 9 | 9 read |
| **Inventory** | MAC table, VLANs, route lookup | 3 | 3 read |
| **Platform / env** | environment, optics, NTP servers, NTP stats, users, SNMP info, VRFs, device_health | 8 | 8 read |
| **Diagnostics / RCA** | interface_health_rca, bgp_neighbor_rca | 2 | 2 read |
| **Config** | backup, diff (dry-run), merge, replace, rollback | 5 | 2 read / 3 write |
| **NetBox** | list devices, get device, device interfaces | 3 | 3 read |
| **Undo** | undo_list, undo_apply | 2 | 1 read / 1 write |

## Quick Install

```bash
uv tool install network-aiops
network-aiops init            # interactive wizard: device + driver + host + encrypted password (+ optional NetBox)
network-aiops doctor          # checks config, encrypted secret store, and per-device password presence
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/network-aiops
openclaw skills info network-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

`init` writes `~/.network-aiops/config.yaml` and stores secrets **encrypted** in `~/.network-aiops/secrets.enc`. Export `NETWORK_AIOPS_MASTER_PASSWORD` in your shell profile so the CLI and MCP server can unlock secrets non-interactively.

## Supported Devices

| Platform | NAPALM driver | Transport |
|----------|---------------|-----------|
| Cisco IOS / IOS-XE | `ios` | SSH |
| Cisco Nexus NX-OS | `nxos` (NX-API) / `nxos_ssh` (SSH) | HTTPS / SSH |
| Cisco IOS-XR | `iosxr` | SSH (XML agent) |
| Arista EOS | `eos` | eAPI (HTTPS) |
| Juniper Junos | `junos` | NETCONF (SSH) |

Other platforms (Nokia SR OS / SR Linux, Huawei VRP, etc.) are reachable via NAPALM **community drivers** but are **not officially tested here** — see [Contributing](#contributing--request-a-device-or-feature).

## When to Use This Skill

- Inspect device facts, interfaces (+ counters/IP), BGP/LLDP neighbors (summary + detail), ARP/MAC tables, VLANs, and route lookups
- Check hardware health: environment (fans/temp/power/CPU/mem), optics, NTP, users, SNMP info, VRFs, or a one-shot `device_health` summary
- Root-cause a problem with read-only RCA: `interface_health_rca` (down/erroring/discarding/flapping ports) and `bgp_neighbor_rca` (down/shut/recently-reset/route-less peers) — each finding cites the measured number that tripped it, worst-first
- Back up a switch/router running config to a file
- Dry-run a config change as a diff before committing
- Merge a config snippet, replace the full config, or roll back the last commit
- Cross-check intended state in NetBox before pushing a change

**Do NOT use when** the target is not a NAPALM-supported network device (Kubernetes clusters, hypervisor VMs, and cloud-provider consoles are out of scope for this skill).

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Network device config / facts (Cisco/Arista/Juniper) | **network-aiops** (this skill) |
| Kubernetes cluster operations | a cluster ops skill |
| Hypervisor VM lifecycle (power, snapshot, migrate) | a hypervisor ops skill |

## Supported Actions

| Tool | R/W | Risk | Driver support |
|------|:---:|:----:|----------------|
| `device_facts` | R | low | all 5 |
| `get_interfaces` | R | low | all 5 |
| `get_interfaces_counters` | R | low | all 5 |
| `get_interfaces_ip` | R | low | all 5 |
| `get_bgp_neighbors` | R | low | all 5 (varies by feature) |
| `get_bgp_neighbors_detail` | R | low | ios/eos/junos/iosxr; nxos varies |
| `get_lldp_neighbors` | R | low | all 5 |
| `get_lldp_neighbors_detail` | R | low | all 5 |
| `get_arp_table` | R | low | all 5 |
| `get_mac_address_table` | R | low | all 5 (varies by image) |
| `get_vlans` | R | low | eos/junos/nxos; ios varies |
| `get_route_to` | R | low | all 5 (varies by feature) |
| `get_environment` | R | low | all 5 (sensor coverage varies) |
| `get_optics` | R | low | eos/junos/iosxr; ios/nxos varies |
| `get_ntp_servers` | R | low | all 5 |
| `get_ntp_stats` | R | low | all 5 |
| `get_users` | R | low | all 5 (password hashes redacted) |
| `get_snmp_information` | R | low | all 5 (community strings redacted) |
| `get_network_instances` | R | low | eos/junos/iosxr; ios/nxos varies |
| `device_health` | R | low | all 5 (environment section optional) |
| `interface_health_rca` | R | low | all 5 (needs get_interfaces + counters) |
| `bgp_neighbor_rca` | R | low | all 5 (varies by BGP feature) |
| `config_backup` | R | low | all 5 |
| `config_diff` (dry-run) | R | low | all 5 |
| `config_merge` | W | medium | all 5 |
| `config_replace` | W | **high** | ios/eos/junos/iosxr; nxos varies |
| `config_rollback` | W | medium | device-dependent rollback depth |
| `netbox_list_devices` | R | low | NetBox (optional) |
| `netbox_get_device` | R | low | NetBox (optional) |
| `netbox_device_interfaces` | R | low | NetBox (optional) |

**Per-driver caveat**: NAPALM does not implement every getter on every platform. Any unsupported getter returns a teaching error ("not supported by the `<driver>` driver") instead of crashing — try a different getter or fall back to `config_backup`. `device_health` is resilient: if a driver lacks `get_environment` that section is reported as a note, not a failure.

**Credentials**: `get_users` reduces password hashes to a boolean and `get_snmp_information` reduces community strings to a count — those two never return secrets at all. `config_backup` and every returned `diff` *mask* credential values (password/secret hashes, SNMP communities, pre-shared keys, RADIUS/TACACS and keychain keys) and report how many lines they changed in a `redaction` block; `include_secrets=True` returns the verbatim text. The masking is pattern-based across five vendor syntaxes, so it reduces exposure rather than guaranteeing none remains — notably it cannot see multi-line PKI key blocks. To hand a real config to a human, prefer the CLI's `-o <path>`, which writes raw to a file instead of into this transcript.

## Common Workflows

### Safely change a device config with a dry-run first

1. `network-aiops config backup -t core-sw1 -o core-sw1.cfg` → keep a known-good copy
2. `network-aiops config diff change.cfg -t core-sw1` → preview the diff (nothing committed)
3. `network-aiops config merge change.cfg -t core-sw1` (double confirm) → commits **under a 300s device-side revert timer**; the harness also records a `config_replace`-to-backup undo descriptor
4. `network-aiops device interfaces -t core-sw1` → verify the result **and that you can still reach the device**
5. `network-aiops config confirm -t core-sw1` → cancels the revert timer, making the change permanent. If you skip this (or get locked out), the device reverts by itself — that is the point
6. **Failure branch**: if the connection fails (`Could not connect/authenticate`), run `network-aiops doctor` — it shows whether `NETWORK_CORE_SW1_PASSWORD` is set and whether the host/port is reachable; the skill never retries a denied auth.

### Change something that could lock you out (mgmt interface, VTY ACL, AAA)

1. `network-aiops config backup -t core-sw1 -o core-sw1.cfg` → an off-box copy, independent of the tool
2. `network-aiops config diff risky.cfg -t core-sw1` → confirm the diff touches only what you intend
3. `network-aiops config merge risky.cfg -t core-sw1 --revert-in 120` → short timer: if the change severs your session, the device restores itself in 2 minutes with nobody logged in
4. Re-connect and verify. **Do not confirm from a session opened before the commit** — it may survive a change that blocks *new* logins
5. `network-aiops config confirm -t core-sw1` → only once a NEW session proves the path still works
6. **Failure branch**: if the result carries `commit.warning` with `safetyNet: "undo-only"`, this driver could not arm a timer. The change is permanent on landing and the recorded undo needs a working session — arrange out-of-band access (console/OOB mgmt) before you commit anything of this kind.

### Root-cause a flaky uplink / peering problem (RCA-first)

1. `network-aiops diagnose interface-health -t edge-rtr` → worst-first interface findings; a link that is admin-up/oper-down with climbing `rx_errors+tx_errors` and a recent `last_flapped` is a physical-layer fault (cable/optic), each cited with its measured value
2. `network-aiops diagnose bgp -t edge-rtr` → worst-first neighbor findings; if the peer riding that link shows `BGP session down` or `recently reset` (low uptime), the L1 fault — not routing — is resetting the session
3. `network-aiops device counters -t edge-rtr` → confirm the error counters are still climbing before you touch anything
4. `network-aiops config diff fix.cfg -t edge-rtr` → dry-run the remediation first, then `config merge` (double confirm) through the audited path
5. **Failure branch**: if `interface_health_rca` / `bgp_neighbor_rca` returns "not supported by the `<driver>` driver", the platform's NAPALM driver lacks the underlying getter — fall back to `device facts` / `config_backup` and request the getter via a GitHub issue.

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models | **CLI** | fewer tokens than MCP |
| Cloud models (Claude, GPT) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | type-safe parameters, audited |

## MCP Tools (33 — 28 read, 5 write)

| Category | Tools | R/W |
|----------|-------|:---:|
| Facts | `device_facts`, `get_interfaces`, `get_interfaces_counters`, `get_interfaces_ip`, `get_bgp_neighbors`, `get_bgp_neighbors_detail`, `get_lldp_neighbors`, `get_lldp_neighbors_detail`, `get_arp_table` | Read |
| Inventory | `get_mac_address_table`, `get_vlans`, `get_route_to` | Read |
| Platform / env | `get_environment`, `get_optics`, `get_ntp_servers`, `get_ntp_stats`, `get_users`, `get_snmp_information`, `get_network_instances`, `device_health` | Read |
| Diagnostics / RCA | `interface_health_rca`, `bgp_neighbor_rca` | Read |
| Config | `config_backup`, `config_diff` | Read |
| | `config_merge`, `config_replace`, `confirm_commit`, `config_rollback` | Write |
| NetBox | `netbox_list_devices`, `netbox_get_device`, `netbox_device_interfaces` | Read |
| Undo | `undo_list` | Read |
| | `undo_apply` | Write |

**Commit-confirm is the primary safety net.** `config_merge` and `config_replace` commit with a device-side revert timer (`revert_in`, default 300s): the device rolls the change back on its own unless `confirm_commit` follows. This is the only guard that survives the change severing your own management path — a commit that shuts the management interface, tightens the VTY ACL or breaks AAA also kills the session the recorded undo would need, so the *device* has to be the one enforcing the rollback. Workflow: **commit with timer → verify you can still reach the device → `confirm_commit`** (or do nothing and let it revert). Drivers that cannot arm a timer fall back to a plain commit and say so in `commit.warning` / `commit.safetyNet` — check that field, because for those devices the net is absent.

**Harness features that light up**: `config_merge` and `config_replace` capture the pre-change running config and pass an `undo=` lambda so the harness records an inverse descriptor (with `_undo_id`) that restores the captured config via `config_replace` — the device must support config replace for the undo to apply. The raw config is handed to the harness out-of-band and kept only in `undo.db` (0600); the tool result returns a **digest** (size + SHA-256), never the config body, because a running config carries credential hashes, SNMP communities and PSKs that would otherwise land in the agent transcript. `config_rollback` declares no undo; `config_replace` is tagged `risk_level=high`. `config_diff` is a pure dry-run (stage candidate → compare → discard). The two RCA tools (`interface_health_rca`, `bgp_neighbor_rca`) are pure read-only analyses (`risk_level=low`) that collect getter output and rank findings worst-first. All 33 tools are audit-logged under `~/.network-aiops/` and pass through the budget/runaway guard, with a descriptive risk tier tagged on each audit row. Avoid tight poll loops — the runaway breaker backs this up.

## Encrypted secret store

Secrets never touch disk in plaintext. They live in `~/.network-aiops/secrets.enc` (Fernet/AES-128 + HMAC, key derived from a master password via scrypt; file chmod 600). Both kinds of secret share the one store: per-device login passwords keyed by device name, and the single NetBox API token keyed by the reserved name `netbox-token`.

```bash
network-aiops init                       # wizard: collects devices + passwords (encrypted), optional NetBox
network-aiops secret set core-sw1        # store/replace a device password (hidden prompt)
network-aiops secret set netbox-token    # store the NetBox API token
network-aiops secret list                # names only — values are NEVER printed
network-aiops secret rm core-sw1
network-aiops secret migrate             # import a legacy plaintext .env (renamed to .env.migrated)
network-aiops secret rotate-password     # re-encrypt the whole store under a new master password
```

Unlock non-interactively by exporting `NETWORK_AIOPS_MASTER_PASSWORD` (used by the MCP server / cron / CI). Legacy plaintext env vars (`NETWORK_<TARGET_UPPER>_PASSWORD`, `NETWORK_NETBOX_TOKEN`) are still honoured as a deprecated fallback with a warning. An empty device password is allowed (valid for key-based SSH auth via `optional_args`).

## CLI Quick Reference

```bash
network-aiops init                                               # onboarding wizard (encrypted secrets)
network-aiops device facts [-t <device>]
network-aiops device interfaces [-t <device>]
network-aiops device counters [-t <device>]
network-aiops device bgp [-t <device>]
network-aiops device lldp [-t <device>]
network-aiops device arp [-t <device>]
network-aiops device mac [-t <device>]
network-aiops device vlans [-t <device>]
network-aiops device route <prefix> [-t <device>] [--protocol bgp]
network-aiops device environment [-t <device>]
network-aiops device health [-t <device>]
network-aiops diagnose interface-health [-t <device>]           # interface RCA (worst-first)
network-aiops diagnose bgp [-t <device>]                        # BGP-neighbor RCA (worst-first)
network-aiops config backup [-t <device>] [-o <file>]
network-aiops config diff <file> [-t <device>] [--replace]
network-aiops config merge <file> [-t <device>] [--dry-run]      # double confirm
network-aiops config replace <file> [-t <device>] [--dry-run]    # HIGH RISK
network-aiops config rollback [-t <device>] [--dry-run]          # double confirm
network-aiops netbox list [--name <q>] [--limit N]
network-aiops netbox get <name>
network-aiops netbox interfaces <device> [--limit N]
network-aiops secret set|list|rm|migrate|rotate-password
network-aiops doctor
network-aiops mcp                                                # start MCP server (stdio)
```

See `references/cli-reference.md` for the full command list.

## Troubleshooting

### "Could not connect/authenticate to '<device>'"
The host/port, username, or password is wrong, or the device is unreachable. Run `network-aiops doctor` — it reports whether the encrypted secret store is present, whether a password is stored for the device, and whether the device answers. Store/replace the password with `network-aiops secret set <device>` (or re-run `network-aiops init`). For enable/secret, set it in `optional_args.secret`.

### "Master password not set" / cannot unlock secrets
The encrypted store needs the master password. Export `NETWORK_AIOPS_MASTER_PASSWORD` for non-interactive use (MCP server / cron), or run a CLI command on a TTY to be prompted. If you forgot it, delete `~/.network-aiops/secrets.enc` and re-run `network-aiops init`.

### "Operation not supported by the '<driver>' NAPALM driver"
That getter or config mode is not implemented for this platform. Try a different getter, or fall back to `config_backup` and inspect the relevant stanza. Request the capability via a GitHub issue/PR.

### "Driver '<x>' is not in the officially supported set"
Only `ios`, `nxos`, `nxos_ssh`, `iosxr`, `eos`, `junos` are tested here. Community drivers may work but are untested — request official support via a GitHub issue/PR.

### NetBox commands fail with "NetBox is not configured"
Add a `netbox: {url: ...}` block to `config.yaml` and store the API token encrypted with `network-aiops secret set netbox-token` (or run `network-aiops init`). NetBox tools degrade gracefully when unconfigured.

### `config replace` failed mid-commit
The device may not support full config replace (some Nexus images do not). Use `config merge` for additive changes, or restore from your `config backup` file.

## Audit & Safety

The skill delivers reads and writes and records them; it does **not** decide whether a write is permitted. That is your agent's judgement, or the permission of the account you connect it with (log in with a device account at a read-only privilege level, and give NetBox a read-only API token — writes then fail at the server). There is no read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.network-aiops/audit.db` (relocatable via `NETWORK_AIOPS_HOME`): params, outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `NETWORK_AUDIT_APPROVED_BY` / `NETWORK_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `NETWORK_RUNAWAY_MAX=0`.
- Undo store records inverse descriptors for reversible writes (config merge/replace → restore captured running config).
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI.

The harness is bundled in the package — no external dependency, no manual setup. See `references/setup-guide.md` for security details.

Driving these tools with a smaller / local model? See `references/agent-guardrails.md` — which guardrails the harness now enforces for you, a ready-to-paste system prompt, and the network-specific traps (config merge vs replace, per-vendor interface naming, NetBox intent vs live device state).

## Contributing — request a device or feature

Coverage is intentionally focused. **Need a device (Nokia SR OS, Huawei VRP, …) or an action that isn't here yet?** Open an issue or pull request at [github.com/AIops-tools/Network-AIops](https://github.com/AIops-tools/Network-AIops/issues) — feature requests, contributions, and comments are all welcome.

## License

MIT — [github.com/AIops-tools/Network-AIops](https://github.com/AIops-tools/Network-AIops)
