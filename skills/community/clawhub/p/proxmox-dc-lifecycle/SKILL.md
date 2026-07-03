---
name: proxmox-dc-lifecycle
description: >-
  Rebuild, replace, demote, reinstall, rejoin, or re-promote a Windows Active
  Directory domain controller VM on Proxmox: demote it, clean metadata from a
  healthy DC, reinstall via autounattend, then promote it again. Use for
  Proxmox-hosted DC rebuild requests and symptoms that point to rebuild: NTDS
  will not start, ntds.dit is missing, promotion fails with trust-relationship or
  "no computer account" errors, demotion hangs, dcdiag/replication fails on one
  DC, or a broken DC VM needs to come back. Also use for Windows AD operations
  through QEMU guest agent (qm guest exec). Rule: do not corrupt Active
  Directory; verify replication and FSMO before and after every lifecycle step,
  change one DC at a time, and never destroy or recreate a VM while AD still has
  NTDS Settings for that DC.
---

# Proxmox DC Lifecycle

Rebuild a domain controller that lives as a VM on a Proxmox hypervisor, one DC at a time, without corrupting Active Directory. This skill was distilled from production DC rebuilds; the flow rebuilds any additional (non-last) DC.

## The prime directive

**Do not corrupt Active Directory.** Everything else is negotiable. Concretely:

- **One DC at a time.** Never have two DCs in a broken/in-flight state simultaneously. The FSMO holder must stay healthy throughout.
- **Verify before and after every lifecycle step** with `repadmin /replsummary` (expect `0 fails`) and `netdom query fsmo`. A green replication picture is your license to proceed; anything else means stop and diagnose.
- **Never destroy/recreate the VM while AD still sees it as a DC.** "AD sees it as a DC" = an `nTDSDSA` (NTDS Settings) object exists for it under `CN=Sites`. That object's *absence* — not the VM being off, not the computer object being gone — is the gate that unlocks the OS rebuild.
- **Snapshot the VM before destructive steps.** `qm snapshot <vmid> <label>` is seconds of cost and the only instant rollback.
- **Target only additional DCs.** This flow assumes the DC being rebuilt is NOT the last DC in the domain and holds NO FSMO roles. If it holds FSMO, transfer them to a healthy DC first. If it's the last DC, this is a different (restore-from-backup) procedure — stop and reassess.

## Environment config

All environment-specific values live here, in one place. **Fill this in for YOUR environment before running**, then confirm against live state (`qm config`, `qm list`, a query to a healthy DC) — recalled facts go stale. Everything downstream (reference files, examples) refers to these names rather than hardcoding.

```jsonc
{
  "domain":        "example.local",
  "subnet":        "10.0.0.0/24",
  "gateway":       "10.0.0.1",
  "timezone":      "UTC",
  "fsmoHolder":    "DC1",                 // holds all 5 FSMO; NEVER the rebuild target
  "dcs": [
    { "name": "DC1", "vmid": 0, "ip": "10.0.0.10" },   // authority / DNS
    { "name": "DC2", "vmid": 0, "ip": "10.0.0.20" }
    // ...one entry per DC; rebuild one at a time
  ],
  "primaryDns":    "10.0.0.10",           // a healthy DC; the new DC points here during build
  "bridge":        "vmbr0",
  "vlanTag":       0,                      // 0 / omit if untagged
  "isoStorage":    "local",               // Proxmox storage holding the two ISOs below
  "serverIso":     "<windows-server-eval>.iso",
  "virtioIso":     "virtio-win-<ver>.iso",
  "pxeSource":     null,                   // optional: { name, vmid } of a WDS/MDT server on the same VLAN
  "credentialStore": "BRING YOUR OWN. The host has no secret manager. Generate/store secrets on a machine that does, and apply them by piping into the guest's stdin over SSH (e.g. <secret-source> | ssh root@<pvehost> 'qm guest exec <vmid> --pass-stdin 1 -- ...'). See references/credential-handling.md."
}
```

- You run ON the Proxmox host with passwordless `sudo` and `qm` at `/usr/sbin/qm`. There is no separate SSH hop — "ssh root@host" collapses to local `sudo qm`.
- VMs expose the **QEMU guest agent (QGA)**. You drive Windows guests with `sudo qm guest exec <vmid> ... powershell.exe ...`. This is the execution backbone — see `references/qga-execution.md`. WinRM/PowerShell-Remoting between DCs is NOT used (it fails between DCs — see Gotchas).
- The reference files speak in terms of these names ("the FSMO holder", "isoStorage", "a DC's vmid"). To use this skill, fill the block above for your environment; change nothing else.

