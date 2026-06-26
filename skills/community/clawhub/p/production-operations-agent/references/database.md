# Database & Storage Investigation Reference

Load this when the incident involves database performance, connection issues, replication, or storage systems.

## Key Signals to Surface

- Connection pool exhaustion: max connections hit, connection wait timeouts
- Slow queries: missing indexes, lock contention, full table scans, N+1 patterns
- Replication lag: replica falling behind primary, replication broken
- Disk pressure: WAL buildup, autovacuum bloat (Postgres), log file growth
- Cache hit rate drop: Redis/Memcached evictions, cold cache after restart

## Suggested `neubird investigate` Prompts

```
"Database connections are exhausted on the primary RDS Postgres instance"
"Query latency spiked on the orders table — find the slow queries"
"Read replica is lagging by 45 minutes — what's blocking replication?"
"Redis eviction rate jumped — is the cache undersized or is there a stampede?"
"Postgres autovacuum is not keeping up — what tables are bloated?"
```

## Connection Exhaustion Checklist

1. What is max_connections set to? What is current active count?
2. Are connections being leaked (long-running idle transactions)?
3. Did a new service version increase pool size?
4. Is PgBouncer/ProxySQL in front — is the pooler healthy?
5. Are there long-running transactions holding locks?

## Replication Lag Causes (Postgres)

| Cause | Indicator |
|-------|-----------|
| Heavy write load | High WAL generation rate |
| Large transaction | Single long-running write on primary |
| Network bandwidth | Network saturation between primary and replica |
| Replica disk I/O | Slow replica disk, replica CPU |
| Replication slot bloat | Inactive slot holding WAL |
