# proxmox-aiops CLI reference

All commands take `--target/-t <name>` (config target; omit for default) and,
where relevant, `--node/-n <name>`. Destructive commands support `--dry-run`.

## VM lifecycle

```bash
proxmox-aiops vm list [-t <target>] [-n <node>]
proxmox-aiops vm get <vmid>
proxmox-aiops vm config <vmid>
proxmox-aiops vm start <vmid>
proxmox-aiops vm stop <vmid> [--dry-run]            # hard power-off (double confirm)
proxmox-aiops vm shutdown <vmid> [--dry-run]        # graceful ACPI
proxmox-aiops vm reboot <vmid>
proxmox-aiops vm reconfigure <vmid> [--cores N] [--memory MiB] [--dry-run]
proxmox-aiops vm clone <vmid> --newid <id> [--name <name>]
proxmox-aiops vm delete <vmid> [--dry-run]          # irreversible (double confirm)
proxmox-aiops vm migrate <vmid> --to-node <node> [--offline] [--dry-run]
```

## Snapshots

```bash
proxmox-aiops vm snapshot-create <vmid> --name <snap>
proxmox-aiops vm snapshot-list <vmid>
proxmox-aiops vm snapshot-delete <vmid> --name <snap> [--dry-run]      # double confirm
proxmox-aiops vm snapshot-rollback <vmid> --name <snap> [--dry-run]    # irreversible
```

## LXC containers

```bash
proxmox-aiops ct list [-n <node>]
proxmox-aiops ct start <vmid>
proxmox-aiops ct stop <vmid> [--dry-run]            # double confirm
```

## Cluster / async tasks

```bash
proxmox-aiops cluster nodes
proxmox-aiops cluster status                        # membership + quorum
proxmox-aiops cluster task-status <UPID>            # poll a clone/migrate/backup task
```

## Storage

```bash
proxmox-aiops storage list [-n <node>]
proxmox-aiops storage content <storage> [--content iso|images|backup|vztmpl]
```

## Diagnostics & MCP

```bash
proxmox-aiops doctor                                # verify connectivity + credentials
proxmox-aiops mcp                                   # start the MCP server (stdio)
```

> Proxmox writes are asynchronous and return a task UPID. Poll completion with
> `cluster task-status <UPID>` rather than re-issuing the operation.
