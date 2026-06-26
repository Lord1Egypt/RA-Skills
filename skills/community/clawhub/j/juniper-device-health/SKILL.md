---
name: juniper-device-health
description: >-
  Juniper JunOS device health check and triage procedure. Use when
  troubleshooting Juniper MX, SRX, EX, QFX, or PTX platforms — assessing
  Routing Engine health, Packet Forwarding Engine state, chassis alarms,
  system resources, and environment. Covers dual-RE failover detection,
  alarm severity triage, PFE statistics analysis, and commit-correlated
  diagnostics. Procedure begins with RE mastership verification — health
  data from the wrong RE produces incorrect assessments.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔍","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["juniper","junos","health"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# Juniper JunOS Device Health Check

Structured triage procedure for assessing Juniper device health across MX, SRX,
EX, QFX, and PTX platforms. Produces a prioritized findings report with severity
classifications and recommended actions.

JunOS separates Routing Engine (RE) and Packet Forwarding Engine (PFE). These
are independent health domains — a healthy RE does not guarantee a healthy PFE,
and vice versa. This procedure assesses both explicitly.

## When to Use

- Device reported as slow, dropping traffic, or unresponsive
- Scheduled health audit of Juniper routers, switches, or firewalls
- Post-change verification after commits, upgrades, or ISSU
- Capacity planning data collection for RE CPU, memory, and link utilization
- Incident response when a Juniper device is suspected as the fault domain
- RE failover event — verify mastership and standby RE state
- Chassis alarm triggered — severity triage and root cause identification

## Prerequisites

- SSH or console access to the device (login class with `view` permissions minimum)
- JunOS 21.x or later (commands validated against JunOS 23.2+)
- Network reachability to management interface or fxp0 confirmed
- Awareness of the device's normal baseline (CPU, memory, traffic patterns)
- For dual-RE systems: know which RE should be master under normal operations
- Knowledge of recent commit history if correlating symptoms with changes

## Procedure

Follow this sequence. Each step produces data for the final report. RE mastership
verification is mandatory first — all subsequent data is RE-scoped.

### Step 1: Verify RE Mastership (Mandatory)

On dual-RE systems, health data comes from the RE you are logged into. If you
are on the backup RE, all metrics reflect the standby engine — not the active
forwarding path. This step is non-negotiable.

```
show chassis routing-engine | match "Slot|Current state|Mastership"
show route summary | match "Router ID"
show system uptime
```

Verify: your session is on the master RE. If `Current state` shows `Backup`,
switch to master: `request routing-engine login other-routing-engine`.

On single-RE platforms, confirm RE is `Master` (not in a degraded state).
Record: hostname, RE slot, mastership state, uptime, last reboot reason.
Short uptime after an unexpected reboot — investigate immediately.

### Step 2: Alarm Analysis

JunOS surfaces alarms as first-class status indicators. Check chassis and
system alarms before deeper investigation — alarms may already identify the
problem.

```
show chassis alarms
show system alarms
```

Alarm severities:
- **Major** — service-affecting condition, requires immediate attention
- **Minor** — degraded but service continues, investigate promptly

If alarms are present, record each alarm's class, description, and time.
Major alarms take priority over all other triage — address them first.
Common alarm sources: FPC offline, power supply failure, rescue config
not set, license expiry, FRU removal.

No alarms → proceed with systematic health assessment.

### Step 3: Routing Engine Health

RE handles control plane: routing protocols, management, commit operations.

```
show chassis routing-engine
show system processes extensive | match "PID|last pid|%CPU" | head 20
show task replication
```

Key fields from `show chassis routing-engine`:
- **CPU utilization** — temperature, idle percentage (idle below 30% is warning)
- **Memory utilization** — total and used; watch for used > 80%
- **Temperature** — compare to platform-specific thresholds
- **Start time** — recent RE restart indicates crash or failover
- **Load averages** — 1min/5min/15min; sustained > 1.0 per core is elevated

High RE CPU with top process identification:
- `rpd` — routing protocol daemon: route churn, table size, peer instability
- `chassisd` — chassis management: sensor polling issues, FPC communication
- `snmpd` — SNMP polling storms
- `mgd` — management: large config, slow commit, CLI session overload
- `kmd` — key management: IKE/IPsec negotiation storms (SRX)

RE CPU spikes during `commit` operations are normal (can hit 80–90% briefly).
Compare against commit history: `show system commit`.

### Step 4: PFE Health

PFE handles data plane forwarding independently from RE. A healthy RE with
a degraded PFE means traffic is being dropped even though the control plane
looks fine.

```
show chassis fpc
show chassis fpc detail
show pfe statistics traffic
show pfe statistics error
```

`show chassis fpc`:
- **State** must be `Online`. Any other state (`Present`, `Offline`, `Empty`)
  indicates a hardware issue or intentional deactivation.
- **CPU Total** — PFE CPU utilization; above 80% is warning, above 90% critical
- **Memory heap utilization** — above 80% indicates PFE memory pressure

`show pfe statistics traffic`:
- Compare input vs output packet counts — large delta indicates drops
- Check `fabric input drops` and `local input drops` for discard sources

`show pfe statistics error`:
- Any non-zero error counters warrant investigation
- Sustained incrementing errors (check twice 30 seconds apart) indicate active issues

On MX platforms with multiple FPCs, check each FPC individually. A single
degraded FPC affects only interfaces on that linecard.

### Step 5: System Resources

```
show system storage
show system memory
show system core-dumps
show system commit | head 10
```

**Storage:** JunOS partitions can fill from logs, core dumps, or failed upgrades.
Any partition above 85% used is warning. `/var` filling above 90% can prevent
commits and logging.

**Memory:** `show system memory` gives kernel-level view. Compare to RE memory
from Step 3 for consistency. Sustained growth without corresponding config
changes suggests a memory leak.

**Core dumps:** Presence of recent core files (within last 7 days) indicates
process crashes. Record the process name and timestamp — this is JTAC-relevant
data.

**Commit history:** Recent commits correlate with symptoms. A device that was
healthy before a commit and unhealthy after has an obvious investigation path.

### Step 6: Interface and Routing Health

```
show interfaces terse | match "down|err"
show interfaces extensive [name] | match "error|drop|CRC|carrier"
show route summary
show bgp summary
show ospf neighbor
show isis adjacency
```

For each interface with errors:
- CRC errors → Layer 1 (cabling, optics, SFP)
- Input errors without CRC → buffer overruns, MTU mismatch
- Output drops → congestion or policer drops
- Carrier transitions → link flap, check SFP DOM: `show interfaces diagnostics optics [name]`

Routing: verify expected neighbor count, all adjacencies in Established/Full state.
BGP prefix counts deviating > 10% from baseline indicate route churn.

### Step 7: Environment

```
show chassis environment
show chassis temperature-thresholds
show chassis power
show chassis fan
```

Check: all temperature sensors within thresholds, all power supplies OK, all
fans operational. Any environmental alarm maps directly to Major alarm severity.

On platforms with redundant RE: check both RE temperatures. A standby RE running
hot may indicate cooling issues even if master RE temperature is normal.

## Threshold Tables

Reference: `references/threshold-tables.md` for detailed per-parameter thresholds.

| Parameter | Normal | Warning | Critical | Notes |
|-----------|--------|---------|----------|-------|
| RE CPU idle | > 40% | 20–40% | < 20% | Spikes during commit are normal |
| RE memory used | < 75% | 75–85% | > 85% | |
| RE load avg (1min) | < 0.7/core | 0.7–1.5/core | > 1.5/core | Scale by RE core count |
| PFE CPU | < 60% | 60–80% | > 80% | Per-FPC |
| PFE heap used | < 70% | 70–85% | > 85% | Per-FPC |
| Storage partition | < 80% | 80–90% | > 90% | /var critical for commits |
| Interface error rate | < 0.01% | 0.01–0.1% | > 0.1% | |
| Output drops/hr | < 100 | 100–1000 | > 1000 | |
| Chassis alarm | None | Minor present | Major present | |
| Temperature | Within spec | 5°C of max | At/above max | Per-sensor |

## Decision Trees

### Primary Triage

```
Is the device reachable?
├── No → Check console, power, environment. Collect core dumps after recovery.
└── Yes
    ├── Verify RE mastership → On master RE?
    │   ├── No → Switch to master RE, restart triage
    │   └── Yes → Continue
    │
    ├── Chassis/system alarms present?
    │   ├── Major alarm → Address immediately
    │   │   ├── FPC offline → show chassis fpc detail, check PFE
    │   │   ├── Power supply failure → show chassis power, environment
    │   │   ├── RE failover → show chassis routing-engine, check standby
    │   │   └── Other Major → Collect alarm detail, escalate
    │   ├── Minor alarm → Note for report, continue triage
    │   └── No alarms → Continue systematic assessment
    │
    ├── RE CPU issue?
    │   ├── rpd high → Route churn: check BGP/OSPF/ISIS neighbors
    │   ├── chassisd high → FPC/sensor communication: check chassis fpc
    │   ├── snmpd high → Polling storm: check SNMP community/clients
    │   ├── mgd high → Commit or CLI overload: check system commit
    │   ├── kmd high → IKE storms (SRX): check IPsec SA count
    │   └── Recent commit correlates → Rollback candidate
    │
    ├── PFE issue? (RE healthy but traffic drops)
    │   ├── FPC not Online → Hardware issue, check fpc detail
    │   ├── PFE CPU > 80% → Forwarding overload
    │   │   └── Check traffic rates, filter complexity, NH resolution
    │   ├── PFE drops incrementing → Identify drop category
    │   │   ├── Fabric drops → Linecard-to-fabric issue
    │   │   ├── Local drops → Punt/exception path overload
    │   │   └── Discard → Filter or policer drops (may be expected)
    │   └── PFE memory pressure → Session/route table exhaustion
    │
    ├── Memory issue?
    │   ├── RE memory > 85% → Identify top consumers via processes
    │   ├── Storage > 90% → Clean logs, core dumps, old images
    │   │   └── /var full → Immediate: prevents commits and logging
    │   └── Core dumps present → Process crash, collect for JTAC
    │
    ├── Interface errors? → Classify error type
    │   ├── CRC/input errors → Layer 1 (cable, optic, SFP)
    │   ├── Output drops → QoS policer or congestion
    │   └── Carrier transitions → Link flap, check optics DOM
    │
    └── All within thresholds → Document clean health
```

### Alarm Severity Triage

```
Alarm detected
├── Major alarm?
│   ├── FPC Offline
│   │   ├── Single FPC → Affects only interfaces on that linecard
│   │   ├── check: show chassis fpc detail [slot]
│   │   └── Action: power cycle FPC if transient, RMA if persistent
│   ├── Power Supply Failure
│   │   ├── Redundancy lost → Immediate replacement
│   │   └── Both PSUs failed → Emergency, device at risk
│   ├── RE Failover
│   │   ├── Was this planned? → Verify new master is healthy
│   │   └── Unplanned → Investigate old master: show chassis routing-engine
│   └── Other Major → Collect detail, open JTAC case
│
└── Minor alarm?
    ├── Rescue config not set → `request system configuration rescue save`
    ├── License expiry → Check feature impact, plan renewal
    ├── FRU removal → Verify intentional, document
    └── Other Minor → Note in report, monitor
```

### Escalation Criteria

Escalate to senior engineer or JTAC when:
- RE CPU sustained above 90% for 15+ minutes with no identifiable cause
- RE memory above 90% used with no recent config change
- PFE offline or in non-Online state after power cycle attempt
- Core dumps present from critical processes (rpd, chassisd, pfed)
- Major chassis alarm with no clear remediation
- Multiple FPC failures or fabric errors
- RE failover loop (multiple failovers in short period)
- Any environmental alarm (power, fan, temperature)
- More than 3 routing neighbor state changes in the last hour

## Report Template

```
DEVICE HEALTH REPORT
====================
Device: [hostname]
Platform: JunOS
Model: [from show chassis hardware]
Software: [JunOS version]
RE Slot: [RE0 or RE1]
Mastership: [Master — verified]
Uptime: [uptime string]
Check Time: [timestamp]
Performed By: [operator/agent]

SUMMARY: [HEALTHY | WARNING | CRITICAL | EMERGENCY]

ALARMS:
  Chassis: [count] ([Major: n, Minor: n] or None)
  System: [count] ([Major: n, Minor: n] or None)
  Details: [alarm descriptions if present]

FINDINGS:
1. [Severity] [Component] — [Description]
   Domain: [RE | PFE | Chassis | Interface | Routing]
   Observed: [metric value]
   Threshold: [normal/warning/critical range]
   Action: [recommended action]

2. ...

RE/PFE STATUS:
  RE: [healthy/degraded/critical] — CPU idle: [n]%, Memory: [n]% used
  PFE: [per-FPC state summary]
  Dual-RE: [master/backup state, or N/A for single-RE]

RECOMMENDATIONS:
- [Prioritized action list]

NEXT CHECK: [date based on severity — CRITICAL: 24hr, WARNING: 7d, HEALTHY: 30d]
```

## Troubleshooting

### Device Unresponsive to SSH

Try console access. If console is also unresponsive, check power and environment
via out-of-band management (craft interface, console server). After recovery:
`show system core-dumps`, `show chassis routing-engine` for reboot reason,
`show log messages | match "kernel|panic|watchdog"`.

### Logged Into Backup RE

If `show chassis routing-engine` shows your RE as `Backup`, you are collecting
standby metrics. Switch to master: `request routing-engine login other-routing-engine`.
If master RE is unreachable from backup, this indicates master RE failure — check
`show chassis routing-engine` from backup for master's last known state.

### RE CPU Spikes During Commit

JunOS RE CPU can spike to 80–90% during commit operations. This is expected
behavior — the config daemon and rpd both consume CPU during commit processing.
Verify: `show system commit` to confirm a recent commit, then wait 2–3 minutes
and re-check. Sustained high CPU after commit settles indicates a real problem.

### PFE Drops With Healthy RE

The RE (control plane) and PFE (data plane) are independent. High PFE drops with
a normal RE means traffic is being discarded at the forwarding level. Check:
`show pfe statistics traffic` for drop categories, `show chassis fpc detail`
for PFE CPU and memory. Common causes: filter/policer drops (may be expected),
next-hop resolution failures, PFE memory exhaustion from large tables.

### Storage Full Preventing Commits

If `/var` is above 95%, commits will fail. Clear space:
`request system storage cleanup` — removes old logs, core dumps, and temporary
files. If that is insufficient: `show system storage` to identify the largest
consumers, then selectively remove old software images or rotated log files.

### Dual-RE Failover Investigation

After an RE failover: verify new master is healthy (Steps 1–3), then investigate
the old master. From the new master: `show chassis routing-engine` shows both
REs' state. Check `show log messages | match "mastership|failover|switchover"`
for the event trigger. Common causes: RE crash (core dump present), watchdog
timeout, manual switchover, GRES/NSR failure.
