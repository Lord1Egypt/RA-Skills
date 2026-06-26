## Metric Types

This document maps each inspectable metric to its `/ts/query` query params. Query params are read from this file when constructing API requests — do not infer or invent values.

### Notation

- `d` = downsampler
- `sa` = source_aggregator
- `der` = derivative

### Gauge / Counter Metrics

These metrics use: `d:1, sa:2, der:0`

| Metric Name |
|-------------|
| `cr.node.liveness.livenodes` |
| `cr.node.sys.uptime` |
| `cr.node.sys.cpu.user.percent` |
| `cr.node.sys.cpu.sys.percent` |
| `cr.node.sys.cpu.combined.percent-normalized` |
| `cr.store.capacity` |
| `cr.store.capacity.available` |
| `cr.store.capacity.used` |
| `cr.node.sys.rss` |
| `cr.node.sys.go.allocbytes` |
| `cr.node.sys.go.totalbytes` |
| `cr.node.sql.insert.count` |
| `cr.node.sql.update.count` |
| `cr.node.sql.delete.count` |
| `cr.store.rebalancing.writespersecond` |
| `cr.node.sql.select.count` |
| `cr.node.sql.query.count` |
| `cr.store.rebalancing.queriespersecond` |
| `cr.store.totalbytes` |
| `cr.store.livebytes` |
| `cr.store.replicas` |
| `cr.store.replicas.leaders` |
| `cr.store.replicas.leaseholders` |
| `cr.store.ranges.unavailable` |
| `cr.store.ranges.underreplicated` |
| `cr.store.ranges.overreplicated` |
| `cr.store.raftlog.behind` |

### Latency Metrics

These metrics use: `d:1, sa:1, der:0`

| Metric Name |
|-------------|
| `cr.node.exec.latency-p99` |
| `cr.node.sql.service.latency-p99` |
| `cr.node.sql.distsql.exec.latency-p99` |
| `cr.store.raft.replica.consistent.latency-p99` |
| `cr.node.clock-offset.meannanos` |
