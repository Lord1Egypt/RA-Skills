---
name: network-log-analysis
description: >-
  Device-level network log analysis using raw syslog data without SIEM
  platforms. Guides forensic timeline construction from rsyslog/syslog-ng
  collectors, device console logs, and SNMP trap data. Covers syslog
  pattern recognition across Cisco IOS-XE, Juniper JunOS, and Arista EOS
  message formats, multi-device event correlation using grep/awk/sort,
  anomaly detection via baseline deviation, and chronological timeline
  reconstruction with NTP-aware timestamp normalization.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"📊","safetyTier":"read-only","requires":{"bins":[],"env":[]},"tags":["syslog","log","anomaly"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# Network Log Analysis

Device-level syslog analysis and forensic timeline construction without
SIEM platforms. This skill covers raw log data from rsyslog/syslog-ng
collectors, device console output, and SNMP trap receivers — all
analysis uses standard Unix tools (grep, awk, sort, sed).

For environments with a SIEM platform, use the companion skill
siem-log-analysis which provides the same forensic reasoning with
platform-specific query syntax.

Reference `references/cli-reference.md` for rsyslog/syslog-ng
configuration, device syslog commands, and log parsing one-liners.
Reference `references/syslog-patterns.md` for vendor-specific message
formats, the RFC 5424 facility/severity matrix, and common event
pattern catalogs.

## When to Use

- **No SIEM available** — investigate network events using only raw
  syslog files on a centralized collector or individual device logs
- **Syslog infrastructure audit** — verify that rsyslog or syslog-ng
  is correctly receiving, routing, and retaining logs from all network
  devices in scope
- **Multi-device event correlation** — construct a unified timeline
  from separate per-device or per-facility log files using timestamp
  sorting and pattern matching
- **Anomaly investigation** — identify deviations from normal log
  volume, new message types, or authentication failure clusters
  without statistical query engines
- **Post-incident timeline reconstruction** — assemble a chronological
  evidence chain from raw logs after a network outage or security event
- **Log retention compliance** — verify that log rotation policies
  and retention periods meet organizational or regulatory requirements

## Prerequisites

- **Syslog collector access** — SSH or console access to the
  rsyslog/syslog-ng server with read permissions on log directories
  (typically `/var/log/` or custom paths defined in collector config)
- **Device CLI access** — Read-only credentials for network devices
  to verify syslog forwarding configuration and NTP synchronization
  status
- **Unix tool availability** — `grep`, `awk`, `sort`, `sed`, `wc`,
  and `date` available on the syslog collector (standard on any
  Linux/BSD system)
- **NTP verification** — Confirm time synchronization across all
  network devices and the syslog collector before multi-device
  correlation; skewed clocks corrupt timeline accuracy
- **Log file identification** — Know the log file paths, naming
  conventions, and rotation schedule on the collector; rsyslog and
  syslog-ng route logs differently based on facility, severity, and
  source address

## Procedure

Follow these six steps sequentially. The procedure builds a forensic
timeline from raw syslog evidence through pattern recognition,
correlation, anomaly detection, and chronological reconstruction.
Each step produces artifacts that feed subsequent steps.

### Step 1: Log Collection Assessment

Verify that the syslog infrastructure is complete and healthy before
analyzing log content. Missing or misconfigured sources create blind
spots that invalidate investigation conclusions.

**Syslog server configuration** — Examine the collector configuration
to understand how logs are routed:

- **[rsyslog]** — Review `/etc/rsyslog.conf` and `/etc/rsyslog.d/*.conf`
  for input modules (imudp, imtcp, imrelp), facility/severity routing
  rules, and output file templates. Confirm that `$ActionFileDefaultTemplate`
  includes the source hostname for multi-device disambiguation.
- **[syslog-ng]** — Review `/etc/syslog-ng/syslog-ng.conf` for source
  definitions (network listeners), filter chains (facility, severity,
  host match), and destination paths. Verify that `keep-hostname(yes)`
  preserves the originating device hostname.

**Device syslog verification** — On each in-scope network device,
confirm syslog forwarding is active and targeting the correct collector:

- **[Cisco]** — `show logging` confirms logging host, trap level, and
  facility; `show logging history` shows recent buffered severity counts
- **[JunOS]** — `show system syslog` shows configured host targets,
  facility filters, and structured-data enablement
- **[EOS]** — `show logging` shows syslog server address, logging level,
  and protocol (UDP/TCP)

**NTP synchronization check** — Verify on each device:

- **[Cisco]** — `show ntp status` (stratum, offset)
- **[JunOS]** — `show system ntp` (peer status, offset)
- **[EOS]** — `show ntp status` (clock state, stratum)

Devices with NTP offset exceeding 1 second require timestamp correction
before correlation.

**Log retention and rotation** — Check logrotate configuration for
retention period, compression, and file size limits. Confirm the
retention window covers the investigation period. Missing rotated
files indicate evidence gaps.

### Step 2: Syslog Pattern Recognition

Parse raw syslog messages into structured fields using vendor-specific
format knowledge. Pattern recognition transforms unstructured text into
correlatable evidence.

**Vendor message formats:**

- **[Cisco]** — `%FACILITY-SEVERITY-MNEMONIC: message`. Facility
  identifies the subsystem (LINEPROTO, OSPF, SEC), severity is 0–7
  (RFC 5424), mnemonic is the event identifier.
- **[JunOS]** — `hostname process[pid]: EVENT_ID: message`. When
  `structured-data` is enabled, adds `[tag value]` pairs.
- **[EOS]** — `hostname AgentName: %FACILITY-SEVERITY-message`.
  Agent name identifies the subsystem (Ebra, Bgp, Ospf).

**Severity classification** — Extract the severity digit and map to
RFC 5424 levels (0=Emergency through 7=Debug). Filter scope to
severity 0–4 (Emergency through Warning) for operationally significant
events. Use severity 5–7 only when lower severities lack context.

**Message frequency baseline** — Count messages per facility per hour
to establish normal volume:

```
awk '{print $1, $2, $3}' /var/log/network.log | sort | uniq -c | sort -rn
```

This produces a timestamp-grouped frequency table. Significant
deviations from the hourly mean indicate events worth investigating.

**Facility-to-subsystem mapping** — Map syslog facility codes to
network subsystems using `references/syslog-patterns.md`. Facility
local0–local7 assignments vary per organization — check the rsyslog
routing rules from Step 1 to decode local facility meanings.

### Step 3: Event Correlation

Join events from multiple devices and log files by shared attributes
to build investigation threads from isolated messages.

**Multi-device timeline via grep/awk/sort** — Merge per-device log
files into a single chronologically sorted stream:

```
cat /var/log/rtr*.log /var/log/sw*.log | sort -k1,3 > /tmp/merged-timeline.log
```

If log files use different timestamp formats, normalize first with
awk before merging (see Step 5 for timestamp normalization details).

**Temporal clustering** — Identify events within a configurable time
window of a known trigger event. For precision, convert timestamps to
epoch seconds and select events within the desired window using awk
numeric comparison (see `references/cli-reference.md` for correlation
helpers).

**Causal chain detection** — Network failures propagate through
protocol dependencies in predictable patterns: interface flap
(`LINK-3-UPDOWN`) → OSPF neighbor down (`OSPF-5-ADJCHG`) → BGP route
withdrawal (`BGP-5-ADJCHANGE`) → traffic reroute on alternate paths.
Search for cascading patterns by extracting events matching each stage
and verifying temporal sequence.

**SNMP trap correlation** — If the collector receives SNMP traps
(via snmptrapd), correlate trap OIDs with syslog events. Interface
linkDown traps (OID 1.3.6.1.6.3.1.1.5.3) should pair with LINK-UPDOWN
syslog messages from the same device. Mismatches indicate logging gaps.

### Step 4: Anomaly Detection

Compare observed log patterns against baselines to surface deviations
that warrant investigation. All detection uses grep, awk, and sort
against raw log files.

**Baseline deviation** — Compare current-day event counts per device
against the rolling 7-day average. A current-day count exceeding
twice the average signals a volume anomaly. Calculate per-facility
counts to pinpoint which subsystem generates excess messages.

**New or unseen message types** — Extract unique mnemonics from
the investigation window and compare against a baseline file:

```
grep -oP '%\S+-\d-\S+' /var/log/cisco.log | sort -u > /tmp/current.txt
comm -23 /tmp/current.txt /tmp/baseline-mnemonics.txt
```

Mnemonics present in current but absent from baseline are first-seen
events requiring classification.

**Authentication failure clustering** — Extract auth messages and
group by source IP using grep/awk/sort (see `references/cli-reference.md`
for one-liners). Source IPs with failure counts exceeding 10 per hour
warrant investigation as potential brute-force attempts.

**Config changes outside maintenance windows** — Filter for config
change messages (SYS-5-CONFIG_I, UI_COMMIT) and check timestamps
against the approved schedule. Changes outside the window require
attribution — who changed what, and was it authorized.

**Login source IP anomalies** — Extract management session source IPs
and compare against the authorized management subnet list. IPs outside
known ranges indicate unauthorized access attempts.

### Step 5: Timeline Reconstruction

Assemble a definitive chronological event sequence from all evidence
gathered in Steps 1–4. The timeline is the primary deliverable of
forensic log analysis.

**Chronological assembly** — Merge relevant events from multiple
log sources into a single sorted output:

```
grep -h "PATTERN1\|PATTERN2\|PATTERN3" /var/log/*.log | sort -k1,3
```

Use `sort -s -k1,3` (stable sort) to preserve original order of
events with identical timestamps.

**NTP-aware timestamp normalization** — If devices log in different
timezones or formats, normalize all timestamps to UTC epoch seconds
before sorting. Convert RFC 3164 timestamps with awk piped to `date`
(see `references/cli-reference.md` for conversion one-liners). Apply
the NTP offset correction from Step 1 to events from devices with
known clock drift. For BSD/macOS, use `date -jf` instead of `date -d`.

**Event-to-impact mapping** — For each significant event in the
timeline, annotate the user-visible impact:

1. Identify the event (e.g., `OSPF-5-ADJCHG neighbor down`)
2. Determine the network impact (loss of redundant path)
3. Map to the user symptom (degraded connectivity or failover latency)

**Root cause ordering** — Walk the timeline backward from the
user-reported symptom to the earliest causal event. The root cause
is the first event that, if prevented, would have prevented all
downstream effects. Document the causal chain with event references
for each link.

### Step 6: Report

Compile all findings into a structured deliverable. Present the event
timeline from Step 5 as the central artifact — annotate each entry
with its classification (root cause, contributing factor, symptom,
or informational). Summarize anomaly findings from Step 4 with counts
and severity assessments. Document correlation chains from Step 3
with supporting evidence. State the root cause assessment with
confidence level and the supporting evidence chain. Include an
integrity section listing evidence gaps that limit conclusions.

## Threshold Tables

### Log Volume Anomaly Thresholds

| Metric | Normal | Warning (>1.5×) | Alert (>2×) | Critical (>3×) |
|--------|--------|-----------------|-------------|-----------------|
| Messages per hour (per device) | Baseline ± 50% | 1.5–2× baseline | 2–3× baseline | >3× baseline |
| Unique mnemonics per day | Baseline count | 1–3 new mnemonics | 4–10 new mnemonics | >10 new mnemonics |
| Auth failure events (per source IP) | ≤3/hour | 4–10/hour | 11–50/hour | >50/hour |
| Config change events (per device) | ≤2/day during windows | Any outside window | 3+ outside window | >5 outside window |
| SNMP trap rate (per device) | ≤5/hour | 6–20/hour | 21–100/hour | >100/hour |

### Syslog Severity Response Matrix

| Severity | RFC 5424 Level | Investigation Action |
|----------|---------------|---------------------|
| 0 — Emergency | System unusable | Immediate investigation, all-hands |
| 1 — Alert | Immediate action needed | Priority investigation within 15 minutes |
| 2 — Critical | Critical conditions | Investigation within 1 hour |
| 3 — Error | Error conditions | Investigation within 4 hours |
| 4 — Warning | Warning conditions | Review within 24 hours |
| 5 — Notice | Normal but significant | Log for trending, review weekly |
| 6 — Info | Informational | Baseline data, no action |
| 7 — Debug | Debug-level | Exclude from standard analysis |

### Correlation Confidence Levels

| Confidence | Criteria | Action |
|------------|----------|--------|
| **Confirmed** | 3+ events across 2+ devices with matching attributes and <60s window | Treat as established fact in report |
| **Probable** | 2 correlated events or single-device chain with supporting evidence | Include in report with qualification |
| **Possible** | Single event or loose time correlation (>5 min window) | Note as hypothesis, do not assert as finding |

## Decision Trees

### Investigation Entry Point

```
Investigation trigger received
├── Reported outage with known time window?
│   ├── Yes → Start at Step 3 (Correlation) scoped to window
│   │   └── Expand to Step 2 (Pattern Recognition) if correlation
│   │       yields insufficient events
│   └── No → Start at Step 1 (Log Collection Assessment)
│
├── Anomaly detected in monitoring (no log detail)?
│   ├── Time of anomaly known? → Start at Step 4 (Anomaly Detection)
│   │   └── Confirm with Step 2 pattern analysis
│   └── Time unknown? → Full procedure Steps 1–6
│
├── Post-incident review (incident already resolved)?
│   └── Start at Step 1 → Full procedure for completeness
│       └── Focus Step 5 (Timeline) for the deliverable
│
└── Compliance audit of syslog infrastructure?
    └── Steps 1 and 2 only (Collection + Pattern verification)
```

### Anomaly Classification

```
Anomaly identified in Step 4
├── Volume anomaly (message count deviation)?
│   ├── Single device affected?
│   │   ├── Device reload or maintenance → Expected, document
│   │   └── No maintenance → Investigate device health
│   └── Multiple devices affected?
│       ├── Shared upstream link event? → Correlate in Step 3
│       └── Independent spikes? → Investigate each separately
│
├── New mnemonic or event type?
│   ├── Matches known firmware upgrade pattern? → Expected
│   ├── Security-related facility (SEC, AUTH)? → Priority review
│   └── Informational facility? → Add to baseline if benign
│
├── Authentication anomaly?
│   ├── Single source IP, many targets? → Brute-force scanning
│   ├── Many source IPs, single target? → Distributed attack
│   └── Single source, single target? → Credential issue
│
└── Configuration change outside window?
    ├── Attributed to known admin? → Verify authorization
    ├── Attributed to unknown user? → Security incident
    └── No attribution available? → Escalate immediately
```

## Report Template

```
NETWORK LOG ANALYSIS REPORT
==============================
Report ID: [unique identifier]
Investigation Trigger: [outage report / anomaly alert / compliance audit]
Investigation Window: [start timestamp] — [end timestamp] (UTC)
Analyst: [name/identifier]
Log Sources: [collector hostname, device count, log file paths]

SUMMARY:
- Investigation type: [outage / security / compliance / anomaly]
- Root cause confidence: [Confirmed / Probable / Possible]
- Devices involved: [count and hostnames]
- Evidence gaps: [list any missing log sources or time gaps]

LOG COLLECTION STATUS (Step 1):
- Syslog collector: [rsyslog / syslog-ng, config path]
- Devices forwarding: [count] / [total expected]
- NTP synchronized: [count] / [total], max offset: [ms]
- Retention coverage: [days available] vs [days needed]

EVENT TIMELINE (Step 5):
| # | Timestamp (UTC) | Device | Facility-Sev | Mnemonic/Event | Message Summary | Classification |
|---|-----------------|--------|-------------|----------------|-----------------|----------------|
| 1 | [time] | [host] | [fac-sev] | [mnemonic] | [summary] | [root cause / contributing / symptom] |

ANOMALIES DETECTED (Step 4):
| # | Type | Device(s) | Description | Severity |
|---|------|-----------|-------------|----------|

CORRELATION CHAINS (Step 3):
- Chain 1: [event A] → [event B] → [event C]
  Confidence: [Confirmed / Probable / Possible]

ROOT CAUSE ASSESSMENT:
- Root cause: [description]
- Confidence: [level with justification]
- Causal chain: [first event → ... → user impact]

EVIDENCE INTEGRITY:
- Gaps: [missing devices, time periods, rotated files]
- NTP corrections applied: [list any offset adjustments]

RECOMMENDATIONS:
1. [immediate — e.g., fix syslog forwarding gap, address root cause]
2. [short-term — e.g., add missing devices to collector, tune rotation]
3. [long-term — e.g., improve NTP architecture, add log redundancy]
```

## Troubleshooting

### Missing Device Logs on Collector

**Symptom:** Expected device logs are absent from syslog collector files
despite the device being configured to forward syslog.

**Diagnosis:** Verify syslog configuration on the device (see Step 1
commands). Check network path — firewall rules may block UDP 514 or
TCP 514 between the device and collector. On the collector, check
rsyslog/syslog-ng for dropped messages: `rsyslogd` logs input errors
to its own syslog facility. Verify the collector is listening on the
expected port with `ss -ulnp | grep 514`.

**Resolution:** Fix the forwarding path (device config, network ACLs,
collector listener). Generate a test message from the device and confirm
receipt. Document the gap period in the investigation report.

### Timestamp Format Inconsistencies

**Symptom:** Merged log files produce an unsortable timeline because
timestamp formats differ (RFC 3164 vs RFC 5424 vs device-specific).

**Diagnosis:** Inspect the first 10 lines of each source. RFC 3164
uses `Mmm dd HH:MM:SS` (no year); RFC 5424 uses ISO 8601 with timezone.

**Resolution:** Write an awk normalizer for each format (see Step 5
and `references/cli-reference.md`). Add the year to RFC 3164 timestamps
based on file modification date or logrotate naming convention.

### Log Rotation Destroyed Evidence

**Symptom:** Investigation period extends beyond the oldest available
log file.

**Diagnosis:** Check `/etc/logrotate.d/` for retention and compression
settings. Look for compressed archives (`.gz`, `.bz2`, `.xz`).

**Resolution:** Search within compressed files using `zgrep` or
`zcat | grep`. If data is permanently lost, document the gap and state
which conclusions are limited by missing evidence.

### High Log Volume Makes grep Impractical

**Symptom:** Multi-GB log files make interactive grep analysis
impractically slow.

**Resolution:** Narrow to the investigation window with a date-based
grep first, redirect to a working file, then apply detailed analysis
to the smaller extract. Use `LC_ALL=C grep` for faster processing.
Consider GNU parallel for multi-file analysis.
