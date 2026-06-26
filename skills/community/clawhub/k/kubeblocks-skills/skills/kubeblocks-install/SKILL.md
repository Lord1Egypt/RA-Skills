---
name: kubeblocks-install
metadata:
  version: "0.1.0"
description: Install the KubeBlocks operator on any Kubernetes cluster via Helm. Handles version selection, environment detection (local dev vs production, China mainland vs global network), image registry configuration, prerequisite checks, and post-install verification. Use when the user asks to install, deploy, or set up KubeBlocks. NOT for upgrading an existing KubeBlocks installation (see KubeBlocks official upgrade docs), uninstalling KubeBlocks (see the Uninstall section in this skill), or creating database clusters after installation (see kubeblocks-create-cluster or kubeblocks-addon-* skills).
---

# Install KubeBlocks Operator

## Overview

KubeBlocks is a Kubernetes operator for managing databases (MySQL, PostgreSQL, Redis, MongoDB, Kafka, etc.). This skill guides installation of the KubeBlocks operator onto any Kubernetes cluster.

Official docs: https://kubeblocks.io/docs/preview/user_docs/overview/install-kubeblocks
Full doc index: https://kubeblocks.io/llms-full.txt

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Check prerequisites
- [ ] Step 2: Determine version
- [ ] Step 3: Detect network environment
- [ ] Step 4: Install CRDs
- [ ] Step 5: Install KubeBlocks via Helm
- [ ] Step 6: Verify installation
```

## Step 1: Check Prerequisites

This skill requires an **existing Kubernetes cluster**. If the user does not have one, point them to the [create-local-k8s-cluster](../kubeblocks-create-local-k8s-cluster/SKILL.md) skill first.

Run these checks and **install any missing tools automatically**:

### 1a: kubectl

```bash
kubectl version --client 2>/dev/null
```

If the command fails (not found), install it:

```bash
# macOS
brew install kubectl

# Linux (amd64)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/

# Linux (arm64)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
```

### 1b: Helm (v3+)

```bash
helm version --short 2>/dev/null
```

If the command fails (not found), install it:

```bash
# macOS
brew install helm

# Linux (script, works on amd64/arm64)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 1c: Verify cluster access

```bash
kubectl get nodes
```

If this fails, the user has no accessible Kubernetes cluster. **Stop here** and tell the user:
- For local testing, use the [create-local-k8s-cluster](../kubeblocks-create-local-k8s-cluster/SKILL.md) skill
- For production, ensure kubeconfig is properly configured (`~/.kube/config` or `$KUBECONFIG`)

**Resource requirements** (minimum):
- Control Plane: 1 node, 4 cores, 4GB RAM, 50GB storage
- Data Plane: 2-3 nodes, 2 cores, 4GB RAM, 50GB storage each

## Step 2: Determine Version

Ask the user if they want a specific version. If not specified, fetch the latest stable release:

```bash
# Get latest stable version
curl -s https://api.github.com/repos/apecloud/kubeblocks/releases/latest | grep '"tag_name"' | cut -d'"' -f4
```

To list all available versions:

```bash
# Via GitHub API
curl -s https://api.github.com/repos/apecloud/kubeblocks/tags | grep '"name"' | head -20 | cut -d'"' -f4

# Or via Helm (after adding repo)
helm search repo kubeblocks/kubeblocks --versions
```

Known stable releases: v1.0.2, v1.0.1, v1.0.0, v0.9.5, v0.9.4, v0.9.3, v0.9.2, v0.9.1, v0.9.0

**Always tell the user which version is being installed.**

## Step 3: Detect Network Environment

Determine which image registry to use.

**Default (global access / docker.io available):**
- registry: `docker.io`
- namespace: `apecloud`

**China mainland (docker.io blocked/slow):**
- registry: `apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com`
- namespace: `apecloud`

**How to detect:** Ask the user, or run a quick test:

