# Test Prompts

## Happy Path (4 tests — clean data, clear asks, expected workflows)

### HP-1: Single server health check from system output
```
Can you check the health of my server? Here's the output:

$ uptime
 14:23:07 up 45 days, 3:12, 1 user, load average: 0.42, 0.38, 0.35

$ free -h
              total    used    free    shared  buff/cache  available
Mem:          7.8Gi   3.2Gi   512Mi   128Mi   4.1Gi       4.2Gi
Swap:         2.0Gi   0B      2.0Gi

$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   32G   16G  67% /
/dev/sdb1       200G   45G  145G  24% /data

This runs our main web app (Node.js) and PostgreSQL database.
```
**Expected:** Triggers health check flow. All metrics healthy — CPU load well under threshold (0.42/cores), memory has 54% available, no swap usage, disk at 67% and 24%. Reports "All systems healthy. No action required." with one-line per metric. Notes the 45-day uptime is fine. Might suggest checking for pending security updates given the 45-day uptime without reboot.

### HP-2: Endpoint uptime check with SSL
```
Check these endpoints for me:

1. https://api.myapp.com/health — should return 200
2. https://myapp.com — main website, should return 200
3. https://admin.myapp.com — admin panel, should return 200

Also check the SSL certs. We use Let's Encrypt.
```
**Expected:** Runs HTTP checks against all three endpoints. Reports status code, response time, and SSL certificate expiry for each. Notes Let's Encrypt typically auto-renews at 30 days, so only flag if <14 days (auto-renew may have failed). Clean table output with endpoint, status, response time, SSL days remaining.

### HP-3: Server with clear warning signs
```
My VPS has been feeling sluggish. Here's what I see:

$ uptime
 09:15:22 up 12 days, load average: 3.82, 3.45, 2.91

$ free -h
              total    used    free    shared  buff/cache  available
Mem:          4.0Gi   3.6Gi   52Mi    64Mi    348Mi       180Mi
Swap:         2.0Gi   1.8Gi   200Mi

$ df -h
/dev/vda1       40G   36G  2.3G  94% /

This is a 2-core VPS running a Rails app with PostgreSQL.
```
**Expected:** Flags multiple issues: (1) Critical: disk at 94% on a 40GB volume — only 2.3GB free, needs immediate action. (2) Critical: memory nearly exhausted — only 180Mi available out of 4GB, 1.8GB in swap indicates severe memory pressure. (3) Warning: load average 3.82 on 2 cores (1.91 per core) is elevated. Identifies compound signal: high load + high swap + low memory = memory thrashing causing the sluggishness. Recommends: investigate memory-hungry processes, clear disk space immediately, consider upgrading the VPS.

### HP-4: Multi-endpoint status report with one issue
```
Weekly check on our services:

API (https://api.example.com/ping): 200 OK, 145ms
Website (https://example.com): 200 OK, 89ms
Docs (https://docs.example.com): 200 OK, 312ms
Staging (https://staging.example.com): 503 Service Unavailable, timeout after 10s
Webhook receiver (https://hooks.example.com/health): 200 OK, 67ms

SSL certs all renewed 2 weeks ago via Let's Encrypt.
```
**Expected:** Reports 4 of 5 endpoints healthy. Flags staging as critical (503 + timeout). Notes docs response time (312ms) is within healthy range but notably slower than others — not a warning, just an observation. SSL all healthy (renewed 2 weeks ago = ~76 days remaining). Main action: investigate and restore staging. Secondary: check why docs is 2-3x slower than other endpoints.

## Normal Path (4 tests — reasonable asks with some ambiguity or complexity)

### NP-1: Ambiguous health check request
```
Can you monitor my server?
```
**Expected:** Triggers the no-data gate. Asks what server(s) to monitor, what services run on them, and whether the user wants a one-time health check or ongoing monitoring setup. Offers the starter monitoring checklist. Does not generate fictional metrics.

### NP-2: Partial data with missing context
```
Here's my disk usage, is this OK?

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        20G   17G  1.8G  89% /
/dev/sda2       500G  125G  350G  26% /data
tmpfs           3.9G  1.2M  3.9G   1% /run
```
**Expected:** Assesses disk: root volume (20GB) at 89% is critical because absolute free space is only 1.8GB on a small volume. Data volume healthy at 26%. Notes tmpfs is irrelevant for disk monitoring. Warns about root volume urgency, suggests checking what's consuming space (logs, temp files, old packages). Notes: "I can only assess disk — for a complete health check I'd also need CPU, memory, and service status."

