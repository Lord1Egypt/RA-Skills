# Infrastructure Metrics — Thresholds Reference

Standard thresholds for common infrastructure metrics. These are defaults for general-purpose servers. Adjust based on workload context (a database server has different normal ranges than a static file server).

## CPU

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| CPU utilization (avg) | <70% | 70-90% | >90% |
| Load average (1m) / cores | <0.7 | 0.7-1.0 | >1.0 |
| Load average (5m) / cores | <0.7 | 0.7-1.0 | >1.0 |
| Load average (15m) / cores | <0.5 | 0.5-0.8 | >0.8 |
| CPU steal (virtualized) | <5% | 5-15% | >15% |
| iowait | <10% | 10-25% | >25% |

**Context adjustments:**
- Build servers and CI runners: CPU >90% during builds is expected, not critical
- Web servers: sustained >80% indicates insufficient capacity or runaway process
- Database servers: iowait is more important than raw CPU — high iowait + moderate CPU = disk bottleneck

## Memory

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Memory used (% of total) | <75% | 75-90% | >90% |
| Swap used (% of total) | <10% | 10-50% | >50% |
| Swap used (absolute) | <500MB | 500MB-2GB | >2GB |
| Available memory | >25% of total | 10-25% | <10% |
| OOM kills (last 24h) | 0 | 1-2 | >2 |

**Context adjustments:**
- Database servers: high memory usage is often intentional (buffer/cache). Check `available` not just `used`.
- Java/JVM apps: heap is pre-allocated — 80% memory used may be normal. Check for OOM kills instead.
- Redis/memcached: designed to use all allocated memory. Monitor eviction rate instead.

## Disk

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Disk usage (%) | <75% | 75-90% | >90% |
| Inode usage (%) | <75% | 75-90% | >90% |
| Disk I/O utilization | <60% | 60-85% | >85% |
| Disk latency (avg) | <10ms | 10-50ms | >50ms |
| Days until full (projected) | >60 days | 14-60 days | <14 days |

**Context adjustments:**
- Small volumes (<20GB): tighter thresholds — 80% is effectively critical because absolute free space is tiny
- Large volumes (>1TB): percentage matters less — 85% on 2TB still leaves 300GB free
- Log volumes: growth rate matters more than current usage — check for log rotation
- Database volumes: also check WAL/journal space separately

**Volume-size scaling:**
| Volume size | Warning threshold | Critical threshold |
|---|---|---|
| <20GB | 70% | 85% |
| 20-100GB | 75% | 90% |
| 100GB-1TB | 80% | 92% |
| >1TB | 85% | 95% |

## Network

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Interface errors/min | 0 | 1-10 | >10 |
| Dropped packets/min | 0 | 1-5 | >5 |
| Bandwidth utilization | <60% | 60-85% | >85% |
| TCP retransmission rate | <1% | 1-5% | >5% |
| Connection count | <80% of limit | 80-95% | >95% |

**Context adjustments:**
- CDN/proxy servers: high bandwidth is expected — monitor error rate instead
- API servers: connection count and retransmission rate are better signals than raw bandwidth

## Uptime / Endpoint Checks

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| HTTP status code | 2xx | 3xx (unexpected) | 4xx/5xx |
| Response time | <500ms | 500ms-2s | >2s |
| Response time (API) | <200ms | 200ms-1s | >1s |
| SSL days remaining (auto-renew) | >14 days | 7-14 days | <7 days |
| SSL days remaining (manual renewal) | >45 days | 14-45 days | <14 days |
| SSL days remaining (unknown type) | >30 days | 7-30 days | <7 days |
| DNS resolution time | <100ms | 100-500ms | >500ms |
| Uptime (7-day) | >99.9% | 99-99.9% | <99% |

**Context adjustments:**
- Static sites: response time should be <200ms, tighter than API default
- Background/batch endpoints: response time thresholds are irrelevant — check completion status
- Internal services: SSL expiry on self-signed certs requires different handling (user manages renewal)

## System

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Uptime | >1 day | — | <1 hour (unexpected reboot) |
| Pending security updates | 0 | 1-5 | >5 or any critical CVE |
| Reboot required | No | — | Yes (security patch pending) |
| NTP drift | <100ms | 100ms-1s | >1s |
| Open file descriptors | <60% of limit | 60-85% | >85% |
| Zombie processes | 0-2 | 3-10 | >10 |

## Compound Signals

These combinations are more significant than individual metrics:

| Signal combination | Likely cause | Severity boost |
|---|---|---|
| High CPU + high swap + low memory | Memory exhaustion causing swap thrash | Escalate to critical |
| High iowait + high disk latency + normal CPU | Disk I/O bottleneck | Escalate to critical |
| High connection count + rising response time | Connection saturation | Escalate to critical |
| Disk >85% + positive growth trend + <30 days projected | Imminent disk full | Escalate to critical |
| Multiple OOM kills + high swap | Persistent memory pressure | Escalate to critical |
| Multiple OOM kills + no swap configured | No memory relief valve — any spike kills processes instantly | Escalate to critical |
| High CPU steal + degraded response time | Noisy neighbor (shared hosting) | Note: user can't fix this directly |
