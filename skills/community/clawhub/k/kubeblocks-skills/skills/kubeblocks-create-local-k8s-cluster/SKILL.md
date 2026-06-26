---
name: kubeblocks-create-local-k8s-cluster
metadata:
  version: "0.1.0"
description: Create a local Kubernetes test cluster using Kind, Minikube, or k3d. Handles tool installation, cluster creation, multi-node configuration, and verification. Use when the user needs a local K8s cluster for testing or development, or when they have no existing Kubernetes cluster. NOT for production cluster provisioning (use cloud provider tools like EKS, AKS, GKE) or for installing KubeBlocks (see kubeblocks-install).
---

# Create a Local Kubernetes Test Cluster

## Overview

Create a local Kubernetes cluster for development and testing using Kind, Minikube, or k3d. All three tools run K8s inside Docker containers on the local machine.

Official docs: https://kubeblocks.io/docs/preview/user_docs/references/prepare-a-local-k8s-cluster

## Tool Comparison

| Feature | Kind | Minikube | k3d |
|---------|------|----------|-----|
| Engine | K8s in Docker | VM or Docker | k3s in Docker |
| Multi-node | Yes (via config) | Limited | Yes (via flags) |
| Resource usage | Low | Medium | Low |
| Startup speed | Fast | Slower | Fast |
| Best for | CI/CD, testing | Learning, local dev | Lightweight testing |

**Default recommendation:** Kind (widely used, lightweight, supports multi-node easily).

## Workflow

```
- [ ] Step 1: Check Docker is running
- [ ] Step 2: Choose and install a tool
- [ ] Step 3: Create a cluster
- [ ] Step 4: Verify the cluster
```

## Step 1: Check Docker

All three tools require Docker. Verify it is installed and running:

```bash
docker info > /dev/null 2>&1
```

If Docker is not available, tell the user to install it first:
- macOS/Windows: https://www.docker.com/products/docker-desktop/
- Linux: https://docs.docker.com/engine/install/

## Step 2: Choose and Install a Tool

Ask the user which tool they prefer. If no preference, default to **Kind**.

### Kind

```bash
# macOS
brew install kind

# Linux (amd64)
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Linux (arm64)
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-arm64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Windows
choco install kind
```

### Minikube

```bash
# macOS
brew install minikube

# Linux (rpm-based)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-latest.x86_64.rpm
sudo rpm -Uvh minikube-latest.x86_64.rpm

# Linux (deb-based)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

# Windows
choco install minikube
```

### k3d

```bash
# macOS
brew install k3d

# Linux
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Windows
choco install k3d
```

## Step 3: Create a Cluster

### Kind (default)

**Single-node cluster (simplest):**

```bash
kind create cluster --name kb-test
```

**Multi-node cluster (recommended for KubeBlocks):**

Create a config file `kind-config.yaml`:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

Then create the cluster:

```bash
kind create cluster --name kb-test --config kind-config.yaml
```

### Minikube

```bash
# Single-node (default)
minikube start

# With Docker driver (recommended)
minikube start --driver=docker

# With more resources
minikube start --driver=docker --cpus=4 --memory=8192
```

### k3d

```bash
# Single-node
k3d cluster create kb-test

# Multi-node (1 server + 2 agents)
k3d cluster create kb-test --servers 1 --agents 2
```

## Step 4: Verify the Cluster

```bash
kubectl get nodes
```

Expected output (Kind multi-node example):

```
NAME                    STATUS   ROLES           AGE   VERSION
kb-test-control-plane   Ready    control-plane   30s   v1.31.0
kb-test-worker          Ready    <none>          20s   v1.31.0
kb-test-worker2         Ready    <none>          20s   v1.31.0
```

Also verify kubectl context is set correctly:

```bash
kubectl config current-context
```

## Delete the Cluster

When the cluster is no longer needed:

```bash
# Kind
kind delete cluster --name kb-test

# Minikube
minikube delete

# k3d
k3d cluster delete kb-test
```

## Next Steps

Once the cluster is running, you can install KubeBlocks using the [install-kubeblocks](../kubeblocks-install/SKILL.md) skill.
