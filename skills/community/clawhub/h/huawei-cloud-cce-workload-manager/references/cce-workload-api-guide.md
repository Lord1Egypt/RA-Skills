# CCE Workload Manager API Reference Guide

## Overview

This document provides API reference information for Huawei Cloud CCE workload management operations using hcloud CLI and kubectl. All hcloud commands follow the standard format: `hcloud CCE <Operation> --param=value --cli-region=<region>`. All kubectl commands require a valid kubeconfig: `kubectl --kubeconfig=<file> <command>`.

## Authentication

### Environment Variables

```bash
export HUAWEI_CLOUD_AK=<your-ak>
export HUAWEI_CLOUD_SK=<your-sk>
```

### hcloud CLI Configuration

```bash
hcloud configure

hcloud configure list
```

✅ **Correct**: Use `hcloud configure list` to verify credentials
❌ **Incorrect**: Never use `echo $HUAWEI_CLOUD_AK` to check credentials

## hcloud CCE Kubeconfig API

### 1. CreateKubernetesClusterCert — Obtain CCE Cluster Kubeconfig

```bash
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --project_id=<project-id> --cli-region=<region>
```

With optional duration:

```bash
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --project_id=<project-id> --duration=30 --cli-region=<region>
```

**Parameters**:

| Parameter        | Type     | Required | Description                                      |
| ---------------- | -------- | -------- | ------------------------------------------------ |
| `--cluster_id`   | string   | Yes (path) | CCE cluster UUID                              |
| `--project_id`   | string   | Yes      | Huawei Cloud project ID                          |
| `--duration`     | integer  | No (body) | Kubeconfig validity in days (1-1827)          |
| `--expire_at`    | string   | No       | Specific expiration timestamp                   |
| `--cli-region`   | string   | Yes      | Region where the CCE cluster resides             |

**Response**: Returns a Kubernetes kubeconfig YAML content that can be saved to a file for kubectl access.

```bash
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --project_id=<project-id> --duration=30 --cli-region=cn-north-4 > cce-kubeconfig.yaml

kubectl --kubeconfig=cce-kubeconfig.yaml get nodes
```

### 2. ListClusters — Find CCE Cluster IDs

```bash
hcloud CCE ListClusters --project_id=<project-id> --cli-region=<region>
```

With filter parameters:

```bash
hcloud CCE ListClusters --project_id=<project-id> --detail=true --status=Available --type=VirtualMachine --version=v1.28 --cli-region=<region>
```

**Parameters**:

| Parameter      | Type    | Required | Description                              |
| -------------- | ------- | -------- | ---------------------------------------- |
| `--project_id` | string  | Yes      | Huawei Cloud project ID                  |
| `--detail`     | boolean | No       | Return detailed cluster information      |
| `--status`     | string  | No       | Filter by cluster status                 |
| `--type`       | string  | No       | Filter by cluster type                   |
| `--version`    | string  | No       | Filter by Kubernetes version             |
| `--cli-region` | string  | Yes      | Region ID                                |

**Response Fields**:
- `id`: CCE cluster UUID (use as `--cluster_id` in other operations)
- `name`: Cluster display name
- `status`: Cluster status (`Available`, `Creating`, `Deleting`, etc.)
- `version`: Kubernetes version
- `type`: Cluster type (`VirtualMachine`, `BareMetal`, etc.)

### 3. ShowCluster — Verify CCE Cluster Status

```bash
hcloud CCE ShowCluster --cluster_id=<cce-cluster-id> --project_id=<project-id> --cli-region=<region>
```

With detail:

```bash
hcloud CCE ShowCluster --cluster_id=<cce-cluster-id> --project_id=<project-id> --detail=true --cli-region=<region>
```

**Parameters**:

| Parameter        | Type    | Required | Description                              |
| ---------------- | ------- | -------- | ---------------------------------------- |
| `--cluster_id`   | string  | Yes (path) | CCE cluster UUID                       |
| `--project_id`   | string  | Yes      | Huawei Cloud project ID                  |
| `--detail`       | boolean | No       | Return detailed cluster information      |
| `--cli-region`   | string  | Yes      | Region ID                                |

**Response Fields**:
- `id`: CCE cluster UUID
- `name`: Cluster display name
- `status.phase`: Cluster phase (`Available`, `Creating`, `Deleting`, `Unavailable`)
- `spec.version`: Kubernetes version
- `spec.type`: Cluster type
- `spec.flavor`: Cluster flavor (node configuration)

