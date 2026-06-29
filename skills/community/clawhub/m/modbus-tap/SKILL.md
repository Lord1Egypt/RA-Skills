---
name: modbus-tap
description: >-
  Read Modbus-TCP PLCs — holding/input registers (FC03/FC04) and coils/discrete
  inputs (FC01/FC02) with decode hints (uint16/int16/uint32/int32/float32), plus
  a warn/alarm threshold health summary. Covers many domestic 国产 controllers
  (汇川/信捷/和利时/台达) and any vendor speaking Modbus-TCP. Use when the task
  names Modbus, a register/coil address, or unit/slave id. Routes to the ot-aiops
  MCP server. Read-only. For OPC-UA/S7/Mitsubishi/MTConnect/MQTT use the sibling
  *-tap skills; not for IT/network gear, Kubernetes, hypervisors, or backups.
---

# modbus-tap

Read-only Modbus-TCP telemetry via the **ot-aiops** MCP server. Preview —
validated against a mocked pymodbus client, NOT live PLCs.

## When to use
- A PLC speaking Modbus-TCP (`host:502`, `unit_id`), incl. domestic 国产 PLCs.
- Read registers/coils; classify registers against thresholds.

## When NOT to use (routing)
- OPC-UA → `opcua-tap`; Siemens S7 → `s7-tap`; Mitsubishi → `mc-tap`; CNC →
  `mtconnect-tap`; MQTT/UNS → `sparkplug-tap`; cross-protocol triage →
  `industrial-diagnostics`.
- IT/network devices, Kubernetes, hypervisors, backups → not this tool.

## Tools

| Tool | Params | Returns |
|------|--------|---------|
| `modbus_read_holding` | `address, endpoint?, count=1, decode="uint16"` | `{raw_registers, decoded[...]}` |
| `modbus_read_input` | `address, endpoint?, count=1, decode="uint16"` | `{raw_registers, decoded[...]}` |
| `modbus_read_coils` | `address, endpoint?, count=1` | `{bits[bool,...]}` |
| `modbus_read_discrete` | `address, endpoint?, count=1` | `{bits[bool,...]}` |
| `modbus_health_summary` | `endpoint?, addresses[]?, thresholds?, register_type="holding"` | `{overall, counts, offenders[...]}` |

Registers are untyped 16-bit words; pick `decode`. Word order is big-endian.

## Example
`modbus_read_holding(address=0, endpoint="plc2", count=2, decode="float32")`
→ `{"address":0,"count":2,"decode":"float32","decoded":[20.0]}`

## Setup
`ot-aiops init` (add a modbus endpoint) · `ot-aiops doctor` · `ot-aiops mcp`.

## Safety
Read-only (FC05/06/15/16 writes are NOT implemented). Device text sanitized;
secrets never returned. 缺功能提 issue/PR 欢迎留言.
