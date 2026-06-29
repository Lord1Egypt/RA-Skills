---
name: industrial-diagnostics
description: >-
  Cross-protocol, READ-ONLY OT troubleshooting via the ot-aiops MCP server.
  diagnose_dataflow localizes a "no data" break (cannot connect vs stale value vs
  flatline sensor) across any endpoint's reachable hops; alarm_bad_actors runs
  ISA-18.2 alarm-flood analysis (rate vs thresholds, Pareto offenders, chattering,
  standing); tag_health ranks bad-quality/flatline/out-of-range/anomaly offenders;
  historian_health finds flatline/gaps over a sample series. Use when the task is
  "why is there no data / why did the dashboard go blank", alarm flooding, bad
  actors, stuck/flatline tags, or general OT data-quality triage. Not for
  IT/network/Kubernetes/hypervisor/backup troubleshooting.
---

# industrial-diagnostics

The cross-protocol intelligence layer of **ot-aiops** (read-only). Structured
JSON outputs are designed for an agent to visualize multi-dimensionally. Preview —
diagnoses the layers reachable from this host and accepts injected series for the
historian/SCADA tiers it cannot reach.

## When to use
- "No data" / blank dashboard triage; alarm floods; bad-actor tags; stuck sensors.
- After a protocol *-tap skill connects, to reason about *why* values are wrong.

## When NOT to use
- Single-tag reads → use the matching protocol *-tap skill directly (incl.
  `ethernetip-tap` for Rockwell/Allen-Bradley Logix).
- OEE / downtime / asset inventory / change-of-value → `industrial-analytics`.
- IT/network/Kubernetes/hypervisor/backup → not this tool.

## Tools

### `diagnose_dataflow(endpoint?, ref?, freshness_threshold_s=60, series?, flatline_eps?)`
Probes connect → read(ref) → freshness → variance. Returns
`{verdict, diagnosis, recommended_action, hops:[{hop, ok, detail}]}` where
`verdict` ∈ `cannot_connect` (network/PLC down) · `comms_ok_value_unreadable`
(wrong address) · `comms_ok_bad_quality` (sensor/source fault) ·
`comms_ok_value_stale` (upstream stopped updating) · `comms_ok_flatline`
(stuck source) · `healthy`. Works over any protocol (`ref` = OPC-UA node id /
Modbus address / S7 address / MELSEC device). Pass `series` (scalars or
`{value,timestamp}`) for freshness/variance when a historian is out of reach.

### `alarm_bad_actors(events, window_minutes?, chatter_window_s=60, standing_s=86400, top_n=10)`
ISA-18.2 over `events:[{source, timestamp, priority?, state?}]`. Returns
`{alarms_per_hour, isa_18_2:{ok_max:6,manageable_max:12,flood_min:30},
flood_verdict, priority_distribution, pareto_sources_for_80pct,
top_offenders:[{source,count,share_pct,chattering,standing}], chattering[...],
standing[...]}`.

### `tag_health(tags, thresholds?)`
`tags:[{ref, samples:[scalar|{value,good|quality}], warn_high?, alarm_high?, ...}]`.
Returns `{overall, offenders:[{ref, latest, flags, anomaly_count, severity 0..3}]}`.
Flags: bad_quality, flatline, out_of_range_warn/alarm, statistical_anomaly
(z-score >3σ and IQR fence).

### `historian_health(series, gap_threshold_s=60, flatline_eps?)`
`series:[scalar|{value,timestamp,quality|good}]` → `{bad_quality_count, flatline,
gap_count, gaps[...], verdict ('ok'|'degraded'|'gappy'|'flatline'|'bad_tag')}`.

## Example
`diagnose_dataflow(endpoint="line1", ref="ns=2;i=5", freshness_threshold_s=30)`
→ `{"verdict":"comms_ok_value_stale","diagnosis":"... value is STALE ...",
"recommended_action":"Trace upstream ...","hops":[...]}`

## Safety
Strictly read-only — never writes. 缺功能提 issue/PR 欢迎留言.
