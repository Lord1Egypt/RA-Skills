# Compute VM Reference

## Create Boot Disk

Create a boot disk with a CUDA-enabled Ubuntu image:

```bash
nebius compute disk create \
  --name <disk-name> \
  --parent-id <PROJECT_ID> \
  --type network_ssd \
  --size-gibibytes 200 \
  --block-size-bytes 4096 \
  --source-image-family-image-family ubuntu22.04-cuda12 \
  --format json
```

### Available Image Families

| Family | Description | Min Disk Size |
|---|---|---|
| `ubuntu22.04-cuda12` | Ubuntu 22.04 with CUDA 12 (recommended for GPU) | **50 GiB** |
| `ubuntu22.04` | Ubuntu 22.04 (CPU only) | 10 GiB |

**Critical**: The `--source-image-family-image-family` flag has a double "image-family" — this is correct, not a typo. Using `--source-image-family` alone will fail.

**Critical**: Disk type must use underscores: `network_ssd`, NOT `network-ssd`.

## Create VM Instance

### GPU VM (e.g., H200 for self-hosted inference)

```bash
nebius compute instance create \
  --name <vm-name> \
  --parent-id <PROJECT_ID> \
  --resources-platform gpu-h200-sxm \
  --resources-preset 1gpu-16vcpu-200gb \
  --boot-disk-attach-mode read_write \
  --boot-disk-existing-disk-id <DISK_ID> \
  --network-interfaces '[{
    "name": "eth0",
    "subnet_id": "<SUBNET_ID>",
    "ip_address": {},
    "public_ip_address": {}
  }]' \
  --cloud-init-user-data "$(cat cloud-init.yaml)" \
  --format json
```

### Key Parameters

| Parameter | Description |
|---|---|
| `--name` | VM name |
| `--parent-id` | Project ID |
| `--resources-platform` | GPU/CPU platform (see platforms table) |
| `--resources-preset` | Resource allocation preset |
| `--boot-disk-existing-disk-id` | ID of the boot disk to attach |
| `--boot-disk-attach-mode` | `read_write` or `read_only` |
| `--network-interfaces` | JSON array of network interfaces |
| `--cloud-init-user-data` | Cloud-init configuration (string or file) |
| `--gpu-cluster-id` | GPU cluster ID (for multi-GPU with InfiniBand) |
| `--service-account-id` | Service account for VM API access |
| `--preemptible-priority` | 1-5 priority for preemptible (cheaper) VMs |
| `--stopped` | Create in stopped state (`true`/`false`) |

### Cloud-Init Example

```yaml
#cloud-config
users:
  - name: user
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - <YOUR_SSH_PUBLIC_KEY>

package_update: true
packages:
  - docker.io
  - jq

runcmd:
  - systemctl enable docker
  - systemctl start docker
```

## Manage VMs

```bash
# List all instances
nebius compute instance list --format json

# Get instance details
nebius compute instance get --id <INSTANCE_ID> --format json

# Stop instance (pauses billing)
nebius compute instance stop --id <INSTANCE_ID>

# Start instance
nebius compute instance start --id <INSTANCE_ID>

# Delete instance
nebius compute instance delete --id <INSTANCE_ID>
```

## GPU Clusters (for multi-GPU with InfiniBand)

```bash
# Create GPU cluster
nebius compute gpu-cluster create \
  --name <cluster-name> \
  --infiniband-fabric <fabric-name>

# List GPU clusters
nebius compute gpu-cluster list --format json
```

## Disk Management

```bash
# List disks
nebius compute disk list --format json

# Delete disk
nebius compute disk delete --id <DISK_ID>
```

## Platform Discovery

```bash
# List available platforms in current region
nebius compute platform list --format json
```

## SSH Access

After VM creation, get the public IP and SSH in:

```bash
# Get public IP (strip the /32 CIDR suffix)
PUBLIC_IP=$(nebius compute instance get --id <INSTANCE_ID> --format json \
  | jq -r '.status.network_interfaces[0].public_ip_address.address' \
  | cut -d/ -f1)

# SSH to VM — username is "nebius" (NOT root, ubuntu, admin, or user)
ssh nebius@${PUBLIC_IP}
# Or if using cloud-init with a custom user:
ssh <your-cloud-init-user>@${PUBLIC_IP}
```

**Important**: The default SSH username on Nebius VMs and AI endpoints is `nebius`. Cloud-init can override this with a custom user.

## Cost Considerations

- GPU VMs are billed per hour while running. Always `stop` when not in use.
- Use `--preemptible-priority` for cheaper preemptible instances (may be interrupted).
- Boot disks are billed separately from compute. Delete disks when deleting VMs.
- H200 > H100 in performance but also cost. Choose based on model size requirements.
