---
name: netbox-sync-ops
version: 1.0.2
description: >-
  Infrastructure inventory automation and utility/integration operations for
  netbox-proxmox-sync, an idempotent state sync that models Proxmox VE and UniFi
  into NetBox DCIM/IPAM. Use when deploying it, running it on a schedule, adding
  a sync phase, tuning the VM removal lifecycle (reaper), enabling iDRAC/Redfish
  node enrichment, debugging churn, or resolving HTTP 400s and idempotency
  problems against the NetBox API. Encodes the safe operating procedure and the
  NetBox/UniFi API gotchas so changes stay idempotent and never destructively
  touch production systems. Source and full docs live at
  https://github.com/eddygk/netbox-proxmox-sync.
metadata:
  openclaw:
    homepage: https://github.com/eddygk/netbox-proxmox-sync
    os:
      - linux
    requires:
      bins:
        - python3
      env:
        - NETBOX_URL
        - NETBOX_TOKEN
        - PROXMOX_HOST
        - PROXMOX_TOKEN_ID
        - PROXMOX_TOKEN_SECRET
    envVars:
      - name: NETBOX_URL
        required: true
        description: NetBox API base URL.
      - name: NETBOX_TOKEN
        required: true
        description: NetBox API token.
      - name: PROXMOX_HOST
        required: true
        description: Proxmox API URL.
      - name: PROXMOX_TOKEN_ID
        required: true
        description: Proxmox API token identifier.
      - name: PROXMOX_TOKEN_SECRET
        required: true
        description: Proxmox API token secret.
---

# NetBox Sync Ops

Operate and safely extend `netbox-proxmox-sync` (https://github.com/eddygk/netbox-proxmox-sync) —
a cron-driven, idempotent sync that builds a rich NetBox inventory from Proxmox VE
and UniFi. This skill is the operator runbook; the repo has install/config/README.

## Safety rules (the prime directives)

- **The sync only touches NetBox via its REST API, and Proxmox/UniFi read-only.**
  It never powers off or destroys a guest. Keep it that way — no `pct stop/destroy`,
  no Proxmox writes.
- **Never destructively test against records named after production.** To test
  auto-create or the reaper, use a throwaway NetBox VM record with a VMID that is
  not a real guest (e.g. 99999), not a real service's record.
- **Every change must be idempotent.** Run the sync twice; the second run must
  report all-`unchanged`. Churn means a comparison bug — see references/gotchas.md.

## Core workflow

1. Configure `.env` from `.env.example` (NetBox + Proxmox required; UniFi + iDRAC
   optional). Optionally point `PREFIXES_FILE` at your VLAN/subnet map.
2. Dry-run first — `python3 sync_v2.py --dry-run --report` writes nothing and logs
   field-level before→after.
3. Apply — `python3 sync_v2.py`. Then run it again; confirm all-`unchanged`.
4. UniFi side — `python3 fetch_unifi_and_populate.py` (fetch + populate).
5. Schedule via cron (see repo `cron.example`); offset the UniFi job after the
   Proxmox job so MAC correlation matches against freshly-created interfaces.

## First safe run and reaper gate

Use this sequence before the first production run, after reconfiguring ownership
rules, or before enabling cron:

1. Preview a single known guest: `python3 sync_v2.py --dry-run --report --only-vmid <id> --no-reap`.
2. Apply the same scoped guest, then run it again and require all-`unchanged`.
3. Run a full dry-run with `--report --no-reap`; review any create/update/delete
   intent before allowing a full apply.
4. Enable the reaper only after the sync-owned NetBox records and thresholds are
   reviewed. The reaper can mark and eventually delete sync-owned VM records
   whose `proxmox_vmid` no longer exists in Proxmox; schedule with `--no-reap`
   until that behavior is intentional for the environment.

## Useful flags

`--dry-run` (no writes) · `--report` (field-level diffs) · `--phases 0,1,2,…`
(subset) · `--only-vmid N` (one guest) · `--idrac` (live Redfish node enrichment) ·
`--no-reap` (disable removal lifecycle).

## When to read the references

- **references/gotchas.md** — NetBox/UniFi API quirks that cause churn or 400s.
  Read first for any "re-patches every run" or HTTP 400.
- **references/extending.md** — phase model, field-ownership boundaries, the reaper
  lifecycle and its env knobs, and the recipe for adding a phase idempotently.

## Validate a change

```bash
python3 -m py_compile sync_v2.py populate_network.py
python3 sync_v2.py --dry-run --report --only-vmid <id>   # preview one guest
python3 sync_v2.py            # apply
python3 sync_v2.py            # MUST be all-unchanged (idempotency gate)
```
A full run scales with guest count; for large fleets run it in the background
rather than blocking on a short timeout.