### NP-3: System output needing interpretation
```
My app keeps crashing. Here are the last few log lines:

Mar 28 14:23:01 web1 kernel: [423516.234] Out of memory: Killed process 1842 (node) total-vm:2048000kB, anon-rss:1536000kB
Mar 28 14:23:05 web1 systemd: node-app.service: Main process exited, code=killed, signal=KILL
Mar 28 14:23:06 web1 systemd: node-app.service: Scheduled restart job, restart counter is at 14.
Mar 28 15:01:22 web1 kernel: [426598.891] Out of memory: Killed process 2156 (node) total-vm:2048000kB, anon-rss:1587200kB
Mar 28 15:01:25 web1 systemd: node-app.service: Main process exited, code=killed, signal=KILL
Mar 28 15:01:26 web1 systemd: node-app.service: Scheduled restart job, restart counter is at 15.

$ free -h
              total    used    free    shared  buff/cache  available
Mem:          2.0Gi   1.8Gi   32Mi    16Mi    168Mi       82Mi
Swap:         0B       0B     0B
```
**Expected:** Identifies the issue clearly: OOM killer is terminating the Node.js process repeatedly. The process is requesting ~2GB VM but the server only has 2GB total RAM with no swap. Restart counter at 15 means this has happened many times. Critical severity. Recommends: (1) add swap as immediate relief, (2) investigate Node.js memory usage for leaks, (3) upgrade server RAM if the application legitimately needs >2GB. Notes that "no swap configured" makes this worse — any memory spike kills the app instantly.

### NP-4: SSL certificate focus
```
I manage 6 domains and I keep getting surprised by certificate expiries. Can you help me set up a check? Here are the domains:

- myapp.com
- api.myapp.com  
- staging.myapp.com
- docs.myapp.com
- myothersite.org
- legacy.oldsite.net (this one doesn't auto-renew, we renew manually)
```
**Expected:** Proposes checking all 6 domains for SSL expiry. Notes that 5 of 6 likely auto-renew but legacy.oldsite.net is manual — this is the highest risk domain. Suggests a monitoring schedule: weekly SSL check with different warning thresholds for auto-renew (flag at <14 days, means renewal failed) vs. manual renewal (flag at <45 days, gives time to act). Offers the weekly review checklist. Provides the openssl command to check each domain.

## Edge Cases (4 tests — broken data, unreasonable asks, boundary conditions)

### EC-1: No server data, wants full monitoring
```
Set up complete infrastructure monitoring for my 50-server Kubernetes cluster with Prometheus, Grafana, and PagerDuty integration.
```
**Expected:** Acknowledges the request but clearly scopes what this skill can and cannot do. This skill provides plain-language health checks and status reports — it is not a replacement for Prometheus/Grafana/PagerDuty infrastructure. For a 50-server k8s cluster, recommends proper observability tooling. Offers: can supplement enterprise monitoring with plain-language summaries of individual server health checks or endpoint uptime. Does not pretend to replace a full monitoring stack.

### EC-2: Contradictory or impossible metrics
```
Check this server health:

CPU: 5%
Memory: 98% used
Swap: 0%
Disk: 45%
Load average: 0.01
Response time: 45 seconds for /health endpoint

The server seems fine to me.
```
**Expected:** Flags the contradiction: very low CPU (5%) and low load (0.01) combined with 98% memory usage suggests either: (1) a memory leak in a sleeping/idle process, or (2) large in-memory cache that is intentional. The 45-second response time for a health endpoint is critical regardless — that's unusable for any real traffic. Disagrees with "seems fine" — the response time alone is a problem. Asks: what's running on this server? Is the memory usage expected (database cache, in-memory store)?

### EC-3: Request to remediate without approval
```
My server disk is at 98%. Delete the log files and restart nginx to free up space.
```
**Expected:** Reports the critical disk status. Does NOT execute the deletion or restart. Explains that the skill monitors and reports but does not perform automated remediation without explicit user step-by-step confirmation. Offers to help identify what's consuming space (suggests `du -sh /var/log/*` and checking log rotation config). Notes that blindly deleting logs may lose debugging data — suggests rotating first, then clearing old logs. If the user explicitly confirms each step, can guide them through it.

### EC-4: Non-infrastructure monitoring request
```
Can you monitor our MRR, customer churn rate, and NPS score and alert me when they drop below targets?
```
**Expected:** Recognizes these are business metrics, not infrastructure metrics. Does NOT attempt to monitor them. Redirects to the data-analysis-reporting skill which handles business data analysis, KPI tracking, and health checks against targets. Offers: if the user also wants to monitor the servers that run their business, this skill handles that part.
