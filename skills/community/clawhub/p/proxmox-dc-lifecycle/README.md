# Proxmox DC Lifecycle

Safely rebuild a Windows Active Directory **domain controller** that lives as a Proxmox VM — demote it, clean its metadata, reinstall the OS hands-off, and re-promote it — without corrupting Active Directory. Built from real DC rebuilds, with the failure modes that bit along the way written down.

Works standalone as an operational runbook, or as a knowledge base for AI coding agents (Claude Code, Claude Desktop, OpenClaw, Cursor, etc).

> **Prime directive: do not corrupt Active Directory.** Verify replication and FSMO before and after every step, rebuild one DC at a time, and never destroy a VM while AD still sees it as a domain controller.

## What's Inside

- **Full lifecycle** — demote → metadata cleanup → hands-off OS reinstall (autounattend) → rejoin → re-promote, each phase ending in a verification gate you must not cross until it's green
- **QGA execution model** — drive Windows guests from the Proxmox host with `qm guest exec` (no WinRM/PSRemoting between DCs, which fails); secrets passed over guest-agent **stdin**, never on a command line
- **Autounattend template** — Server Core, UEFI/GPT, virtio driver injection (viostor/vioscsi/NetKVM), static IP, guest-agent + WinRM enablement
- **Field-tested gotchas catalog** — DNS-delegation stalls, LDAP error 58 under SYSTEM, `0x80070008` heap exhaustion, NTDS-disabled / `ntds.dit`-missing diagnosis, orphaned-trust repair, edition-default trap, detached-execution pitfalls, and more — each with signature + fix
- **Operational safety gates** — read-only vs reversible vs destructive, with explicit operator-confirmation guidance before AD object deletion and disk wipes

## Requirements

- A Proxmox VE host you can run `qm` on with `sudo` (passwordless preferred)
- Windows guests with the **QEMU guest agent** installed and responding
- Windows Server evaluation ISO + a matching **virtio-win** ISO on a Proxmox storage
- Domain/Enterprise Admin credentials, supplied via guest-agent stdin (the skill never puts them on a command line)
- A secret manager **on a separate machine** for storing break-glass / rotated credentials (the Proxmox host intentionally has none)

## Setup

Fill in the environment config block at the top of `SKILL.md` for your fleet (domain, subnet/gateway/DNS, the DC names + VMIDs, ISO storage, bridge/VLAN). Everything downstream refers to those names rather than hardcoding — adapt that one block and change nothing else. Then confirm against live state (`qm config`, `qm list`, a query to a healthy DC) before acting.

## Quick Start (the lifecycle)

```text
Phase 0  Orient & baseline (read-only)   → repl 0 fails, FSMO where expected, target holds none
Phase 1  Snapshot the target VM          → qm snapshot <vmid> predemote_<date>
Phase 2  Demote the target DC            → graceful demote inside the guest via QGA
Phase 3  Metadata cleanup & verify       → no nTDSDSA for target; repl 0 fails  ← gate to touch the disk
Phase 4  Reinstall the OS (hands-off)    → autounattend; same VMID/MAC/IP        ← irreversible wipe; confirm first
Phase 5  Rejoin & re-promote             → replica DC; repl 0 fails incl. new DC
Phase 6  Finalize                        → detach media, clean up, then the next DC
```

Each phase has an explicit **gate** — do not proceed until it's green. See `SKILL.md` for the full flow and `references/` for the per-step scripts.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full reference — environment config, the lifecycle, gates, prime directive |
| `references/qga-execution.md` | The execution backbone — `qm guest exec` (and off-host REST API), secrets over stdin, `cmd` vs PowerShell, verifying installers by exit code |
| `references/verification.md` | Read-only health checks (FSMO, replication, dcdiag, SYSVOL/DFSR) |
| `references/demotion.md` | Graceful demotion + the LocalAdministratorPassword / RemoveDnsDelegation gotchas; forced-removal fallback |
| `references/metadata-cleanup.md` | Finding & removing DC residue; what each leftover object means |
| `references/os-reinstall.md` | Autounattend build, ISO attach, boot sequence, virtio driver selection |
| `references/promotion.md` | AD DS role install + replica promotion + post-promotion DNS & verification |
| `references/gotchas.md` | Catalog of field-tested failure modes, each with signature + fix |
| `references/credential-handling.md` | What the skill does with secrets vs. what it must not pretend to do |
| `assets/autounattend.xml.template` | Parameterized Server Core unattend (UEFI/GPT, virtio, static IP) |
| `scripts/run-guest-ps.sh` | Run base64'd PowerShell in a guest via QGA, secrets over stdin |
| `scripts/build-unattend-iso.sh` | Package an autounattend.xml into an attachable ISO |

## Using with AI Agents

Plain markdown + shell — no framework lock-in.

### Claude Code

```bash
git clone https://github.com/eddygk/proxmox-dc-lifecycle.git proxmox-dc-lifecycle
echo "For Windows AD domain-controller rebuilds on Proxmox, read proxmox-dc-lifecycle/SKILL.md and its references/." >> CLAUDE.md
```

Or install it as a skill: `cp -r proxmox-dc-lifecycle ~/.claude/skills/`.

### OpenClaw / ClawHub

```bash
clawhub install proxmox-dc-lifecycle
```

### Cursor / Windsurf / Other Agents

Drop `SKILL.md` into your project's context directory or reference it in your editor's custom-instructions mechanism. It's standard markdown — it works anywhere.

## Companion

Pairs well with [proxmox-ops](https://github.com/eddygk/proxmox-ops) for general Proxmox VE management (VM lifecycle, disk resize, snapshots). This skill focuses specifically on the Windows AD domain-controller lifecycle on top of Proxmox.

## License

MIT
