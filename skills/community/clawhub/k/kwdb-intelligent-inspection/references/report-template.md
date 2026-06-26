## Required Report Sections

The default inspection report must cover these sections unless the user explicitly narrows scope.

### Data Source Priority

1. **Port listener status**: Use Workflow Step 1 connectivity probe results (no fixed script) in SKILL.md
2. **Slow queries**: Use `scripts/get_kwdb_statements.py` (`/_status/statements` API)
3. **All other metrics**: Use `scripts/get_kwdb_ts_metrics.py` (`/ts/query` API)

### Report Sections

#### 1. Basic Indicators

- Database running state (`cr.node.liveness.livenodes`)
- Uptime (`cr.node.sys.uptime`)

#### 2. System Resources

- CPU user % (`cr.node.sys.cpu.user.percent`)
- CPU sys % (`cr.node.sys.cpu.sys.percent`)
- CPU combined % normalized (`cr.node.sys.cpu.combined.percent-normalized`)
- Disk total/available/used (`cr.store.capacity`, `cr.store.capacity.available`, `cr.store.capacity.used`)
- Memory RSS (`cr.node.sys.rss`)
- Go alloc/total bytes (`cr.node.sys.go.allocbytes`, `cr.node.sys.go.totalbytes`)

#### 3. Database Performance

- Write QPS: insert + update + delete + rebalancing writes
- Query QPS: select + query + rebalancing queries
- Exec latency: `cr.node.exec.latency-p99`, `cr.node.sql.service.latency-p99`, `cr.node.sql.distsql.exec.latency-p99`
- Slow query information (via `/_status/statements` API)

#### 4. Storage

- Total data size (`cr.store.totalbytes`, `cr.store.livebytes`, `cr.store.capacity.used`)

#### 5. Cluster

- Replicas, Raft leaders, Lease holders (`cr.store.replicas`, `cr.store.replicas.leaders`, `cr.store.replicas.leaseholders`)
- Unavailable/Under-replicated/Over-replicated ranges
- Sync lag (`cr.store.raft.replica.consistent.latency-p99`, `cr.store.raftlog.behind`, `cr.store.raft.replica.consistent.latency-p99`)
- Data distribution balance

#### 6. Network

- Node-to-node latency (`round-trip-latency`, `cr.node.clock-offset.meannanos`)
