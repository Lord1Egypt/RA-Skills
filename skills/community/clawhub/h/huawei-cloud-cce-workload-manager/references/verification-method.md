# Verification Method - CCE Workload Manager Skill

## Overview

This document defines the verification steps for the CCE Workload Manager skill. Verification is divided into six levels: installation verification, configuration verification, kubeconfig acquisition, connectivity verification, read-only operations, and write operations.

## Level 1: Installation Verification

### 1.1 hcloud CLI Installation

| Item                 | Command           | Success Criteria                          |
| -------------------- | ------------------ | ----------------------------------------- |
| hcloud installed     | `hcloud version`   | Returns version number >= 7.2.2           |

### 1.2 hcloud CLI First Run

```bash
printf "y\n" | hcloud version
```

Expected: Version number displayed without error.

### 1.3 kubectl Installation

| Item                 | Command                | Success Criteria                          |
| -------------------- | ---------------------- | ----------------------------------------- |
| kubectl installed    | `kubectl version --client` | Returns Kubernetes client version |

If kubectl is not installed, follow the installation guide in [kubectl Setup](task-kubectl-setup.md).

**Official Download**: https://kubernetes.io/docs/tasks/tools/

**Quick Install (Linux)**:
```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/' | sed 's/aarch64/arm64/')
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/${ARCH}/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

**Quick Install (Windows)**:
```powershell
$version = (Invoke-WebRequest -Uri "https://dl.k8s.io/release/stable.txt" -UseBasicParsing).Content.Trim()
$arch = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { 'arm64' } else { 'amd64' }
curl -LO "https://dl.k8s.io/release/$version/bin/windows/$arch/kubectl.exe"
```

## Level 2: Configuration Verification

### 2.1 Credential Configuration

| Item                    | Command                | Success Criteria                        |
| ----------------------- | ---------------------- | --------------------------------------- |
| Credentials configured  | `hcloud configure list` | Shows valid AK/SK configuration (values masked) |

Never use `echo $HUAWEI_CLOUD_AK` to check credentials.

## Level 3: Kubeconfig Acquisition

### 3.1 Find CCE Cluster ID

```bash
hcloud CCE ListClusters --cli-region=cn-north-4
```

Expected: Returns list of CCE clusters with `metadata.uid` field.

### 3.2 Obtain CCE Cluster Kubeconfig

```bash
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --duration=1 --cli-region=cn-north-4 > ~/.kube/cce-test-kubeconfig.yaml
```

Expected: kubeconfig YAML file created with clusters, contexts, and users sections.

### 3.3 Verify Kubeconfig Content

```bash
cat ~/.kube/cce-test-kubeconfig.yaml
```

Expected: Contains `apiVersion: v1`, `kind: Config`, `clusters`, `contexts`, `users` sections.

## Level 4: Connectivity Verification

### 4.1 Test Cluster Connectivity

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml cluster-info
```

Expected: Returns cluster information (API server URL, Kubernetes version).

### 4.2 Check Node Status

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml get nodes
```

Expected: Returns list of cluster nodes with `STATUS` = `Ready`.

## Level 5: Read-Only Operations

### 5.1 List Namespaces

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml get namespaces
```

Expected: Returns namespace list including `default`, `kube-system`.

### 5.2 List All Pods

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml get pods -A
```

Expected: Returns pods across all namespaces.

### 5.3 Check RBAC Permissions

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml auth can-i create deployments -n default
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml auth can-i list pods -n default
```

Expected: Returns `yes` or `no` based on RBAC permissions.

## Level 6: Write Operations (Test Namespace)

### CCE StorageClass Reference

CCE clusters provide the following StorageClasses for PVC creation. Use `csi-disk` for general block storage (the most common choice):

| StorageClass | Type | Use Case |
|-------------|------|----------|
| `csi-disk` | Cloud disk (EVS) | General block storage (recommended default) |
| `csi-disk-topology` | Cloud disk with topology | Cross-AZ scheduling with delayed binding |
| `csi-disk-dss` | Dedicated storage disk | DSS pool storage |
| `csi-sfsturbo` | SFS Turbo (extreme file storage) | High-performance shared file storage (500Gi min, supports subdirectory) |
| `csi-nas` | General file storage (SFS) | Shared file storage |
| `csi-obs` | Object storage (OBS) | Object storage mount (obsfs/s3fs) |
| `csi-sfs` | SFS 3.0 capacity | High-bandwidth shared storage |
| `csi-sfsturbo` subdirectory | SFS Turbo subdirectory | Cost-effective shared storage with quota control |

