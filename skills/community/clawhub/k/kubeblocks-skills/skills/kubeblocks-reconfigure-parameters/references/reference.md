# Reconfigure Parameters Reference

Common tunable database parameters for each KubeBlocks addon.

## MySQL / ApeCloud MySQL

### Dynamic Parameters (no restart)

| Parameter | Description | Default | Recommended Range |
|-----------|-------------|---------|-------------------|
| `max_connections` | Maximum concurrent connections | 151 | 100–10000 |
| `max_allowed_packet` | Maximum packet size (bytes) | 67108864 | 16M–1G |
| `table_open_cache` | Number of open tables cache | 4000 | 2000–16384 |
| `thread_cache_size` | Number of threads to cache | 9 | 8–100 |
| `sort_buffer_size` | Sort buffer per session (bytes) | 262144 | 256K–4M |
| `read_buffer_size` | Read buffer per session (bytes) | 131072 | 128K–2M |
| `read_rnd_buffer_size` | Random read buffer (bytes) | 262144 | 256K–4M |
| `join_buffer_size` | Join buffer per session (bytes) | 262144 | 256K–4M |
| `tmp_table_size` | Max in-memory temp table size | 16777216 | 16M–256M |
| `max_heap_table_size` | Max MEMORY table size | 16777216 | 16M–256M |
| `binlog_format` | Binary log format | ROW | ROW, MIXED, STATEMENT |
| `long_query_time` | Slow query threshold (seconds) | 10 | 0.1–30 |
| `slow_query_log` | Enable slow query log | OFF | ON, OFF |

### Static Parameters (requires restart)

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `innodb_buffer_pool_size` | InnoDB buffer pool size | 128M | Set to 50–80% of available memory |
| `innodb_log_file_size` | Redo log file size | 48M | 256M–2G for high write loads |
| `innodb_log_buffer_size` | Log buffer size | 16M | 16M–128M |
| `innodb_flush_method` | InnoDB flush method | O_DIRECT | O_DIRECT recommended |

## PostgreSQL

### Dynamic Parameters (no restart)

| Parameter | Description | Default | Recommended Range |
|-----------|-------------|---------|-------------------|
| `work_mem` | Per-operation work memory | 4MB | 4MB–256MB |
| `maintenance_work_mem` | Maintenance operation memory | 64MB | 64MB–2GB |
| `effective_cache_size` | Planner cache estimate | 4GB | 50–75% of total memory |
| `random_page_cost` | Random page access cost | 4.0 | 1.1 (SSD) to 4.0 (HDD) |
| `effective_io_concurrency` | Concurrent I/O operations | 1 | 200 (SSD), 2 (HDD) |
| `checkpoint_completion_target` | Checkpoint spread ratio | 0.9 | 0.7–0.9 |
| `wal_buffers` | WAL buffer size | -1 (auto) | 16MB–64MB |
| `log_min_duration_statement` | Slow query threshold (ms) | -1 (off) | 100–5000 |
| `statement_timeout` | Max statement time (ms) | 0 (off) | 30000–300000 |
| `idle_in_transaction_session_timeout` | Idle txn timeout (ms) | 0 (off) | 60000–600000 |

### Static Parameters (requires restart)

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `max_connections` | Maximum connections | 100 | 100–5000 |
| `shared_buffers` | Shared memory buffers | 128MB | 25% of total memory |
| `max_wal_size` | Max WAL size before checkpoint | 1GB | 1GB–16GB |
| `min_wal_size` | Min WAL size | 80MB | 80MB–1GB |
| `max_worker_processes` | Max background workers | 8 | Match CPU cores |

## Redis

### Dynamic Parameters (no restart)

| Parameter | Description | Default | Recommended Range |
|-----------|-------------|---------|-------------------|
| `maxmemory` | Maximum memory limit | 0 (no limit) | Set to ~75% of pod memory |
| `maxmemory-policy` | Eviction policy | noeviction | noeviction, allkeys-lru, volatile-lru, allkeys-random, volatile-ttl |
| `timeout` | Client idle timeout (seconds) | 0 (no timeout) | 300–3600 |
| `tcp-keepalive` | TCP keepalive interval | 300 | 60–300 |
| `hz` | Server timer frequency | 10 | 10–500 |
| `activedefrag` | Active defragmentation | no | yes, no |
| `lazyfree-lazy-eviction` | Lazy eviction | no | yes, no |
| `lazyfree-lazy-expire` | Lazy expiration | no | yes, no |
| `slowlog-log-slower-than` | Slow log threshold (μs) | 10000 | 1000–50000 |
| `slowlog-max-len` | Slow log max entries | 128 | 128–1024 |

## MongoDB

### Dynamic Parameters (no restart)

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `wiredTigerCacheSizeGB` | WiredTiger cache size (GB) | 50% of (RAM - 1GB) | Adjust based on working set |
| `maxIncomingConnections` | Max incoming connections | 65536 | 100–65536 |
| `slowOpThresholdMs` | Slow operation threshold (ms) | 100 | 50–5000 |
| `cursorTimeoutMillis` | Cursor timeout (ms) | 600000 | 60000–3600000 |

## OpsRequest Example

Modify any parameter from the tables above:

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-reconfigure
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Reconfiguring
  reconfigures:
  - componentName: <component>
    parameters:
    - key: <parameter-name>
      value: "<new-value>"
```

## Documentation Links

- MySQL Configuration: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/configuration/configure-cluster-parameters
- PostgreSQL Configuration: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/configuration/configure-cluster-parameters
- Redis Configuration: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/configuration/configure-cluster-parameters
- MongoDB Configuration: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/configuration/configure-cluster-parameters
