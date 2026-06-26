# Managed Kubernetes (mk8s) Reference

## Create Cluster

```bash
nebius mk8s cluster create \
  --name <cluster-name> \
  --parent-id <PROJECT_ID> \
  --control-plane-subnet-id <SUBNET_ID> \
  --control-plane-version "1.31" \
  --control-plane-endpoints-public-endpoint \
  --format json
```

### Key Parameters

| Parameter | Description |
|---|---|
| `--name` | Cluster name |
| `--parent-id` | Project ID (required) |
| `--control-plane-subnet-id` | Subnet for control plane (required) |
| `--control-plane-version` | Kubernetes version (e.g., `1.31`) |
| `--control-plane-endpoints-public-endpoint` | Enable public API endpoint |
| `--control-plane-etcd-cluster-size` | etcd cluster size (default: 3) |
| `--control-plane-karpenter` | Install Karpenter for auto-provisioning |
| `--kube-network-service-cidrs` | Service CIDR (default: `/16`) |

## Create Node Group

```bash
nebius mk8s node-group create \
  --parent-id <CLUSTER_ID> \
  --name <node-group-name> \
  --fixed-node-count 2 \
  --template-resources-platform gpu-h100-sxm \
  --template-resources-preset 1gpu-16vcpu-200gb \
  --format json
```

### Node Group Parameters

| Parameter | Description |
|---|---|
| `--parent-id` | Cluster ID |
| `--name` | Node group name |
| `--fixed-node-count` | Number of nodes |
| `--template-resources-platform` | GPU/CPU platform |
| `--template-resources-preset` | Resource preset |

## Get Cluster Credentials (kubectl access)

```bash
# Generate kubeconfig for external access
nebius mk8s cluster get-credentials \
  --id <CLUSTER_ID> \
  --external

# Verify access
kubectl get nodes
```

## Manage Clusters

```bash
# List clusters
nebius mk8s cluster list --format json

# Get cluster details
nebius mk8s cluster get --id <CLUSTER_ID> --format json

# List available Kubernetes versions
nebius mk8s cluster list-control-plane-versions --format json

# Delete cluster
nebius mk8s cluster delete --id <CLUSTER_ID>
```

## Manage Node Groups

```bash
# List node groups
nebius mk8s node-group list --parent-id <CLUSTER_ID> --format json

# Upgrade node group
nebius mk8s node-group upgrade --id <NODE_GROUP_ID>

# Delete node group
nebius mk8s node-group delete --id <NODE_GROUP_ID>
```

## Soperator (Slurm on Kubernetes)

Soperator runs Slurm clusters on top of Kubernetes for HPC/AI training workloads.

### Prerequisites

- A running mk8s cluster with GPU node groups
- NVIDIA GPU Operator installed
- NVIDIA Network Operator (if using InfiniBand)
- Cilium CNI
- Shared storage with ReadWriteMany PVC

### Deploy via Helm

```bash
# Add Nebius Helm repo
helm repo add nebius https://charts.nebius.com
helm repo update

# Install Soperator
helm install soperator nebius/soperator \
  --namespace soperator-system \
  --create-namespace

# Deploy a Slurm cluster
helm install my-slurm nebius/slurm-cluster \
  --namespace my-slurm \
  --create-namespace \
  --values slurm-values.yaml
```

### Managed Soperator

For a fully managed experience, Nebius offers Managed Soperator which pre-packages all components including NVIDIA drivers. Deploy from the web console or use:

```bash
nebius applications k8s-release create \
  --name <release-name> \
  --format json
```

## Full Workflow: Cluster + GPU Node Group

```bash
# 1. Create network & subnet (see networking-reference.md)

# 2. Create cluster
CLUSTER_ID=$(nebius mk8s cluster create \
  --name my-k8s-cluster \
  --parent-id $PROJECT_ID \
  --control-plane-subnet-id $SUBNET_ID \
  --control-plane-version "1.31" \
  --control-plane-endpoints-public-endpoint \
  --format json | jq -r '.metadata.id')

# 3. Wait for cluster to be ready
echo "Waiting for cluster to be ready..."
while true; do
  STATE=$(nebius mk8s cluster get --id $CLUSTER_ID --format json | jq -r '.status.state')
  echo "State: $STATE"
  [ "$STATE" = "RUNNING" ] && break
  sleep 15
done

# 4. Create GPU node group
nebius mk8s node-group create \
  --parent-id $CLUSTER_ID \
  --name gpu-nodes \
  --fixed-node-count 1 \
  --template-resources-platform gpu-h100-sxm \
  --template-resources-preset 1gpu-16vcpu-200gb \
  --format json

# 5. Get credentials
nebius mk8s cluster get-credentials --id $CLUSTER_ID --external

# 6. Verify
kubectl get nodes
```
