# Task: Kubeconfig Acquisition

## Operations Catalog

| Operation ID | Operation Name                   | hcloud Command                                   | Key Parameters                     |
| ------------ | -------------------------------- | ------------------------------------------------ | ---------------------------------- |
| OP-KC-1      | Obtain CCE Cluster Kubeconfig    | `hcloud CCE CreateKubernetesClusterCert`         | `--cluster_id`, `--duration`       |
| OP-KC-2      | Obtain UCS Federation Kubeconfig | `hcloud UCS DownloadFederationKubeconfig`        | `--clustergroupid`, `--duration`   |

> **Note**: This skill focuses on CCE direct cluster access and UCS fleet (federation) operations. UCS single-cluster kubeconfig (CreateClusterKubeconfig) is out of scope — it only applies to clusters registered in UCS but not yet joined a fleet, which is a transitional state.

## W1: Obtain CCE Cluster Kubeconfig

### Step 1: Find Cluster ID

If the user does not know the CCE cluster ID, locate it first:

```bash
# List all CCE clusters in the region
hcloud CCE ListClusters --cli-region=cn-north-4
```

Identify the target cluster from the output and record its `cluster_id` (the `metadata.uid` or `clusterId` field).

### Step 2: Create Kubeconfig Certificate

```bash
# Generate kubeconfig (duration in days, 1-1827)
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --duration=1 --cli-region=cn-north-4
```

**Important**: `--duration` is in **days** (range 1-1827). Use the minimum duration needed for your session.

### Step 3: Save Kubeconfig to File

```bash
# Save kubeconfig to a dedicated file
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --duration=1 --cli-region=cn-north-4 > ~/.kube/cce-kubeconfig.yaml

# Set restrictive file permissions
chmod 600 ~/.kube/cce-kubeconfig.yaml
```

### Step 4: Verify Connection

```bash
# Verify the kubeconfig is valid and cluster is reachable
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml cluster-info

# Test listing nodes
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get nodes
```

If `cluster-info` returns cluster details, the kubeconfig is valid and the connection is successful.

### Troubleshooting

- **404 error**: Verify `--cluster_id` is correct and the cluster exists in the specified region
- **Authentication failure**: Check AK/SK configuration; ensure `HUAWEI_CLOUD_AK` and `HUAWEI_CLOUD_SK` are set
- **Permission denied**: Verify IAM permissions include `cce:cluster:createCert`

## W2: Obtain UCS Federation Kubeconfig

UCS federation kubeconfig provides multi-cluster fleet access. It contains two contexts:
- `federation`: Operates on fleet-level resources (propagated workloads, policies)
- `karmada-aggregated-apiserver`: Proxy access to individual member clusters via URL path `/clusters/<cluster-name>/proxy`

### Step 1: Find Fleet Group ID

If the user does not know the fleet group ID, locate it first:

```bash
# List all fleet groups
hcloud UCS ListClusterGroup --limit=20 --offset=0 --cli-region=cn-north-4
```

Identify the target fleet group and record its `metadata.uid` as the `clustergroupid`.

### Step 2: Download Federation Kubeconfig

```bash
# Generate federation kubeconfig (duration in days, 1-1825)
hcloud UCS DownloadFederationKubeconfig --clustergroupid=<fleet-id> --duration=1 --cli-region=cn-north-4
```

**Important**: `--duration` is in **days** (range 1-1825), not seconds.

### Step 3: Save and Verify

```bash
# Save federation kubeconfig
hcloud UCS DownloadFederationKubeconfig --clustergroupid=<fleet-id> --duration=1 --cli-region=cn-north-4 > ~/.kube/ucs-federation-kubeconfig.yaml

# Set restrictive file permissions
chmod 600 ~/.kube/ucs-federation-kubeconfig.yaml

# Verify connection (federation kubeconfig provides access to all clusters in the fleet)
kubectl --kubeconfig=~/.kube/ucs-federation-kubeconfig.yaml cluster-info
```

### Step 4: Use Federation Contexts

```bash
# Default context: federation (fleet-level operations)
kubectl --kubeconfig=~/.kube/ucs-federation-kubeconfig.yaml get deployments

# Switch to karmada-aggregated-apiserver (proxy to specific member cluster)
kubectl --kubeconfig=~/.kube/ucs-federation-kubeconfig.yaml --context=karmada-aggregated-apiserver get nodes
```

