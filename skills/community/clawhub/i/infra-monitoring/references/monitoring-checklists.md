# Monitoring Checklists

## Daily Health Check

Run once per day. Takes <5 minutes for a single server.

- [ ] **CPU load average** — check 15-minute load average relative to core count
- [ ] **Memory available** — confirm >10% available (not just "free" — available includes reclaimable cache)
- [ ] **Disk usage** — check all mount points, flag any >75%
- [ ] **Swap usage** — any swap activity on a server that shouldn't be swapping?
- [ ] **Uptime** — unexpected reboots since yesterday?
- [ ] **Key services running** — web server, database, application process, queue workers
- [ ] **Endpoint checks** — hit your main URLs, confirm 200 and reasonable response time
- [ ] **SSL certificates** — any expiring within 30 days?
- [ ] **Error logs** — quick scan of syslog/application logs for new errors since yesterday
- [ ] **Backup status** — did last night's backup complete?

### Commands for quick daily check (Linux)
```bash
# CPU and load
uptime

# Memory
free -h

# Disk
df -h
df -i  # inode usage

# Swap
swapon --show

# Key processes (example: nginx, postgres, node)
systemctl is-active nginx postgresql node-app

# Recent errors
journalctl --since yesterday --priority err --no-pager | tail -20

# SSL cert check (replace with your domain)
echo | openssl s_client -connect yourdomain.com:443 -servername yourdomain.com 2>/dev/null | openssl x509 -noout -dates
```

## Weekly Review

Run once per week. Builds trend awareness.

- [ ] **Disk growth rate** — how much did each volume grow this week? Project days-until-full.
- [ ] **Memory trend** — is baseline memory usage creeping up? (indicates leaks)
- [ ] **Uptime summary** — any outages this week? Total downtime minutes.
- [ ] **Response time trends** — are endpoints getting slower week-over-week?
- [ ] **Security updates** — any pending patches? Any critical CVEs?
- [ ] **Log volume** — are logs growing faster than expected? Is log rotation working?
- [ ] **Backup verification** — pick one backup and verify it can actually restore
- [ ] **Certificate expiry** — anything expiring within 60 days?
- [ ] **Resource headroom** — at current growth, when do you need to upgrade?

## Incident Response Checklist

Use when something breaks. Work top to bottom.

### 1. Assess (first 5 minutes)
- [ ] What is the user-facing impact? (total outage, degraded, cosmetic)
- [ ] When did it start? (check monitoring data, error logs, deploy timestamps)
- [ ] What changed recently? (deploys, config changes, infrastructure changes, traffic spikes)
- [ ] Is this affecting one server/service or multiple?

### 2. Triage (next 10 minutes)
- [ ] Can you reproduce the issue?
- [ ] Check server health: CPU, memory, disk, network
- [ ] Check application logs for errors
- [ ] Check database connectivity and performance
- [ ] Check external dependencies (DNS, CDN, third-party APIs)
- [ ] Is the issue in the server, the application, or the network?

### 3. Mitigate (next 15 minutes)
- [ ] Can you restore service without fixing the root cause? (restart, rollback, failover)
- [ ] If a deploy caused it, can you revert?
- [ ] If a resource is exhausted, can you free space/memory/connections?
- [ ] Communicate status to affected users if applicable

### 4. Resolve
- [ ] Identify root cause
- [ ] Apply fix
- [ ] Verify fix resolves the issue
- [ ] Monitor for recurrence (30 minutes minimum)

### 5. Post-Incident
- [ ] Document: what happened, when, impact, root cause, fix applied
- [ ] Identify: what monitoring would have caught this earlier?
- [ ] Action items: what prevents recurrence?
- [ ] Update monitoring: add checks for the failure mode that was missed

## New Server Setup Checklist

When bringing a new server into your fleet.

- [ ] **OS updated** — all packages current, security patches applied
- [ ] **Firewall configured** — only required ports open
- [ ] **SSH hardened** — key-only auth, no root login, non-default port (optional)
- [ ] **Monitoring agent** — whatever your monitoring solution requires
- [ ] **Log forwarding** — logs shipping to centralized location
- [ ] **Backup configured** — automated, tested, offsite
- [ ] **SSL certificates** — installed and auto-renewal configured
- [ ] **NTP configured** — time sync verified
- [ ] **Swap configured** — appropriate for workload
- [ ] **Disk alerts** — monitoring in place for all mount points
- [ ] **Health endpoint** — application exposes a /health or equivalent
- [ ] **DNS configured** — hostname resolves correctly
- [ ] **Documented** — server purpose, services, access procedures recorded
