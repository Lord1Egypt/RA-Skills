---
name: mc-tap
description: >-
  Read Mitsubishi MELSEC PLCs (三菱 Q/L/QnA/iQ-R/iQ-L) over the MC protocol (3E
  binary, pymcprotocol) — CPU type, word devices (D/W/R), bit devices (M/X/Y/B),
  and scattered random reads. A governed, MOC-gated word write exists but is OFF
  by default. Use when the task names Mitsubishi/MELSEC, a D/M/X/Y device, or
  plctype Q/L/iQ-R. Routes to the ot-aiops MCP server. For OPC-UA/Modbus/Siemens/
  MTConnect/MQTT use the sibling *-tap skills; not for IT/network gear,
  Kubernetes, hypervisors, or backups.
---

# mc-tap

Mitsubishi MC read-first telemetry via the **ot-aiops** MCP server, using
**pymcprotocol** (pure Python, MELSEC 3E binary). Preview — validated against a
mocked client, NOT live PLCs. Only the 3E frame is supported (1E/4E are not).

## When to use
- A Mitsubishi Q/L/iQ-R/iQ-L PLC with an Ethernet module open for MC (`host:5007`).
- Read word/bit devices; check CPU type.

## When NOT to use (routing)
- OPC-UA → `opcua-tap`; Modbus → `modbus-tap`; Siemens → `s7-tap`; CNC →
  `mtconnect-tap`; MQTT/UNS → `sparkplug-tap`; cross-protocol triage →
  `industrial-diagnostics`. IT/network/Kubernetes/hypervisor/backup → not this tool.

## Read tools

| Tool | Params | Returns |
|------|--------|---------|
| `mc_cpu_status` | `endpoint?` | `{cpu_type, cpu_code, plctype}` |
| `mc_read_words` | `headdevice (e.g. "D100"), endpoint?, count=1` | `{words:[int,...]}` |
| `mc_read_bits` | `headdevice (e.g. "M0"), endpoint?, count=1` | `{bits:[bool,...]}` |
| `mc_read_many` | `endpoint?, word_devices[]?, dword_devices[]?` | `{words:[{device,value}], dwords:[...]}` |

Example: `mc_read_words(headdevice="D100", count=8)` →
`{"headdevice":"D100","count":8,"words":[10,20,30, ...]}`

## Write tool (HIGH risk · MOC · off by default)

`mc_write_words(headdevice, values[], endpoint?, dry_run=true)`
- **OT-DANGEROUS. 未经授权勿对生产控制系统写入.** Defaults to `dry_run=true`.
  Captures BEFORE values (read-back of the range) and records an undo descriptor.
- Apply: `dry_run=false` + `OPCUA_AUDIT_APPROVED_BY`. CLI:
  `ot-aiops mc write-words D100 1 2 3 --apply` (double-confirm prompt).
- Dry-run → `{dry_run:true, before, would_write, note}`; applied →
  `{applied:true, before, written, _undo_id}`.

## Setup
`ot-aiops init` (mc: host/port/plctype) · `ot-aiops doctor` · `ot-aiops mcp`.
plctype ∈ Q | L | QnA | iQ-R | iQ-L. 缺功能提 issue/PR 欢迎留言.