**Network Prerequisite**: UCS federation API server uses `<fleet-name>.fleet.ucs.<region>.myhuaweicloud.com` domain, which resolves via VPC Endpoint (VPCEP). If DNS resolution fails (`no such host` error), ensure your network environment can reach the UCS VPCEP — this typically requires:
- Running from within a Huawei Cloud VPC (ECS/Cloud Desktop)
- VPN access to Huawei Cloud VPC
- VPC peering with the UCS fleet's VPC

The VPCEP ID can be found in the fleet group's `spec.connectGatewayEndpoints` field from `ShowClusterGroup` output.

### Troubleshooting

- **Missing duration**: `--duration` is required for `DownloadFederationKubeconfig`
- **Duration unit**: Must be days (1-1825), not seconds
- **404 error**: Verify `--clustergroupid` is correct; the fleet group must exist
- **DNS resolution failure (`no such host`)**: Network cannot reach UCS federation domain; ensure VPCEP access

## W4: Switch Between Multiple Contexts

When working with multiple clusters, manage kubeconfig contexts efficiently.

### Option 1: KUBECONFIG Environment Variable

```bash
# Point kubectl to a specific kubeconfig file
export KUBECONFIG=~/.kube/cce-kubeconfig.yaml
kubectl get nodes

# Switch to UCS federation kubeconfig
export KUBECONFIG=~/.kube/ucs-federation-kubeconfig.yaml
kubectl get nodes
```

### Option 2: Merge Multiple Kubeconfigs

```bash
# Merge CCE and UCS federation kubeconfigs
KUBECONFIG=~/.kube/cce-kubeconfig.yaml:~/.kube/ucs-federation-kubeconfig.yaml kubectl config view --flatten > ~/.kube/merged-kubeconfig.yaml

# Use merged kubeconfig
export KUBECONFIG=~/.kube/merged-kubeconfig.yaml
```

### Option 3: Switch Context Within Merged Kubeconfig

```bash
# List available contexts
kubectl config get-contexts

# Switch to a specific context
kubectl config use-context <context-name>

# Show current context
kubectl config current-context
```

### Option 4: Explicit --kubeconfig Flag

```bash
# Use explicit flag for each command (most explicit, least error-prone)
kubectl --kubeconfig=~/.kube/cce-kubeconfig.yaml get pods -n production
kubectl --kubeconfig=~/.kube/ucs-kubeconfig.yaml get pods -n production
```

**Recommendation**: Use `--kubeconfig` flag for production operations to avoid accidental operations on the wrong cluster.

## Common Scenarios

### CCE vs UCS Kubeconfig Choice

| Scenario                        | Use Which Kubeconfig             | Reason                                      |
| ------------------------------- | -------------------------------- | ------------------------------------------- |
| CCE cluster workload management | CCE CreateKubernetesClusterCert  | Direct CCE cluster access                   |
| UCS multi-cluster fleet ops     | UCS DownloadFederationKubeconfig | Single kubeconfig for all fleet clusters    |
| UCS proxy to specific member    | UCS Federation + karmada context | Proxy access via `/clusters/<name>/proxy`   |
| CI/CD pipeline deployment        | CCE CreateKubernetesClusterCert  | Short-lived cert for automated deployments  |

### Duration Selection

| Use Case          | CCE Duration (days) | UCS Federation Duration (days) |
| ----------------- | -------------------- | --------------------------------- |
| Quick inspection  | 1                    | 1                                 |
| Daily operations  | 7                    | 7                                 |
| CI/CD pipeline    | 1                    | 1                                 |
| Long-term access  | 30 (max recommended) | 30 (max recommended)              |

### CI/CD Integration

```bash
# CI/CD: Acquire kubeconfig, deploy, cleanup
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --duration=1 --cli-region=cn-north-4 > /tmp/ci-kubeconfig.yaml
kubectl --kubeconfig=/tmp/ci-kubeconfig.yaml apply -f deployment.yaml -n production
kubectl --kubeconfig=/tmp/ci-kubeconfig.yaml rollout status deployment/my-app -n production
rm /tmp/ci-kubeconfig.yaml
```

## Kubeconfig Security Guidelines

1. **File Permissions**: Always set kubeconfig files to mode 600 (`chmod 600`)
2. **Short Duration**: Use minimum duration needed; prefer 1 day for CCE, 1 day for UCS federation
3. **Never Commit**: Never commit kubeconfig files to version control; add `*.kubeconfig.yaml` to `.gitignore`
4. **Cleanup**: Remove temporary kubeconfig files after use, especially in CI/CD
5. **Storage**: Store persistent kubeconfig files in `~/.kube/` with restricted permissions
6. **Context Verification**: Always verify `current-context` before executing destructive operations