# Extending — phases, ownership, reaper, adding a phase

## Phase model (sync_v2.py, run in order)

- **0 custom fields** — ensure all custom fields exist (idempotent); also drives VM
  custom-field + tag population and the removal lifecycle.
- **1 VM interfaces + MACs** from `net*` config.
- **2 IP assignment** to interfaces (LXC static `ip=`; QEMU via guest-agent MAC match).
- **3 VLANs** from interface `tag=`.
- **4 node enrichment** — Proxmox node DCIM interfaces/IPs, CPU/memory, Proxmox
  version as platform, tags. With `--idrac`, live Redfish adds serial/firmware/NIC MACs.
- **5 virtual disks** (real data disks only; firmware-state volumes excluded).
- **6 platform/OS** via guest agent, fallback to `ostype`.

Per-guest the driver also auto-creates absent VMs, refreshes core fields
(status/vcpus/memory) for existing ones, applies tags, and stamps a last-seen time.

## Field ownership (don't cross)

- Interface `description` is owned by the Proxmox sync.
- `unifi_*` custom fields are owned by the UniFi sync.
- VM `disk` is derived by NetBox from VirtualDisks — never written directly.
- Manually-set node device fields are never overwritten unless an override flag is
  passed.

## Removal lifecycle (reaper)

Runs only on a full run (no single-VMID scope) unless disabled with `--no-reap`.
Acts only on sync-owned VMs (those carrying the `proxmox_vmid` custom field) that
are absent from Proxmox, transitioning by age since last-seen:

- `REAP_OFFLINE_DAYS` → status `offline`
- `REAP_DECOM_DAYS` → status `decommissioning`
- `REAP_DELETE_DAYS` → delete the NetBox record

All thresholds are environment variables. Records the sync didn't create (no
`proxmox_vmid`) are never reaped.

## Adding a phase idempotently

1. New custom field? add it to the phase-0 ensure step.
2. Route all writes through the client's `patch`/`post` so `--dry-run` and
   `--report` work for free.
3. Compare correctly (numeric for floats; re-fetch the object for custom-field
   comparisons; skip writes when already at the target) so a second run is
   all-`unchanged`.
4. Increment a per-object stat so it appears in the run summary.
5. Verify: dry-run → apply → run again and confirm no changes.
