# Switchover Reference

## Table of Contents

- [Per-Engine Switchover Behavior](#per-engine-switchover-behavior)
- [HA Middleware Details](#ha-middleware-details)
- [Replication Health Check Commands](#replication-health-check-commands)

## Per-Engine Switchover Behavior

| Engine | Switchover Mechanism | Write Downtime | Automatic Failover |
|---|---|---|---|
| MySQL (semisync) | KubeBlocks built-in role manager | 1-3 seconds | Yes (via role probe) |
| MySQL (MGR) | Group Replication consensus | Sub-second | Yes (built-in) |
| MySQL (Orchestrator) | Orchestrator promotes replica | 2-5 seconds | Yes (Orchestrator detects failure) |
| PostgreSQL | Patroni DCS-based leader election | 1-5 seconds | Yes (Patroni) |
| Redis (replication) | Sentinel-based promotion | 1-3 seconds | Yes (Sentinel) |
| MongoDB | Replica set election via internal protocol | 2-10 seconds | Yes (built-in) |

Switchover docs:
- MySQL: https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/04-operations/08-switchover
- PostgreSQL: https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/04-operations/08-switchover
- MongoDB: https://kubeblocks.io/docs/preview/kubeblocks-for-mongodb/04-operations/08-switchover
- Redis: https://kubeblocks.io/docs/preview/kubeblocks-for-redis/04-operations/08-switchover

## HA Middleware Details

### MySQL Orchestrator

Orchestrator is an external HA manager that monitors MySQL replication topology and can perform automated failover.

- Used in the `orc` and `orc-proxysql` topologies
- Discovers replication topology by querying `SHOW SLAVE STATUS` / `SHOW REPLICAS`
- On primary failure: selects the most up-to-date replica, promotes it, and reconfigures other replicas
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/03-topologies/05-orchestrator

### PostgreSQL Patroni

Patroni uses a distributed configuration store (DCS, typically Kubernetes endpoints) to manage leader election.

- All PostgreSQL instances run a Patroni sidecar
- Patroni holds a leader lock in the DCS; if the leader fails to renew, a new leader is elected
- During switchover, Patroni demotes the current leader and promotes the target replica
- FAQ and DCS details: https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/09-faqs

### Redis Sentinel

Redis Sentinel monitors Redis master-replica setups and performs automatic failover.

- Sentinel instances run as sidecars alongside Redis pods
- On master failure, Sentinels vote to elect a new master
- Client connections are re-routed via the Sentinel-aware service
- FAQ: https://kubeblocks.io/docs/preview/kubeblocks-for-redis/09-faqs

## Replication Health Check Commands

### MySQL

```bash
# Check replication status on a replica
kubectl exec -it <replica-pod> -n <ns> -- mysql -u root -p -e "SHOW REPLICA STATUS\G"

# Key fields to check:
#   Replica_IO_Running: Yes
#   Replica_SQL_Running: Yes
#   Seconds_Behind_Source: 0  (should be low)

# For Group Replication
kubectl exec -it <pod> -n <ns> -- mysql -u root -p -e "SELECT * FROM performance_schema.replication_group_members;"
```

### PostgreSQL

```bash
# Check replication from the primary
kubectl exec -it <primary-pod> -n <ns> -- psql -U postgres -c "SELECT pid, usename, client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn FROM pg_stat_replication;"

# Check replication lag in bytes
kubectl exec -it <primary-pod> -n <ns> -- psql -U postgres -c "SELECT client_addr, pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes FROM pg_stat_replication;"

# On the replica, check recovery status
kubectl exec -it <replica-pod> -n <ns> -- psql -U postgres -c "SELECT pg_is_in_recovery(), pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn();"
```

### Redis

```bash
# Check replication info
kubectl exec -it <pod> -n <ns> -- redis-cli INFO replication

# Key fields:
#   role: master/slave
#   connected_slaves: N
#   master_repl_offset: <offset>
#   slave_repl_offset: <offset>  (should be close to master_repl_offset)

# For Redis Cluster
kubectl exec -it <pod> -n <ns> -- redis-cli CLUSTER INFO
kubectl exec -it <pod> -n <ns> -- redis-cli CLUSTER NODES
```

### MongoDB

```bash
# Check replica set status
kubectl exec -it <pod> -n <ns> -- mongosh --eval "rs.status()"

# Check replication lag
kubectl exec -it <pod> -n <ns> -- mongosh --eval "rs.printSecondaryReplicationInfo()"

# Key fields in rs.status():
#   members[].stateStr: PRIMARY / SECONDARY
#   members[].optimeDate: should be close across all members
```
