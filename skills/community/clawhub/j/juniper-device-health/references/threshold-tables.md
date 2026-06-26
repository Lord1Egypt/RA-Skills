# Juniper JunOS Threshold Tables

Detailed threshold definitions for JunOS device health parameters. JunOS reports
RE CPU as idle percentage (invert for utilization). PFE thresholds are per-FPC.
Adjust thresholds per device role, platform, and traffic profile.

## RE CPU Thresholds

### RE CPU Utilization (inverted from idle %)

| Level | Utilization | Idle % | Meaning | Action |
|-------|------------|--------|---------|--------|
| Normal | 0–40% | > 60% | Typical operating range | No action |
| Warning | 41–70% | 30–60% | Elevated load | Identify top daemons via `show system processes extensive` |
| Critical | 71–90% | 10–30% | High load, protocol timer risk | Investigate rpd, chassisd, mgd consumers |
| Emergency | > 90% | < 10% | Control plane at risk | Immediate triage, collect RSI |

### RE CPU During Commit (Expected Behavior)

JunOS RE CPU spikes during commit operations are normal. Do not alarm on transient
spikes that correlate with `show system commit` timestamps.

| Condition | CPU Spike | Duration | Action |
|-----------|----------|----------|--------|
| Small config change | 40–60% | 5–30 seconds | No action |
| Large config change | 60–85% | 30–120 seconds | Monitor, wait for completion |
| Full config replace | 70–95% | 1–5 minutes | Expected, do not interrupt |
| Spike after commit settles | Sustained > 70% | > 5 minutes after commit | Investigate — not commit-related |

### RE Load Average

Scale by RE core count (most MX/SRX/EX REs have 2–4 cores). Values are per-core.

| Level | Load/Core | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | < 0.7 | Healthy headroom | No action |
| Warning | 0.7–1.0 | Fully loaded | Monitor trend, identify top daemon |
| Critical | 1.0–2.0 | Overloaded, process queuing | Reduce load, investigate cause |
| Emergency | > 2.0 | Severely overloaded | Processes backed up, immediate intervention |

## RE Memory Thresholds

| Level | Used % | Meaning | Action |
|-------|--------|---------|--------|
| Normal | 0–70% | Healthy utilization | No action |
| Warning | 71–80% | Elevated usage | Identify top consumers, monitor trend |
| Critical | 81–90% | Memory pressure | Check for leaks, plan maintenance |
| Emergency | > 90% | Risk of process kills | Collect data, plan reload, open JTAC case |

## PFE Thresholds (Per-FPC)

### PFE CPU Utilization

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–60% | Healthy forwarding load | No action |
| Warning | 61–80% | Elevated forwarding | Check traffic rates, filter complexity |
| Critical | 81–95% | Forwarding stress | Identify traffic anomaly or table pressure |
| Emergency | > 95% | Forwarding engine saturated | Traffic loss likely, divert traffic |

### PFE Heap Memory

| Level | Used % | Meaning | Action |
|-------|--------|---------|--------|
| Normal | 0–65% | Healthy allocation | No action |
| Warning | 66–80% | Elevated usage | Monitor for growth |
| Critical | 81–90% | Memory pressure | Route/session table may be nearing limit |
| Emergency | > 90% | Heap exhaustion risk | New entries may fail, plan remediation |

### PFE Drop Rate

| Level | Drops/sec | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | < 50 | Normal operation | No action |
| Warning | 50–500 | Elevated drops | Identify drop category (fabric/local/discard) |
| Critical | 500–5,000 | Significant forwarding drops | Investigate traffic, filter, or NH issue |
| Emergency | > 5,000 | Severe data plane impact | Immediate investigation, may need traffic shift |

## Storage Thresholds

| Level | Used % | Meaning | Action |
|-------|--------|---------|--------|
| Normal | 0–75% | Healthy | No action |
| Warning | 76–85% | Filling | Monitor, plan cleanup |
| Critical | 86–95% | Near full | `request system storage cleanup`, remove old images |
| Emergency | > 95% | Full — commits may fail | Immediate cleanup, /var full prevents logging |

## Alarm Thresholds

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | No alarms | Healthy | No action |
| Warning | Minor alarm(s) only | Degraded but operational | Investigate, plan remediation |
| Critical | Major alarm present | Service-affecting | Address immediately |
| Emergency | Multiple Major alarms | Multiple service impacts | Immediate escalation |

## Interface Thresholds

### Error Rate

| Level | Rate | Meaning | Action |
|-------|------|---------|--------|
| Normal | < 0.001% | Clean | No action |
| Warning | 0.001–0.01% | Low errors | Monitor, check optics DOM |
| Critical | 0.01–0.1% | Significant errors | Investigate L1: cable, SFP, fiber |
| Emergency | > 0.1% | High error rate | Replace cable/optic, check remote end |

### Output Drops Per Hour

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–50/hr | Minimal | No action |
| Warning | 51–500/hr | Moderate congestion | Review policers, bandwidth |
| Critical | 501–5,000/hr | Significant drops | Tune policers, consider link upgrade |
| Emergency | > 5,000/hr | Severe congestion | Immediate intervention |

### Carrier Transitions Per Day

| Level | Count | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0 | Stable link | No action |
| Warning | 1–5/day | Intermittent flap | Check optics DOM, cable integrity |
| Critical | 6–20/day | Active instability | Replace cable/SFP, check remote end |
| Emergency | > 20/day | Persistent flapping | Hard bounce, replace, or disable until fixed |

## Routing Thresholds

### BGP Session Health

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Established, stable prefix count | Healthy peering | No action |
| Warning | Prefix count changed > 10% | Route churn | Investigate upstream change |
| Critical | Session flap in last hour | Peer instability | Check transport, hold timers |
| Emergency | Session down > 5 minutes | Peering failure | Verify connectivity, remote peer |

### OSPF/ISIS Adjacency Health

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All neighbors Full/Up | Healthy | No action |
| Warning | Adjacency reform in last hour | Recent instability | Monitor, check interface |
| Critical | Adjacency flapping | Active instability | Check MTU, timers, L1 |
| Emergency | Expected neighbor missing | Adjacency lost | Verify interface, check remote device |

## Environment Thresholds

### Temperature

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Below yellow threshold | Within operating spec | No action |
| Warning | Above yellow, below red | Approaching limit | Check fans, airflow, ambient |
| Critical | Above red, below shutdown | Thermal stress | Fix cooling immediately |
| Emergency | At shutdown threshold | Imminent shutdown | Emergency cooling, reduce load |

### Power Supply

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All PSUs OK, n+1 redundancy | Fully protected | No action |
| Warning | Single PSU, no redundancy | Unprotected | Plan PSU installation |
| Critical | Redundant PSU failed | Lost redundancy | RMA failed PSU |
| Emergency | Single PSU degraded | Power loss risk | Emergency maintenance |

### Fan Status

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All fans OK | Adequate cooling | No action |
| Warning | Fan RPM degraded | Reduced cooling capacity | Monitor temperature, plan replacement |
| Critical | One fan failed | Major alarm triggered | RMA fan tray |
| Emergency | Multiple fans failed | Thermal shutdown risk | Reduce load, emergency service |
