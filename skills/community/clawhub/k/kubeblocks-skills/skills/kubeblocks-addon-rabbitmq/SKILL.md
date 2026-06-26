---
name: kubeblocks-addon-rabbitmq
metadata:
  version: "0.1.0"
description: Deploy and manage RabbitMQ clusters on KubeBlocks. RabbitMQ is an open-source message broker supporting AMQP, MQTT, and STOMP protocols. Use when the user mentions RabbitMQ, message broker, AMQP, message queue, or explicitly wants to create a RabbitMQ cluster. Provides cluster creation, connection methods (Management UI, rabbitmqctl), and Day-2 operations. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, etc.), use the corresponding operation skill.
---

# Deploy RabbitMQ on KubeBlocks

## Overview

Deploy RabbitMQ clusters on Kubernetes using KubeBlocks. RabbitMQ is a lightweight message broker supporting AMQP, MQTT, and STOMP. Multiple replicas form a cluster with queue mirroring and quorum queues. Default ports: 5672 (AMQP), 15672 (Management UI), 15692 (Prometheus metrics).

Official docs: https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/01-overview
Quickstart: https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/02-quickstart

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The RabbitMQ addon must be enabled:

```bash
# Check if rabbitmq addon is installed
helm list -n kb-system | grep rabbitmq

# Install if missing
helm install kb-addon-rabbitmq kubeblocks/rabbitmq --namespace kb-system --version 1.0.0
```

## Topology

| Topology | Value | Component | Use Case |
|---|---|---|---|
| Cluster Mode | `clustermode` | rabbitmq | Single topology; multiple replicas form a cluster with queue mirroring/quorum queues |

## Supported Versions

| Version | serviceVersion |
|---|---|
| RabbitMQ 3.8 | `3.8.34` |
| RabbitMQ 3.9 | `3.9.29` |
| RabbitMQ 3.10 | `3.10.25` |
| RabbitMQ 3.11 | `3.11.28` |
| RabbitMQ 3.12 | `3.12.14` |
| RabbitMQ 3.13 | `3.13.7` |
| RabbitMQ 4.0 | `4.0.9` |
| RabbitMQ 4.1 | `4.1.6` |
| RabbitMQ 4.2 | `4.2.1` |

List available versions: `kubectl get cmpv rabbitmq`

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (dry-run, then apply)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect (Management UI or rabbitmqctl)
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep rabbitmq
```

If not found:

```bash
helm install kb-addon-rabbitmq kubeblocks/rabbitmq --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: rabbitmq-cluster
  namespace: demo
spec:
  clusterDef: rabbitmq
  topology: clustermode
  terminationPolicy: Delete
  componentSpecs:
    - name: rabbitmq
      serviceVersion: "3.13.7"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

**Dry-run before apply:**

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

If dry-run succeeds:

```bash
kubectl apply -f cluster.yaml
```

## Step 4: Wait for Cluster Ready

```bash
kubectl -n demo get cluster rabbitmq-cluster -w
```

**Success condition:** `STATUS` shows `Running`. Typical duration: 1-2 minutes. Investigate after 10 min if stuck.

Check pods:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=rabbitmq-cluster
```

## Step 5: Connect

### Management UI (port-forward)

Credentials are in Secret `<clusterName>-<componentName>-account-root` (e.g. `rabbitmq-cluster-rabbitmq-account-root`):

```bash
# Get credentials
NAME=$(kubectl get secrets -n demo rabbitmq-cluster-rabbitmq-account-root -o jsonpath='{.data.username}' | base64 -d)
PASSWD=$(kubectl get secrets -n demo rabbitmq-cluster-rabbitmq-account-root -o jsonpath='{.data.password}' | base64 -d)

# Port-forward Management UI (port 15672)
kubectl port-forward svc/rabbitmq-cluster-rabbitmq -n demo 15672:15672
```

Access `http://localhost:15672` and log in with the credentials.

### rabbitmqctl (CLI)

```bash
kubectl -n demo exec -it rabbitmq-cluster-rabbitmq-0 -- rabbitmqctl cluster_status
```

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster rabbitmq-cluster
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Pod not starting:**
```bash
kubectl -n demo logs rabbitmq-cluster-rabbitmq-0
```

**Cluster formation issues:**
- Ensure odd number of replicas (3, 5, 7) for quorum
- Check peer discovery; KubeBlocks creates SA with required privileges

## Day-2 Operations

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/01-stop-start-restart) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/02-vertical-scaling) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/03-horizontal-scaling) |
| Expand storage | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/04-volume-expansion) |
| Expose externally | [expose-service](../kubeblocks-expose-service/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-rabbitmq/04-operations/) |

## Safety Patterns

Follow [safety-patterns](../../references/safety-patterns.md): dry-run before apply, confirm status after apply, pre-deletion checklist for delete.