## The lifecycle, in order

Work the phases below top to bottom. Each phase ends with a verification gate. **Do not cross a gate that isn't green.** Use a task list so a long rebuild survives interruptions.

### Phase 0 — Orient & baseline (read-only)
1. Confirm you're on the right host: `hostname`, `ip -4 addr`, `sudo qm list`. The DC VMIDs must be present.
2. Ping the guest agents: `sudo qm guest cmd <vmid> ping` for each DC.
3. Capture the baseline from the FSMO holder: FSMO roles, `repadmin /replsummary`, each DC's SYSVOL/NETLOGON shares and DFSR state. See `references/verification.md` for exact commands.
4. **Gate:** replication shows `0 fails`, FSMO are where you expect, the target DC holds none. Record this — it's your "known good."

### Phase 1 — Snapshot the target
`sudo qm snapshot <vmid> predemote_<date> --description "..."`. Confirm with `qm listsnapshot <vmid>`.

### Phase 2 — Demote the target DC
Run the demotion **locally inside the target guest** via QGA (NOT remoting from another DC). See `references/demotion.md` for the script and the two gotchas that will otherwise hang or fail it:
- supply `-LocalAdministratorPassword` (else it prompts and blocks under `-NonInteractive`),
- supply `-RemoveDnsDelegation:$false` when the parent DNS zone is on external nameservers (Cloudflare, etc.) you don't manage via Windows DNS — otherwise it stalls for minutes on RPC timeouts trying to delete a delegation it can't reach.

If graceful demotion is genuinely impossible, fall back to forced removal + metadata cleanup — but only after intentionally taking the DC offline. See `references/demotion.md`.

**Gate:** from a surviving DC, the target no longer appears in `Get-ADDomainController`, and replication among the remaining DCs is still `0 fails`.

### Phase 3 — Metadata cleanup & verify
A graceful demote usually cleans its own metadata. A forced/interrupted removal does NOT — you must clean it. Check from a surviving DC for residue: the `nTDSDSA` object (should be gone), an empty `CN=<dc>` **server object** under Sites (delete it), the computer object, DFSR/FRS member objects, and stale DNS records. Full procedure and the "what each leftover means" table is in `references/metadata-cleanup.md`. Tip: keep the computer object (delete only the server-object shell) to make re-promotion's trust step trivial — see `promotion.md` §0.

Then run the full health verification (`repadmin /replsummary`, `dcdiag` on the FSMO holder and each surviving DC). A lone `DFSREvent` warning referencing the just-removed DC is expected and benign (it's retrying a partner that's gone); everything else should pass.

**Gate (this is the big one):** No `nTDSDSA` for the target anywhere. `Get-ADDomainController` lists only the surviving DCs (the target is absent). Replication `0 fails`. **Only now may you touch the VM's disk.**

### Phase 4 — Reinstall the OS (hands-off)
Keep the same VMID, MAC, and disk — reinstall *onto* the existing VM, don't recreate it (that's how MAC/IP/config are preserved).

> **The disk wipe is irreversible — gate it.** Step 3 wipes the boot disk. Before running it: confirm the Phase-3 gate is green (no `nTDSDSA` for this DC anywhere — AD does not see it as a DC), confirm the `<vmid>` is the intended target and nothing else, and **get explicit operator confirmation to wipe that specific VM**. Never wipe while AD still sees the box as a DC, and never run this step unattended.

1. Read `qm config <vmid>`: note the boot disk bus (`virtio0` ⇒ **viostor** driver; a `scsiN` disk ⇒ **vioscsi**), BIOS (OVMF ⇒ UEFI/GPT partitioning), MAC, net bridge/VLAN.
2. Build an `autounattend.xml` from `assets/autounattend.xml.template` — it injects virtio drivers in WinPE, partitions UEFI/GPT, installs Server Core, sets name + static IP + DNS, and enables the guest agent + WinRM at first logon. Fill the placeholders (see template header). Select the image by **`/IMAGE/INDEX`**, verified with `wiminfo` against the ISO's `install.wim`.
3. Package the unattend as a tiny ISO and attach all three ISOs; set boot to DVD. `scripts/build-unattend-iso.sh` does the packaging. See `references/os-reinstall.md` for the exact `qm set` invocations and the destructive shutdown→boot sequence.
4. **Gate:** install is complete (`ImageState=IMAGE_STATE_COMPLETE`), the guest agent responds, hostname/IP/timezone are correct, time is in sync. The box is a clean domain-*member*-to-be (not yet a DC).