### 4. ShowClusterEndpoints — Get Cluster Access Addresses

```bash
hcloud CCE ShowClusterEndpoints --cluster_id=<cce-cluster-id> --project_id=<project-id> --cli-region=<region>
```

**Parameters**:

| Parameter        | Type    | Required | Description                              |
| ---------------- | ------- | -------- | ---------------------------------------- |
| `--cluster_id`   | string  | Yes (path) | CCE cluster UUID                       |
| `--project_id`   | string  | Yes      | Huawei Cloud project ID                  |
| `--cli-region`   | string  | Yes      | Region ID                                |

**Response Fields**:
- `externalEndpoint`: Public API server endpoint
- `internalEndpoint`: Private API server endpoint (VPC access)
- `externalOTCEndpoint`: OpenTelekomCloud endpoint (if applicable)

## hcloud UCS Kubeconfig API

### 1. CreateClusterKubeconfig — Obtain UCS-Managed Cluster Kubeconfig

```bash
hcloud UCS CreateClusterKubeconfig --clusterid=<ucs-cluster-id> --cli-region=cn-north-4
```

**Parameters**:

| Parameter      | Type   | Required | Description                              |
| -------------- | ------ | -------- | ---------------------------------------- |
| `--clusterid`  | string | Yes (path) | UCS cluster ID (no underscore)        |
| `--cli-region` | string | Yes      | Region ID                                |

**Response**: Returns a Kubernetes kubeconfig YAML content for kubectl access to the UCS-managed cluster.

### 2. DownloadFederationKubeconfig — Download Fleet Federation Kubeconfig

```bash
hcloud UCS DownloadFederationKubeconfig --clustergroupid=<group-id> --duration=1 --cli-region=cn-north-4
```

**Parameters**:

| Parameter         | Type    | Required | Description                                  |
| ----------------- | ------- | -------- | -------------------------------------------- |
| `--clustergroupid` | string | Yes (path) | Fleet group ID (no underscore)            |
| `--duration`      | integer | Yes      | Kubeconfig validity duration in days (1-1825)  |
| `--cli-region`    | string  | Yes      | Region ID                                    |

**Response**: Returns a federation kubeconfig YAML that provides unified kubectl access to all clusters in the fleet group.

### 3. ShowClusterList — Find UCS Cluster IDs

```bash
hcloud UCS ShowClusterList --cli-region=cn-north-4
```

**Response Fields**:
- `items[].metadata.uid`: UCS cluster UUID (use as `--clusterid`)
- `items[].metadata.name`: Cluster display name
- `items[].status.phase`: Cluster phase

### 4. ListClusterGroup — Find Fleet Group IDs

```bash
hcloud UCS ListClusterGroup --cli-region=cn-north-4
```

**Response Fields**:
- `id`: Fleet group UUID (use as `--clustergroupid`)
- `name`: Fleet group display name

## kubectl Command Reference

All kubectl commands require `--kubeconfig=<file>` and typically `-n <namespace>`.

### Common Flags

| Flag               | Description                              |
| ------------------ | ---------------------------------------- |
| `--kubeconfig=<f>` | Path to kubeconfig file                  |
| `-n <namespace>`   | Target namespace                         |
| `-o wide`          | Additional columns in output             |
| `-o yaml`          | YAML output format                       |
| `-o json`          | JSON output format                       |
| `-f <file>`        | Apply from file or directory             |

### Namespace Operations

```bash
kubectl --kubeconfig=<f> create namespace <name>
kubectl --kubeconfig=<f> get namespaces
kubectl --kubeconfig=<f> describe namespace <name>
kubectl --kubeconfig=<f> delete namespace <name>
```

### Deployment Operations

```bash
kubectl --kubeconfig=<f> create deployment <name> --image=<image> -n <ns>
kubectl --kubeconfig=<f> get deployments -n <ns> -o wide
kubectl --kubeconfig=<f> describe deployment <name> -n <ns>
kubectl --kubeconfig=<f> delete deployment <name> -n <ns>
kubectl --kubeconfig=<f> rollout status deployment/<name> -n <ns>
kubectl --kubeconfig=<f> rollout history deployment/<name> -n <ns>
kubectl --kubeconfig=<f> rollout undo deployment/<name> -n <ns>
kubectl --kubeconfig=<f> scale deployment/<name> --replicas=<N> -n <ns>
```

