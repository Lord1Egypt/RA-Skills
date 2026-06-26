# Deploy a GPU VM on Nebius AI Cloud

This example creates a GPU virtual machine with CUDA and Docker pre-installed, suitable for running vLLM or other GPU workloads.

## Prerequisites

- Nebius CLI installed and authenticated
- SSH public key for access
- GPU quota in your project

## Steps

```bash
# 1. Set variables
PROJECT_ID=$(nebius config get parent-id)
VM_NAME="my-gpu-vm"
GPU_PLATFORM="gpu-h200-sxm"  # Options: gpu-h100-sxm, gpu-h200-sxm, gpu-l40s-pcie
GPU_PRESET="1gpu-16vcpu-200gb"
SSH_PUBLIC_KEY="$(cat ~/.ssh/id_rsa.pub 2>/dev/null || cat ~/.ssh/id_ed25519.pub)"

# 2. Create networking
NETWORK_ID=$(nebius vpc network create \
  --name ${VM_NAME}-net \
  --parent-id $PROJECT_ID \
  --format json | jq -r '.metadata.id')

SUBNET_ID=$(nebius vpc subnet create \
  --name ${VM_NAME}-subnet \
  --parent-id $PROJECT_ID \
  --network-id $NETWORK_ID \
  --ipv4-cidr-blocks '["10.0.0.0/24"]' \
  --format json | jq -r '.metadata.id')

echo "Network: $NETWORK_ID"
echo "Subnet: $SUBNET_ID"

# 3. Create boot disk with CUDA
DISK_ID=$(nebius compute disk create \
  --name ${VM_NAME}-boot \
  --parent-id $PROJECT_ID \
  --type network_ssd \
  --size-gibibytes 200 \
  --block-size-bytes 4096 \
  --source-image-family-image-family ubuntu22.04-cuda12 \
  --format json | jq -r '.metadata.id')

echo "Boot disk: $DISK_ID"

# 4. Prepare cloud-init
CLOUD_INIT=$(cat <<'CLOUD_INIT_EOF'
#cloud-config
users:
  - name: user
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - SSH_KEY_PLACEHOLDER

package_update: true
packages:
  - docker.io
  - docker-compose
  - jq
  - htop
  - tmux

runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker user
  - echo "VM setup complete" > /tmp/setup-done
CLOUD_INIT_EOF
)

# Inject SSH key
CLOUD_INIT="${CLOUD_INIT//SSH_KEY_PLACEHOLDER/$SSH_PUBLIC_KEY}"

# 5. Create VM
INSTANCE_ID=$(nebius compute instance create \
  --name $VM_NAME \
  --parent-id $PROJECT_ID \
  --resources-platform $GPU_PLATFORM \
  --resources-preset $GPU_PRESET \
  --boot-disk-attach-mode read_write \
  --boot-disk-existing-disk-id $DISK_ID \
  --network-interfaces "[{
    \"name\": \"eth0\",
    \"subnet_id\": \"${SUBNET_ID}\",
    \"ip_address\": {},
    \"public_ip_address\": {}
  }]" \
  --cloud-init-user-data "$CLOUD_INIT" \
  --format json | jq -r '.metadata.id')

echo "Instance: $INSTANCE_ID"

# 6. Wait for VM and get public IP
echo "Waiting for VM to be ready..."
while true; do
  STATE=$(nebius compute instance get --id $INSTANCE_ID --format json | jq -r '.status.state')
  echo "  State: $STATE"
  if [ "$STATE" = "RUNNING" ]; then
    # Public IP includes /32 CIDR suffix — strip it
    PUBLIC_IP=$(nebius compute instance get --id $INSTANCE_ID --format json \
      | jq -r '.status.network_interfaces[0].public_ip_address.address' \
      | cut -d/ -f1)
    echo "VM ready! Public IP: $PUBLIC_IP"
    break
  fi
  sleep 10
done

# 7. SSH in (wait for cloud-init to finish)
# Note: SSH username depends on cloud-init config. Default is "nebius" for
# Nebius VMs, but this example uses "user" (set in cloud-init above).
echo ""
echo "SSH command: ssh user@${PUBLIC_IP}"
echo "Wait ~2 min for cloud-init to complete before SSHing."
```

## After SSH: Run vLLM

```bash
# On the VM:
docker run --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

## Managing Your VM

```bash
# Stop VM (pause GPU billing)
nebius compute instance stop --id $INSTANCE_ID

# Start VM
nebius compute instance start --id $INSTANCE_ID

# Delete VM and disk
nebius compute instance delete --id $INSTANCE_ID
nebius compute disk delete --id $DISK_ID

# Also clean up networking if no longer needed
nebius vpc subnet delete --id $SUBNET_ID
nebius vpc network delete --id $NETWORK_ID
```

## Cost Tips

- **Stop VMs when not in use** - GPU billing stops when the instance is stopped
- **Use H100 over H200** if your model fits in 80GB VRAM - it's cheaper
- **Use L40S** for cost-effective inference of smaller models
- **Use preemptible VMs** (`--preemptible-priority 3`) for batch/training jobs where interruptions are acceptable
