# KubeBlocks Addons Reference

Complete list of supported database addons and their feature compatibility.

Source: https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons

## Supported Addons by Category

### Relational Databases

| Addon | Engine | Helm Chart Name |
|---|---|---|
| MySQL | MySQL Community | `mysql` |
| ApeCloud MySQL | ApeCloud MySQL (Raft-based HA) | `apecloud-mysql` |
| MariaDB | MariaDB | `mariadb` |
| PostgreSQL | PostgreSQL (with Patroni HA) | `postgresql` |
| Vanilla PostgreSQL | PostgreSQL (single-node, no HA) | `vanilla-postgresql` |
| OrioleDB | OrioleDB (PostgreSQL-based) | `orioledb` |

### NoSQL Databases

| Addon | Engine | Helm Chart Name |
|---|---|---|
| MongoDB | MongoDB | `mongodb` |
| Redis | Redis | `redis` |
| etcd | etcd | `etcd` |
| ZooKeeper | Apache ZooKeeper | `zookeeper` |

### OLAP & Search

| Addon | Engine | Helm Chart Name |
|---|---|---|
| Elasticsearch | Elasticsearch | `elasticsearch` |
| OpenSearch | OpenSearch | `opensearch` |
| StarRocks CE | StarRocks Community Edition | `starrocks-ce` |
| ClickHouse | ClickHouse | `clickhouse` |

### Distributed SQL

| Addon | Engine | Helm Chart Name |
|---|---|---|
| TiDB | TiDB (PingCAP) | `tidb` |
| OceanBase CE | OceanBase Community Edition | `oceanbase-ce` |
| PolarDB-X | PolarDB-X (Alibaba) | `polardb-x` |

### Message Queues & Streaming

| Addon | Engine | Helm Chart Name |
|---|---|---|
| Kafka | Apache Kafka | `kafka` |
| RabbitMQ | RabbitMQ | `rabbitmq` |
| Pulsar | Apache Pulsar | `pulsar` |

### Vector Databases

| Addon | Engine | Helm Chart Name |
|---|---|---|
| Qdrant | Qdrant | `qdrant` |
| Weaviate | Weaviate | `weaviate` |
| Milvus | Milvus | `milvus` |

### Time Series Databases

| Addon | Engine | Helm Chart Name |
|---|---|---|
| InfluxDB | InfluxDB | `influxdb` |
| VictoriaMetrics | VictoriaMetrics | `victoria-metrics` |
| GreptimeDB | GreptimeDB | `greptimedb` |
| TDengine | TDengine | `tdengine` |

### Graph Databases

| Addon | Engine | Helm Chart Name |
|---|---|---|
| NebulaGraph | NebulaGraph | `nebula` |

### Object Storage

| Addon | Engine | Helm Chart Name |
|---|---|---|
| MinIO | MinIO | `minio` |

## Feature Compatibility Matrix

The table below shows which KubeBlocks operations are supported for each major addon. Features may vary by topology (e.g., standalone vs. replication vs. cluster mode).

**Legend:** Y = Supported, N = Not supported, - = Not applicable

### Relational Databases

| Feature | MySQL | ApeCloud MySQL | PostgreSQL | MariaDB |
|---|---|---|---|---|
| Vertical Scaling | Y | Y | Y | Y |
| Horizontal Scaling | Y | Y | Y | N |
| Volume Expansion | Y | Y | Y | Y |
| Stop/Start | Y | Y | Y | Y |
| Restart | Y | Y | Y | Y |
| Backup | Y | Y | Y | N |
| Restore | Y | Y | Y | N |
| Point-in-Time Recovery | Y | Y | Y | N |
| Reconfigure Parameters | Y | Y | Y | Y |
| Switchover | Y | Y | Y | N |
| Minor Version Upgrade | Y | Y | Y | N |
| Monitoring | Y | Y | Y | Y |
| Accounts Management | Y | Y | Y | Y |
| TLS | N | Y | Y | N |

### NoSQL Databases

| Feature | MongoDB | Redis | etcd |
|---|---|---|---|
| Vertical Scaling | Y | Y | Y |
| Horizontal Scaling | Y | Y | Y |
| Volume Expansion | Y | Y | Y |
| Stop/Start | Y | Y | Y |
| Restart | Y | Y | Y |
| Backup | Y | Y | N |
| Restore | Y | Y | N |
| Point-in-Time Recovery | Y | N | N |
| Reconfigure Parameters | Y | Y | Y |
| Switchover | Y | N | N |
| Minor Version Upgrade | Y | Y | N |
| Monitoring | Y | Y | Y |
| Accounts Management | Y | Y | N |
| TLS | Y | Y | N |

### Message Queues

| Feature | Kafka | RabbitMQ | Pulsar |
|---|---|---|---|
| Vertical Scaling | Y | Y | Y |
| Horizontal Scaling | Y | Y | Y |
| Volume Expansion | Y | Y | Y |
| Stop/Start | Y | Y | Y |
| Restart | Y | Y | Y |
| Backup | N | N | N |
| Restore | N | N | N |
| Reconfigure Parameters | Y | Y | Y |
| Monitoring | Y | Y | Y |

### Vector Databases

| Feature | Qdrant | Weaviate | Milvus |
|---|---|---|---|
| Vertical Scaling | Y | Y | Y |
| Horizontal Scaling | Y | Y | Y |
| Volume Expansion | Y | Y | Y |
| Stop/Start | Y | Y | Y |
| Restart | Y | Y | Y |
| Backup | Y | N | N |
| Restore | Y | N | N |
| Monitoring | Y | Y | Y |

### OLAP & Search

| Feature | Elasticsearch | StarRocks CE | ClickHouse | OpenSearch |
|---|---|---|---|---|
| Vertical Scaling | Y | Y | Y | Y |
| Horizontal Scaling | Y | Y | Y | Y |
| Volume Expansion | Y | Y | Y | Y |
| Stop/Start | Y | Y | Y | Y |
| Restart | Y | Y | Y | Y |
| Backup | N | N | N | N |
| Restore | N | N | N | N |
| Monitoring | Y | Y | Y | Y |

## Addon Installation Quick Reference

Install any addon with:

```bash
helm install kb-addon-<name> kubeblocks/<chart-name> \
  --namespace kb-system \
  --version <VERSION>
```

Where `<chart-name>` is the "Helm Chart Name" from the tables above, and `<VERSION>` should match your KubeBlocks major version (e.g., `1.0.2` for KubeBlocks v1.0.x).

### Common Addon Install Examples

```bash
# Elasticsearch
helm install kb-addon-elasticsearch kubeblocks/elasticsearch --namespace kb-system --version 1.0.2

# StarRocks CE
helm install kb-addon-starrocks-ce kubeblocks/starrocks-ce --namespace kb-system --version 1.0.2

# Milvus (vector DB)
helm install kb-addon-milvus kubeblocks/milvus --namespace kb-system --version 1.0.2

# ClickHouse
helm install kb-addon-clickhouse kubeblocks/clickhouse --namespace kb-system --version 1.0.2

# TiDB
helm install kb-addon-tidb kubeblocks/tidb --namespace kb-system --version 1.0.2

# OceanBase CE
helm install kb-addon-oceanbase-ce kubeblocks/oceanbase-ce --namespace kb-system --version 1.0.2

# MinIO
helm install kb-addon-minio kubeblocks/minio --namespace kb-system --version 1.0.2
```

## Documentation Links

- Supported Addons: https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons
- Install Addons: https://kubeblocks.io/docs/preview/user_docs/references/install-addons
- Full LLM Index: https://kubeblocks.io/llms-full.txt