> **Important**: `cce-standard` is NOT a valid CCE StorageClass. Always use `csi-disk` or one of the CSI StorageClasses listed above. Run `kubectl get sc` to verify available StorageClasses in your cluster.

For SFS Turbo subdirectory PVCs (recommended for cost savings), see the [task-config-secret-storage.md](task-config-secret-storage.md) reference.

To check available StorageClasses in your cluster:

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml get storageclasses
```

### metrics-server Prerequisite

`kubectl top pods` and `kubectl top nodes` require the metrics-server addon. If not installed:

```bash
# Check if metrics-server is available
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml top pods -n default
# If returns "Metrics API not available", install the addon via CCE console or hcloud
```

### 6.1 Create Test Namespace

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml create namespace workload-test
```

Expected: Namespace `workload-test` created.

### 6.2 Deploy Test Workload

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml create deployment nginx-test --image=nginx:1.25 --replicas=1 -n workload-test
```

Expected: Deployment `nginx-test` created.

### 6.3 Verify Deployment

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml get deployments -n workload-test
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml get pods -n workload-test
```

Expected: Deployment shows 1/1 READY, Pod shows Running status.

### 6.4 Scale Deployment

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml scale deployment nginx-test --replicas=3 -n workload-test
```

Expected: Deployment scaled to 3 replicas.

### 6.5 View Pod Logs

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml logs -l app=nginx-test -n workload-test --tail=10
```

Expected: Returns nginx access logs or startup output.

## Level 7: Clean Up

### 7.1 Delete Test Resources

```bash
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml delete deployment nginx-test -n workload-test
kubectl --kubeconfig=~/.kube/cce-test-kubeconfig.yaml delete namespace workload-test
```

Expected: Test deployment and namespace deleted.

### 7.2 Remove Kubeconfig

```bash
rm ~/.kube/cce-test-kubeconfig.yaml
```

Expected: Kubeconfig file removed (security best practice).

## Verification Checklist

| #  | Check Item                | Command                                             | Status |
| -- | ------------------------- | --------------------------------------------------- | ------ |
| 1  | hcloud version >= 7.2.2   | `hcloud version`                                    | ☐      |
| 2  | kubectl installed         | `kubectl version --client`                          | ☐      |
| 3  | Credentials configured    | `hcloud configure list`                             | ☐      |
| 4  | Find CCE cluster          | `hcloud CCE ListClusters --cli-region=cn-north-4`   | ☐      |
| 5  | Obtain kubeconfig         | `hcloud CCE CreateKubernetesClusterCert --cluster_id=<id> --duration=1 --cli-region=cn-north-4` | ☐ |
| 6  | Test connectivity         | `kubectl --kubeconfig=<f> cluster-info`             | ☐      |
| 7  | Check nodes               | `kubectl --kubeconfig=<f> get nodes`                | ☐      |
| 8  | List namespaces           | `kubectl --kubeconfig=<f> get namespaces`           | ☐      |
| 9  | Check RBAC                | `kubectl --kubeconfig=<f> auth can-i create deployments` | ☐ |
| 10 | Create test namespace     | `kubectl --kubeconfig=<f> create namespace workload-test` | ☐ |
| 11 | Deploy test workload      | `kubectl --kubeconfig=<f> create deployment nginx-test --image=nginx:1.25 -n workload-test` | ☐ |
| 12 | Verify deployment         | `kubectl --kubeconfig=<f> get deployments -n workload-test` | ☐ |
| 13 | Scale deployment          | `kubectl --kubeconfig=<f> scale deployment nginx-test --replicas=3 -n workload-test` | ☐ |
| 14 | View logs                 | `kubectl --kubeconfig=<f> logs -l app=nginx-test -n workload-test` | ☐ |
| 15 | Delete test resources     | `kubectl --kubeconfig=<f> delete deployment nginx-test -n workload-test` | ☐ |
| 16 | Delete test namespace     | `kubectl --kubeconfig=<f> delete namespace workload-test` | ☐ |
| 17 | Remove kubeconfig         | `rm ~/.kube/cce-test-kubeconfig.yaml`               | ☐      |