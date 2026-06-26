# Ambari API Endpoints Reference

## Base URL

```
{ambari_host}:8080/api/v1
```

## Authentication

All requests use HTTP Basic Auth with username and password.

Headers:
```
X-Requested-By: ambari
Content-Type: application/json
```

## Cluster Endpoints

### List Clusters
```
GET /clusters
```

### Get Cluster Info
```
GET /clusters/{clusterName}
```

## Service Endpoints

### List Services
```
GET /clusters/{clusterName}/services
```

Response includes service name, state, and cluster info.

### Get Service Details
```
GET /clusters/{clusterName}/services/{serviceName}
```

### Service State Change
```
PUT /clusters/{clusterName}/services/{serviceName}

Body:
{
  "RequestInfo": {
    "context": "START HDFS"
  },
  "Body": {
    "ServiceInfo": {
      "state": "STARTED"
    }
  }
}
```

Valid states: `STARTED`, `INSTALLED` (stopped), `INSTALLING`, `STARTING`, `STOPPING`, `RESTARTING`

## Host Endpoints

### List Hosts
```
GET /clusters/{clusterName}/hosts
```

### Get Host Info
```
GET /clusters/{clusterName}/hosts/{hostName}
```

### List Host Components
```
GET /clusters/{clusterName}/hosts/{hostName}/host_components
```

### Component State Change
```
PUT /clusters/{clusterName}/hosts/{hostName}/host_components/{componentName}

Body:
{
  "RequestInfo": {
    "context": "START DATANODE on host01"
  },
  "HostRoles": {
    "state": "STARTED"
  }
}
```

## Request Tracking

### Get Request Status
```
GET /clusters/{clusterName}/requests/{requestId}
```

### Get Request Tasks
```
GET /clusters/{clusterName}/requests/{requestId}/tasks
```

## Common Service Names

| Service | Service Name |
|---------|-------------|
| HDFS | HDFS |
| YARN | YARN |
| MapReduce2 | MAPREDUCE2 |
| Hive | HIVE |
| HBase | HBASE |
| Spark2 | SPARK2 |
| Kafka | KAFKA |
| ZooKeeper | ZOOKEEPER |
| Storm | STORM |
| Flink | FLINK |
| Oozie | OOZIE |
| Knox | KNOX |
| Ranger | RANGER |
| Atlas | ATLAS |
| Ambari Metrics | AMS |
| Log Search | LOGSEARCH |

## Common Components

| Service | Master Components | Worker Components |
|---------|------------------|-------------------|
| HDFS | NAMENODE, SECONDARY_NAMENODE | DATANODE |
| YARN | RESOURCEMANAGER | NODEMANAGER |
| Hive | HIVE_SERVER, HIVE_METASTORE | - |
| HBase | HBASE_MASTER | HBASE_REGIONSERVER |
| Spark2 | SPARK2_JOBHISTORYSERVER | SPARK2_THRIFTSERVER |
| Kafka | KAFKA_BROKER | - |
| ZooKeeper | ZOOKEEPER_SERVER | - |

## Version Differences

### Ambari 2.7.5
- Standard REST API v1
- Basic service/component operations

### Ambari 3.0.0
- Extended API with additional endpoints
- Enhanced request tracking
- Additional Mpack endpoints: `GET /mpacks`
- Blueprint v2 support: `POST /blueprints`