### StatefulSet Operations

```bash
kubectl --kubeconfig=<f> get statefulsets -n <ns> -o wide
kubectl --kubeconfig=<f> describe statefulset <name> -n <ns>
kubectl --kubeconfig=<f> delete statefulset <name> -n <ns>
kubectl --kubeconfig=<f> scale statefulset/<name> --replicas=<N> -n <ns>
```

### DaemonSet Operations

```bash
kubectl --kubeconfig=<f> get daemonsets -n <ns> -o wide
kubectl --kubeconfig=<f> describe daemonset <name> -n <ns>
kubectl --kubeconfig=<f> delete daemonset <name> -n <ns>
```

### Pod Operations

```bash
kubectl --kubeconfig=<f> get pods -n <ns> -o wide
kubectl --kubeconfig=<f> describe pod <name> -n <ns>
kubectl --kubeconfig=<f> logs <pod> -n <ns>
kubectl --kubeconfig=<f> logs <pod> --previous -n <ns>
kubectl --kubeconfig=<f> delete pod <name> -n <ns>
kubectl --kubeconfig=<f> exec -it <pod> -n <ns> -- <command>
```

### Service Operations

```bash
kubectl --kubeconfig=<f> get services -n <ns> -o wide
kubectl --kubeconfig=<f> describe service <name> -n <ns>
kubectl --kubeconfig=<f> delete service <name> -n <ns>
```

### ConfigMap & Secret Operations

```bash
kubectl --kubeconfig=<f> get configmaps -n <ns>
kubectl --kubeconfig=<f> describe configmap <name> -n <ns>
kubectl --kubeconfig=<f> get secrets -n <ns>
kubectl --kubeconfig=<f> describe secret <name> -n <ns>
```

### PVC & Storage Operations

```bash
kubectl --kubeconfig=<f> get pvc -n <ns>
kubectl --kubeconfig=<f> describe pvc <name> -n <ns>
kubectl --kubeconfig=<f> get pv
kubectl --kubeconfig=<f> get sc
```

### Apply & Delete from File

```bash
kubectl --kubeconfig=<f> apply -f deployment.yaml -n <ns>
kubectl --kubeconfig=<f> delete -f deployment.yaml -n <ns>
```

### RBAC Check

```bash
kubectl --kubeconfig=<f> auth can-i <verb> <resource> -n <ns>
kubectl --kubeconfig=<f> auth can-i create deployments -n prod
kubectl --kubeconfig=<f> auth can-i delete pods -n staging
```

## Common Errors

| Error                   | Cause                       | Solution                                        |
| ----------------------- | --------------------------- | ------------------------------------------------ |
| `InvalidAccessKeyId`    | Invalid AK/SK               | Check credential configuration via `hcloud configure list` |
| `CCE.001`               | Invalid parameter           | Check parameter format (CCE uses `--cluster_id` with underscore) |
| `CCE.002`               | Cluster not found           | Verify cluster_id with `hcloud CCE ListClusters` |
| `CCE.003`               | Cluster status unavailable  | Check cluster status with `ShowCluster`          |
| `CCE.ClusterNotFound`   | Invalid cluster UUID        | Use `hcloud CCE ListClusters` to find correct UUID |
| `KubeconfigExpired`     | Kubeconfig token expired    | Re-create with `CreateKubernetesClusterCert --duration=<days>` |
| `Forbidden (RBAC)`      | Insufficient RBAC           | Check with `kubectl auth can-i`, create RBAC bindings |
| `ConnectionRefused`     | API server unreachable      | Verify network, check `ShowClusterEndpoints`     |
| `NamespaceNotFound`     | Namespace does not exist    | Create with `kubectl create namespace <name>`    |
| `InvalidKubeconfig`     | Kubeconfig format invalid   | Re-download from CCE or UCS API                  |
| `UCS.001`               | Invalid UCS parameter       | UCS uses `--clusterid` (no underscore)           |
| `UCS.002`               | UCS cluster not found       | Use `ShowClusterList` to find UCS cluster ID     |

## Related Documentation

- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud UCS Documentation](https://support.huaweicloud.com/ucs/index.html)
- [hcloud CLI Documentation](https://support.huaweicloud.com/cli/index.html)
- [Huawei Cloud API Explorer](https://apiexplorer.developer.huaweicloud.com/)