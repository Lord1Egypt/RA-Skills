# Kafka Topologies Reference

## Combined Mode with Monitoring

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-combined-monitor
  namespace: demo
spec:
  clusterDef: kafka
  topology: combined_monitor
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
    - name: kafka-exporter
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

## Separated Mode with Monitoring (Full Production)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: kafka-prod
  namespace: demo
spec:
  clusterDef: kafka
  topology: separated_monitor
  terminationPolicy: DoNotTerminate
  componentSpecs:
    - name: kafka-broker
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "2", memory: "4Gi"}
        requests: {cpu: "2", memory: "4Gi"}
      env:
        - name: KB_KAFKA_BROKER_HEAP
          value: "-Xmx2g -Xms2g"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 100Gi}}
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 10Gi}}
    - name: kafka-controller
      serviceVersion: "3.3.2"
      replicas: 3
      resources:
        limits: {cpu: "1", memory: "2Gi"}
        requests: {cpu: "1", memory: "2Gi"}
      env:
        - name: KB_KAFKA_CONTROLLER_HEAP
          value: "-Xmx1g -Xms1g"
      volumeClaimTemplates:
        - name: metadata
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 10Gi}}
    - name: kafka-exporter
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

## Environment Variables

| Variable | Description | Default | Notes |
|---|---|---|---|
| `KB_KAFKA_BROKER_HEAP` | Broker JVM heap | `-Xmx256m -Xms256m` | Set to ~60% of container memory limit |
| `KB_KAFKA_CONTROLLER_HEAP` | Controller JVM heap | `-Xmx256m -Xms256m` | Controllers need less memory than brokers |
| `KB_KAFKA_ENABLE_SASL` | Enable SASL auth | (unset) | Set to `true` for authentication |
| `KB_KAFKA_PUBLIC_ACCESS` | External access mode | (unset) | Set to `true` for NodePort/LB exposure |

## Topology Component and Volume Matrix

| Topology | Components | Volumes per Component |
|---|---|---|
| `combined` | kafka-combine | data + metadata |
| `combined_monitor` | kafka-combine, kafka-exporter | data + metadata (combine only) |
| `separated` | kafka-broker, kafka-controller | broker: data + metadata; controller: metadata only |
| `separated_monitor` | kafka-broker, kafka-controller, kafka-exporter | same as separated |

Key points:
- Brokers store message data (`data`) and cluster metadata (`metadata`)
- Controllers only store metadata — they don't hold message data
- 3 controller replicas are required for KRaft consensus (Raft majority quorum)
- Exporter components have no volumes — they only scrape and expose metrics
