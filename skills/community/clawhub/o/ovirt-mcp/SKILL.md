---
name: ovirt-mcp
description: Manage oVirt/RHV virtualization infrastructure via MCP. Provides 186 tools for VMs, hosts, clusters, networks, storage, templates, snapshots, disks, events, RBAC, quotas, and more. Use when the user asks to manage oVirt virtual machines, create/delete/modify VMs, check host status, manage storage domains, handle templates, configure networks, manage user permissions, view events/alerts, or any oVirt/RHV infrastructure operations. Triggers on "oVirt", "RHV", "virtual machine", "VM management", "storage domain", "cluster", "host management".
---

# oVirt MCP Server

MCP server for oVirt/RHV virtualization management. 186 tools covering the full infrastructure lifecycle.

**Version**: 0.1.0 | **License**: MIT | **Author**: Joey Ma (@imjoey)

## Quick Start

### Install

```bash
pip install ovirt-engine-mcp-server
```

Or from source:

```bash
git clone https://github.com/imjoey/ovirt-engine-mcp-server.git
cd ovirt-engine-mcp-server
pip install -e .
```

### Configure

Environment variables (recommended):

```bash
export OVIRT_ENGINE_URL="https://ovirt-engine.example.com"
export OVIRT_ENGINE_USER="admin@internal"
export OVIRT_ENGINE_PASSWORD="your-password"
```

Or create a `config.yaml`:

```yaml
OVIRT_ENGINE_URL: https://ovirt-engine.example.com
OVIRT_ENGINE_USER: admin@internal
# OVIRT_ENGINE_PASSWORD should be set via environment variable
```

### Run

```bash
ovirt-engine-mcp
```

### Claude Desktop / OpenClaw Integration

```json
{
  "mcpServers": {
    "ovirt": {
      "command": "ovirt-engine-mcp",
      "env": {
        "OVIRT_ENGINE_URL": "https://ovirt-engine.example.com",
        "OVIRT_ENGINE_USER": "admin@internal",
        "OVIRT_ENGINE_PASSWORD": "your-password"
      }
    }
  }
}
```

### Docker

```bash
docker build -t ovirt-engine-mcp-server .
docker run -e OVIRT_ENGINE_URL=... -e OVIRT_ENGINE_USER=... -e OVIRT_ENGINE_PASSWORD=... ovirt-engine-mcp-server
```

## Architecture

```
MCP Client (Claude / OpenClaw / etc.)
        │  stdio (JSON-RPC)
        ▼
  MCP Server (server.py)
  ┌─────────────────────────────┐
  │  OvirtMCP (ovirt_mcp.py)    │  ← Core SDK wrapper (ovirtsdk4)
  │  186 methods               │
  ├─────────────────────────────┤
  │  Extension Modules:         │
  │  NetworkMCP · ClusterMCP    │
  │  TemplateMCP · DataCenterMCP│
  │  HostExtendedMCP            │
  │  StorageExtendedMCP         │
  │  DiskExtendedMCP            │
  │  EventsMCP · AffinityMCP    │
  │  RbacMCP · VmExtendedMCP    │
  │  TemplateExtendedMCP        │
  │  QuotaMCP · SystemMCP       │
  └─────────────────────────────┘
        │
        ▼
  oVirt Engine REST API
```

## Error Handling

All errors return structured JSON with error code, message, and retry guidance:

| Code | Retryable | Description |
|------|-----------|-------------|
| `CONNECTION_ERROR` | ✅ | Failed to connect to oVirt Engine |
| `NOT_FOUND` | ❌ | Requested resource not found |
| `PERMISSION_DENIED` | ❌ | Insufficient permissions |
| `VALIDATION_ERROR` | ❌ | Invalid input parameters |
| `TIMEOUT` | ✅ | Operation timed out |
| `SDK_ERROR` | ✅ | oVirt SDK internal error |

**Retry strategy**: Only retry on `retryable: true` errors. Use exponential backoff (1s → 2s → 4s). `NOT_FOUND` and `PERMISSION_DENIED` require user intervention.

## Available Tools

186 tools across 27 categories. Each reference file is self-contained with its own index:

| File | Tools | Covers |
|------|-------|--------|
| [vm.md](references/vm.md) | 35 | VM lifecycle, pools, checkpoints, snapshots |
| [host.md](references/host.md) | 19 | Host management, fencing, iSCSI |
| [cluster.md](references/cluster.md) | 11 | Clusters, CPU profiles |
| [datacenter.md](references/datacenter.md) | 5 | Data centers |
| [instance-types.md](references/instance-types.md) | 2 | Instance types |
| [storage.md](references/storage.md) | 16 | Storage domains, connections, iSCSI bonds |
| [disk.md](references/disk.md) | 13 | Disk lifecycle, snapshots, move, resize |
| [network.md](references/network.md) | 16 | Networks, VNIC profiles, QoS, MAC pools |
| [template.md](references/template.md) | 8 | Template lifecycle, disk/NIC lists |
| [system.md](references/system.md) | 6 | System info, jobs |
| [events.md](references/events.md) | 11 | Events, bookmarks, alerts |
| [rbac.md](references/rbac.md) | 24 | Users, groups, roles, permissions, tags, filters |
| [quota.md](references/quota.md) | 7 | Data center quotas |
| [affinity.md](references/affinity.md) | 13 | Affinity groups and labels |