```bash
# Test docker.io connectivity (timeout 5s)
curl -sS --connect-timeout 5 https://registry-1.docker.io/v2/ > /dev/null 2>&1 && echo "docker.io: reachable" || echo "docker.io: unreachable, use China mirror"
```

## Step 4: Install CRDs

```bash
# Replace {VERSION} with the chosen version, e.g. v1.0.2
kubectl create -f https://github.com/apecloud/kubeblocks/releases/download/{VERSION}/kubeblocks_crds.yaml
```

**For K8s <= 1.23**, add `--validate=false`:

```bash
kubectl create -f https://github.com/apecloud/kubeblocks/releases/download/{VERSION}/kubeblocks_crds.yaml --validate=false
```

## Step 5: Install KubeBlocks via Helm

### 5a: Add Helm Repo

```bash
helm repo add kubeblocks https://apecloud.github.io/helm-charts
helm repo update
```

### 5b: Install

**Global network (docker.io accessible):**

```bash
helm install kubeblocks kubeblocks/kubeblocks \
  --namespace kb-system --create-namespace \
  --version {VERSION} \
  --set image.registry=docker.io \
  --set dataProtection.image.registry=docker.io \
  --set addonChartsImage.registry=docker.io
```

**China mainland network:**

```bash
helm install kubeblocks kubeblocks/kubeblocks \
  --namespace kb-system --create-namespace \
  --version {VERSION} \
  --set image.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com \
  --set dataProtection.image.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com \
  --set addonChartsImage.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com
```

### Common Extra Options

```bash
# Custom tolerations (e.g. for dedicated control-plane nodes)
--set-json 'tolerations=[{"key":"control-plane-taint","operator":"Equal","effect":"NoSchedule","value":"true"}]'

# Skip auto-installing default addons (lightweight install)
--set autoInstalledAddons="{}"

# Enable in-place vertical scaling
--set featureGates.inPlacePodVerticalScaling.enabled=true
```

For the full options reference, see [reference.md](references/reference.md).

## Step 6: Verify Installation

```bash
# Check pods in kb-system namespace
kubectl -n kb-system get pods

# Expected: kubeblocks and kubeblocks-dataprotection pods in Running state
# Example output:
# NAME                                             READY   STATUS    RESTARTS   AGE
# kubeblocks-7cf7745685-ddlwk                      1/1     Running   0          2m
# kubeblocks-dataprotection-95fbc79cc-b544l        1/1     Running   0          2m
```

If pods are not Running, check events:

```bash
kubectl -n kb-system describe pods
kubectl -n kb-system get events --sort-by='.lastTimestamp'
```

## Troubleshooting

**CRD install fails with `x-kubernetes-validations` error:**
- K8s version <= 1.23. Add `--validate=false` to the `kubectl create` command.

**Image pull errors:**
- Check registry accessibility. Switch to the China mainland mirror if in China.
- Verify the registry setting: `helm get values kubeblocks -n kb-system`

**Helm install timeout:**
- Check node resources: `kubectl describe nodes`
- For resource-constrained environments, skip default addons: `--set autoInstalledAddons="{}"`

**KubeBlocks already installed:**
- Check existing installation: `helm list -n kb-system | grep kubeblocks`
- To upgrade: `helm upgrade kubeblocks kubeblocks/kubeblocks --namespace kb-system --version {VERSION}`

## Uninstall

See [reference.md](references/reference.md) for detailed uninstall instructions.

Quick uninstall:

```bash
# Delete all clusters and backups first
kubectl get cluster -A
kubectl delete cluster --all -A

# Uninstall addons
helm list -n kb-system | grep kb-addon | awk '{print $1}' | xargs -I {} helm -n kb-system uninstall {}

# Uninstall KubeBlocks
helm uninstall kubeblocks --namespace kb-system

# Remove CRDs
kubectl get crd -o name | grep kubeblocks.io | xargs kubectl delete
```
