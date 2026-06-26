# PBS Backup — Architecture

## Decision Tree

```
User: "make a backup"
  │
  ├─ Config exists?
  │   ├─ No → Setup flow
  │   └─ Yes
  │       ├─ Hosts reachable?
  │       │   ├─ No → Diagnose / re-setup host access
  │       │   └─ Yes
  │       │       ├─ How many targets?
  │       │       │   ├─ 0 → Ask user to register targets
  │       │       │   ├─ 1 → Backup directly
  │       │       │   └─ N → Ask which one
  │       │       └─ VMID specified? → Backup that one
  │       └─
  └─
```

## Setup Flow

```
A. PBS present?  ──no──▶  Install PBS (ask all params first, confirm, then execute)
       │yes
       ▼
B. Storage?  ──local──▶  Create datastore at /backup
       │nas
       ▼
   NAS mounted? ──no──▶  Mount NFS/SMB (ask IP, path, type)
       │yes
       ▼
   Create datastore on mount
       │
       ▼
C. Proxmox host access  ──import from proxmox.json?──▶  Import + verify
       │manual
       ▼
   Ask: IP, token ID, token secret → test connection
       │
       ▼
D. PBS storage in Proxmox?  ──no──▶  Guide pvesm add
       │yes
       ▼
E. Register targets (VMID, type, host, name)
       │
       ▼
F. Save config → test backup
```

## Config Schema

```json
{
  "pbs": {
    "host": "192.168.x.x",
    "port": 8007,
    "datastore": "backups",
    "verify_ssl": false
  },
  "defaults": {
    "storage": "my-pbs",
    "mode": "snapshot",
    "compress": "zstd",
    "prune_keep_last": 10
  },
  "proxmox_hosts": {
    "label": {
      "host": "192.168.x.x",
      "node": "pve",
      "token_id": "root@pam!backup",
      "token_secret": "xxx",
      "verify_ssl": false
    }
  },
  "targets": {
    "100": {
      "host": "label",
      "node": "pve",
      "type": "lxc",
      "name": "my-container",
      "storage": "my-pbs"
    }
  }
}
```

**Note:** The `prune_keep_last` key is reserved for a future pruning command and is not currently used by the backup script.

## Safety Rules

- Never assume values — always ask or read from config.
- Always set `storage` explicitly in vzdump calls.
- Use `vzdump --mode snapshot`, never `pct snapshot`.
- Installation: collect ALL parameters first, show plan, wait for user confirmation.
- Credentials: chmod 600, never log token secrets.