### Quick Category Reference

| Category | Count | Key Tools |
|----------|-------|-----------|
| VM Core | 9 | `vm_list`, `vm_create`, `vm_start`, `vm_stop`, `vm_delete` |
| VM Extended | 16 | `vm_migrate`, `vm_console`, `vm_cdrom_*`, `vm_watchdog_*`, `vm_pin_to_host` |
| VM Pools | 5 | `vm_pool_list`, `vm_pool_create`, `vm_pool_update`, `vm_pool_delete` |
| VM Checkpoints | 4 | `vm_checkpoint_list/create/restore/delete` |
| Snapshots | 4 | `snapshot_list/create/restore/delete` |
| Disks Core | 3 | `disk_list`, `disk_create`, `disk_attach` |
| Disks Extended | 9 | `disk_get`, `disk_resize`, `disk_move`, `disk_sparsify`, `disk_export` |
| Networks | 9 | `network_list/create/update/delete`, `nic_list/add/remove` |
| VNIC Profiles | 5 | `vnic_profile_list/create/update/delete/get` |
| Network Filters & QoS | 3 | `network_filter_list`, `mac_pool_list`, `qos_list` |
| Hosts Core | 3 | `host_list`, `host_activate`, `host_deactivate` |
| Hosts Extended | 16 | `host_add`, `host_fence`, `host_iscsi_*`, `host_install`, `host_nic_*` |
| Clusters | 10 | `cluster_list/create/update/delete`, `cluster_cpu_load`, `cluster_memory_usage` |
| CPU Profiles | 2 | `cpu_profile_list`, `cpu_profile_get` |
| Data Centers | 5 | `datacenter_list/create/update/delete/get` |
| Storage Core | 8 | `storage_list/create/delete/attach/detach/stats` |
| Storage Extended | 10 | `storage_refresh`, `storage_import_vm`, `storage_files`, `iscsi_bond_list` |
| Templates Core | 2 | `template_list`, `template_vm_create` |
| Templates Extended | 6 | `template_get/create/delete/update`, `template_disk_list`, `template_nic_list` |
| Instance Types | 2 | `instance_type_list`, `instance_type_get` |
| Affinity Groups | 7 | `affinity_group_list/create/update/delete/add_vm/remove_vm` |
| Affinity Labels | 6 | `affinity_label_list/create/delete/assign/unassign` |
| Events | 11 | `event_list`, `event_search`, `event_alerts/errors/warnings`, `event_summary` |
| RBAC | 24 | `user_*`, `group_*`, `role_*`, `permission_*`, `tag_*`, `filter_list` |
| Quotas | 7 | `quota_list/create/update/delete`, `quota_*_limit_list` |
| System & Jobs | 6 | `system_get`, `job_list`, `job_cancel`, `system_statistics` |

## Common Workflows

### Create VM from Template

```
1. template_list → find template ID
2. cluster_list → find cluster ID
3. template_vm_create(name, template, cluster, ...)
4. vm_start(name_or_id)
```

### Migrate VM

```
1. vm_list(status="up") → find running VM
2. host_list() → find target host
3. vm_migrate(name_or_id, target_host)
```

### Create Snapshot & Restore

```
1. snapshot_create(name_or_id, description="before-patch")
2. ... perform changes ...
3. snapshot_restore(name_or_id, snapshot_id)  # if needed
```

### Storage Health Check

```
1. storage_list → list all domains
2. storage_stats(name_or_id) → check each domain
3. event_errors → check for storage-related errors
```

### RBAC Audit

```
1. permission_list(resource_type="cluster", resource_id="...") → list perms
2. user_list → list users
3. tag_list → list tags
```

## Requirements

- Python >= 3.10
- oVirt Engine 4.4+
- Dependencies: `mcp>=1.0.0`, `ovirtsdk4>=4.6.0`, `pyyaml>=6.0`, `requests>=2.31.0`, `colorlog>=6.8.0`

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check src/ tests/
```

## Related Projects

- [oVirt](https://www.ovirt.org/) — Open-source virtualization management
- [ovirtsdk4](https://github.com/oVirt/ovirt-engine-sdk-python) — Official oVirt Python SDK
- [Model Context Protocol](https://modelcontextprotocol.io/) — The MCP specification
