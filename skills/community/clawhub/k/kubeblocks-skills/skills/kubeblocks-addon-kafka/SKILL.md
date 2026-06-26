---
name: kubeblocks-addon-kafka
metadata:
  version: "0.1.0"
description: Deploy and manage Apache Kafka clusters on KubeBlocks with topology selection guidance. Supports combined mode (broker + controller co-located) and separated mode (dedicated broker and controller nodes) with optional monitoring exporter. Use when the user mentions Kafka, message queue, event streaming, message broker, or explicitly wants to create a Kafka cluster. Provides topology comparison, best-practice defaults, and connection methods. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, etc.), use the corresponding operation skill.
---

# Deploy Kafka on KubeBlocks

## Overview

Deploy Apache Kafka clusters on Kubernetes using KubeBlocks. Supports combined mode (broker + controller in one process) and separated mode (dedicated broker and controller nodes) with optional monitoring via exporter.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/create-a-kafka-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The Kafka addon must be enabled:

```bash
# Check if kafka addon is installed
helm list -n kb-system | grep kafka

# Install if missing
helm install kb-addon-kafka kubeblocks/kafka --namespace kb-system --version 1.0.0
```

## Available Topologies

| Topology | Value | Components | Use Case |
|---|---|---|---|
| Combined | `combined` | kafka-combine | Dev/test, broker+controller in one |
| Combined + Monitor | `combined_monitor` | kafka-combine + exporter | Combined with metrics |
| Separated | `separated` | kafka-broker + kafka-controller | Production, dedicated roles |
| Separated + Monitor | `separated_monitor` | kafka-broker + kafka-controller + exporter | Production with metrics |

Kafka uses KRaft mode (no ZooKeeper dependency). Controllers manage cluster metadata via the Raft protocol.

## Supported Versions

| Version | serviceVersion |
|---|---|
| Kafka 3.3 | `3.3.2` |

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (choose topology)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Produce and consume messages
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep kafka
```

If not found:

```bash
helm install kb-addon-kafka kubeblocks/kafka --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

### Combined Mode (Dev/Test)

Broker and controller run in the same process. Simpler but not recommended for production:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-cluster
  namespace: demo
spec:
  clusterDef: kafka
  topology: combined
  terminationPolicy: Delete
  componentSpecs:
    - name: kafka-combine
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_BROKER_HEAP
          value: "-Xmx256m -Xms256m"
        - name: KB_KAFKA_CONTROLLER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
```

### Separated Mode (Production)

Dedicated broker and controller nodes for better isolation and scalability:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-separated
  namespace: demo
spec:
  clusterDef: kafka
  topology: separated
  terminationPolicy: Delete
  componentSpecs:
    - name: kafka-broker
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_BROKER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
    - name: kafka-controller
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_CONTROLLER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
```

**Key points:**
- Brokers need both `data` and `metadata` volumes
- Controllers only need a `metadata` volume (they don't store message data)
- 3 controller replicas for Raft consensus

### Separated Mode with Monitoring

Add an exporter component for Prometheus-compatible metrics:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-monitored
  namespace: demo
spec:
  clusterDef: kafka
  topology: separated_monitor
  terminationPolicy: Delete
  componentSpecs:
    - name: kafka-broker
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_BROKER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
    - name: kafka-controller
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      env:
        - name: KB_KAFKA_CONTROLLER_HEAP
          value: "-Xmx256m -Xms256m"
      volumeClaimTemplates:
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 5Gi}}
    - name: kafka-exporter
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

## Environment Variables

Kafka configuration can be tuned via environment variables on the component spec:

| Variable | Description | Example |
|---|---|---|
| `KB_KAFKA_BROKER_HEAP` | Broker JVM heap settings | `-Xmx512m -Xms512m` |
| `KB_KAFKA_CONTROLLER_HEAP` | Controller JVM heap settings | `-Xmx256m -Xms256m` |
| `KB_KAFKA_ENABLE_SASL` | Enable SASL authentication | `true` |
| `KB_KAFKA_PUBLIC_ACCESS` | Enable external access mode | `true` |

## Step 4: Wait for Cluster Ready

```bash
kubectl -n demo get cluster <cluster-name> -w
```

Wait until `STATUS` shows `Running`. Kafka clusters typically take 2-4 minutes.

Check pods:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```

## Step 5: Produce and Consume Messages

### Create a Topic

```bash
kubectl -n demo exec -it kafka-cluster-kafka-combine-0 -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic --partitions 3 --replication-factor 1
```

### Produce Messages

```bash
kubectl -n demo exec -it kafka-cluster-kafka-combine-0 -- \
  kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test-topic
```

### Consume Messages

```bash
kubectl -n demo exec -it kafka-cluster-kafka-combine-0 -- \
  kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```

### For Separated Mode

Replace the pod name with the broker pod:

```bash
kubectl -n demo exec -it kafka-separated-kafka-broker-0 -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --list
```

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Broker not starting:**
```bash
kubectl -n demo logs <broker-pod>
```

**Controller quorum issues:**
- Ensure exactly 3 controller replicas for Raft consensus
- Check controller logs for election errors

**Out of memory:**
- Adjust heap settings via `KB_KAFKA_BROKER_HEAP` / `KB_KAFKA_CONTROLLER_HEAP` environment variables
- Ensure container memory limits are larger than heap size

## Day-2 Operations

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/stop-start-restart-a-kafka-cluster) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/scale-for-a-kafka-cluster) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/scale-for-a-kafka-cluster) |
| Expand storage | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/cluster-management/expand-volume-of-a-kafka-cluster) |
| Change parameters | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-kafka/configuration/configure-cluster-parameters) |

## Safety Patterns

Follow [safety-patterns.md](../../references/safety-patterns.md) for dry-run before apply, status confirmation after watch, and pre-deletion checklist.

## Next Steps

- For full YAML examples of all topologies (combined_monitor, separated_monitor with production sizing), environment variable reference, and component/volume matrix, see [reference.md](references/reference.md)
