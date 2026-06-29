---
name: industrial-analytics
description: >-
  Cross-protocol, READ-ONLY OT analytics via the ot-aiops MCP server. oee_compute
  derives OEE = Availability × Performance × Quality from production inputs;
  downtime_events auto-detects and categorizes machine stoppages (changeover /
  material / mechanical / quality / break) from a state series; oee_multidim
  aggregates OEE across machine × part × shift; asset_inventory actively
  fingerprints configured devices (vendor/model/firmware) into an asset register;
  monitor_changes captures bounded change-of-value (only the changes). Use when the
  task is OEE, downtime/stoppage analysis, availability/performance/quality, asset
  inventory / device fingerprint / IEC 62443 register, or change-of-value
  monitoring. Not for IT/network/Kubernetes/hypervisor/backup.
---

# industrial-analytics

The cross-protocol analytics layer of **ot-aiops** (read-only). Structured JSON for
an agent to visualize. The OEE/downtime analyzers operate over **provided/collected
inputs** (fully testable without a plant); asset-inventory and monitor_changes
actively read configured endpoints.

## When to use
- OEE / downtime / stoppage categorization; multi-dimensional OEE matrices.
- Active asset inventory / device fingerprint (IEC 62443-flavored register).
- Bounded change-of-value (deadband-report) capture on a point.

## When NOT to use
- Single-tag reads → the matching protocol *-tap skill.
- "No data"/alarm-flood/tag-quality triage → `industrial-diagnostics`.
- IT/network/Kubernetes/hypervisor/backup → not this tool.

## Tools

### `oee_compute(planned_time_s, run_time_s, ideal_cycle_time_s, total_count, good_count)`
OEE = Availability × Performance × Quality. Returns
`{availability, performance, quality}` (each `{raw, value, capped}`), `oee`,
`oee_pct`, `inputs`, `losses`. Each factor is reported raw + clamped to [0,1]; a
`capped` performance >1.0 flags an optimistic ideal cycle time.

### `downtime_events(series, category_map?, min_duration_s=0)`
`series:[{timestamp, state}]` (state = string/bool/number). Detects every
running→stopped span and returns
`{event_count, total_downtime_s, by_category:{cat:{count,downtime_s}},
events:[{start, end, duration_s, state, category}]}`. Categories: changeover /
material / mechanical / quality / break / unknown (keyword heuristics, or a
`{state: category}` override).

### `oee_multidim(records, dimensions=["machine","part","shift"])`
`records:[{<dimensions>, planned_time_s, run_time_s, ideal_cycle_time_s,
total_count, good_count}]` → `{group_count, mean_oee, worst_performers[...],
matrix:[{dimensions, oee, oee_pct, availability, performance, quality}]}`.

### `asset_inventory(endpoints?)`
ACTIVELY connects to each configured (or named) endpoint and reads its identity
(S7 CPU info, EtherNet/IP controller info, OPC-UA build info, Modbus FC43, MELSEC
CPU, MTConnect device). Returns `{asset_count, reachable_count, method:
'active_fingerprint', assets:[{endpoint, protocol, address, vendor, model,
firmware, serial, reachable, last_seen}]}`. **Honest scope: ACTIVE fingerprinting
(we connect to each device), NOT passive SPAN/tap discovery** (roadmap).

### `monitor_changes(ref, endpoint?, duration_s=10, interval_ms=500, deadband=0, max_changes=100)`
Bounded change-of-value: polls a point and returns **only the changes** (with
timestamps), never every sample and never an open loop. Works over OPC-UA / Modbus
/ S7 / Mitsubishi MC / EtherNet/IP. Hard-capped by `duration_s` (≤120) and
`max_changes` (≤500).

## Example
`oee_compute(planned_time_s=28800, run_time_s=25200, ideal_cycle_time_s=2.0,
total_count=12000, good_count=11800)` →
`{"availability":{"value":0.875},"performance":{"value":0.952},
"quality":{"value":0.983},"oee":0.819,"oee_pct":81.94}`

## CLI
```bash
ot-aiops analytics oee 28800 25200 2.0 12000 11800
ot-aiops analytics downtime --input states.json
ot-aiops analytics oee-multidim --input records.json
ot-aiops analytics asset -e press1 -e cell5
ot-aiops opcua monitor "ns=2;i=5" -e line1 --duration-s 20 --deadband 0.5
```

## Safety
Strictly read-only — never writes. asset_inventory adds light connection load to
each device. 缺功能提 issue/PR 欢迎留言.
