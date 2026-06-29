---
name: mtconnect-tap
description: >-
  Read CNC machine tools via MTConnect (the royalty-free standard for ALL machine
  tools — Fanuc/Siemens/Haas/Mazak/Okuma controllers with an agent). Probe the
  device model, read current values, pull a bounded sample stream, list assets
  (cutting tools/programs), and get an OEE-inputs snapshot (availability/execution
  /mode/program). Use when the task names MTConnect, a CNC/machine-tool agent, or
  an agent REST URL. Routes to the ot-aiops MCP server. Read-only by spec. For
  OPC-UA/Modbus/Siemens/Mitsubishi/MQTT use the sibling *-tap skills; not for
  IT/network gear, Kubernetes, hypervisors, or backups.
---

# mtconnect-tap

Read-only CNC machine-tool telemetry via the **ot-aiops** MCP server. MTConnect
is **read-only by specification** (HTTP REST + XML). Preview — validated against
static XML fixtures, NOT a live agent.

## When to use
- A machine tool exposing an MTConnect agent (`agent_url`, e.g. `http://host:5000`).
- Discover the device model, read current/sample values, OEE inputs, assets.

## When NOT to use (routing)
- OPC-UA → `opcua-tap`; Modbus → `modbus-tap`; Siemens → `s7-tap`; Mitsubishi →
  `mc-tap`; MQTT/UNS → `sparkplug-tap`; cross-protocol triage →
  `industrial-diagnostics`. IT/network/Kubernetes/hypervisor/backup → not this tool.

## Tools (all read-only)

| Tool | Params | Returns |
|------|--------|---------|
| `mtconnect_probe` | `endpoint?` | `{devices:[{name,uuid,components:[{component,data_items:[{id,type,category,units}]}]}]}` |
| `mtconnect_current` | `endpoint?` | `{observations:[{data_item_id,type,name,timestamp,value}]}` |
| `mtconnect_sample` | `endpoint?, count=100` | `{observation_count, observations:[...]}` (bounded) |
| `mtconnect_assets` | `endpoint?` | `{assets:[{asset_type,asset_id,timestamp}]}` |
| `mtconnect_oee_snapshot` | `endpoint?` | `{availability, execution, controller_mode, program, available, running, verdict}` |

Call `mtconnect_probe` first to learn dataItem ids/types, then read values.

## Example
`mtconnect_oee_snapshot(endpoint="vmc1")` →
`{"availability":"AVAILABLE","execution":"ACTIVE","program":"O1234","verdict":"running"}`

## Setup
`ot-aiops init` (mtconnect: agent_url) · `ot-aiops doctor` · `ot-aiops mcp`. Test
against the public MTConnect demo agent. `mtconnect_oee_snapshot` surfaces OEE
*inputs* — full OEE % needs planned-time + ideal-cycle context the standard does
not expose. 缺功能提 issue/PR 欢迎留言.