### Phase 5 — Join & promote
Install AD DS role, then `Install-ADDSDomainController` (replica) against the domain, supplying domain creds + DSRM password. Establish a trusted computer account first (see `promotion.md` §0). Point the new DC's DNS at a healthy DC during promotion; after it's a DC, set DNS to itself + a partner. Full script in `references/promotion.md`.

**Gate:** new DC appears in `Get-ADDomainController` with an `nTDSDSA` object, `repadmin /replsummary` is `0 fails` including the new DC in both directions, SYSVOL/NETLOGON shared, `dcdiag` clean (modulo transient DFSR-initial-sync and SystemLog churn). Re-confirm FSMO unchanged.

### Phase 6 — Finalize
Detach install ISOs, set boot back to the disk, remove the unattend ISO and any temp cred files, hand off the throwaway local-admin/DSRM passwords to the operator, and (optionally) prune now-stale pre-rebuild snapshots once the new DC has been healthy for a while. Then — and only then — move to the next DC.

## Credential & secret handling

Secrets are radioactive. Follow `references/qga-execution.md` precisely: pass passwords to the guest over **QGA stdin** (`--pass-stdin`), never on a process command line or `-EncodedCommand`. If a `creds.txt` convention is used, `chmod 600`, read it silently, delete it the moment it's loaded. Any cred file written into a guest must be deleted as the *first action* of the script that consumes it. For scheduled tasks, use `schtasks /rp *` (password from stdin), never `/rp "<pw>"`. Never echo a secret into chat, logs, or task XML. Show a sha256 fingerprint, never the value.

**Know the boundary:** this skill runs on the Proxmox host, which has no password manager. It can generate throwaway randoms (local Administrator, DSRM) and apply them, but it cannot store or later reveal them — and must not pretend to. After a rebuild, hand off to the operator to set known break-glass values (and rotate any exposed credential) from a machine that has their secret manager. Full detail: `references/credential-handling.md`.

## When to stop and ask

This skill makes real changes to a live directory. Stop and confirm with the user when: a gate isn't green and you can't explain why; the target turns out to hold FSMO or be the last DC; a demotion would need `-ForceRemoval`; or you're about to run the first *destructive* step of a phase (snapshot-and-demote, AD object deletion, disk wipe, promotion). Recommend the safe default, explain the risk in one or two lines, and let them decide.

## Reference files

- `references/qga-execution.md` — the QGA-over-stdin pattern, the `run_guest` helper, secret handling, timeout/backgrounding behavior. **Read this first** — it's how every other phase actually executes.
- `references/verification.md` — exact read-only commands for FSMO, replication, dcdiag, SYSVOL/DFSR, and how to read the results.
- `references/demotion.md` — graceful demotion script + the LocalAdministratorPassword and RemoveDnsDelegation gotchas; forced-removal fallback.
- `references/metadata-cleanup.md` — finding and removing DC residue; what each leftover object means; how to tell a completed-but-messy removal from a real failure.
- `references/os-reinstall.md` — autounattend build, ISO attach, boot sequence, virtio driver selection, the `qm set` commands.
- `references/promotion.md` — establishing trust, AD DS role install + replica promotion + post-promotion DNS and verification.
- `references/gotchas.md` — the catalog of failure modes seen in the field, each with its signature and fix. Skim it before starting and consult it the instant something hangs or errors.
- `references/credential-handling.md` — what the skill does with secrets vs. what it must NOT pretend to do (no password manager on the host); the throwaway-random + hand-off model.
- `assets/autounattend.xml.template` — parameterized Windows Server Core unattend (UEFI/GPT, virtio injection, static IP, agent+WinRM).
- `scripts/run-guest-ps.sh` — wrapper that runs base64'd PowerShell in a guest via QGA, with stdin secret passing.
- `scripts/build-unattend-iso.sh` — packages an autounattend.xml into an attachable ISO.
