---
name: iaiops-energy
description: >-
  Vendor-neutral, governed, READ-ONLY energy/substation telecontrol data tap —
  the energy edition (变电/电力) of Industrial-AIOps. Monitor-direction telemetry
  over IEC 60870-5-104 (IEC-104: RTU link status, general interrogation, single
  monitored-point reads by IOA — 遥测/遥信), DNP3 / IEEE 1815 (outstation link
  status, Class 0/1/2/3 integrity poll), and IEC 61850 MMS (IED logical-device
  directory, model browse, data-attribute reads) — plus the base cross-protocol
  brain (dataflow diagnosis, alarm bad-actors, data-quality scorecards, OEE,
  asset inventory, compliance self-assessment) mounted on the same server. Use
  when the task names IEC 60870-5-104 / IEC-104 / 104规约, DNP3 / IEEE 1815 /
  outstation, IEC 61850 / MMS / IED / GOOSE (GOOSE and Sampled Values are NOT
  supported — MMS reads only), a substation / 变电站 / RTU / SCADA gateway /
  telecontrol front-end, energy / power / utility SCADA telemetry, or 遥测遥信 /
  电力监控. Routes to the iaiops-energy MCP server. Monitor-only by design: no
  control/operate (CROB, setpoints, select-before-operate, IEC-104 command
  ASDUs) is exposed. Do NOT use for factory/building/process protocols (OPC-UA,
  Modbus, S7, BACnet, MQTT …) — those live in the base iaiops server — nor for
  IT/network gear, Kubernetes, hypervisors, or backups.
---

# iaiops-energy — substation / utility telecontrol data tap (变电 / 电力)

The **energy edition** of Industrial-AIOps as one governed MCP server: read-only
connectors for the three utility telecontrol protocols — **IEC 60870-5-104**,
**DNP3 / IEEE 1815**, **IEC 61850 MMS** — built on the base `iaiops` core, plus the
base cross-protocol **brain** mounted onto the same server. Every tool runs
through the iaiops governance harness (audit / budget / risk-tier); startup
refuses to serve any tool missing the `_is_governed_tool` marker.

**Monitor-direction ONLY — deliberately.** No control/operate surface exists in
this edition: no DNP3 CROB or analog-output, no setpoints, no
select-before-operate, no IEC-104 command ASDUs (C_SC / C_DC / C_SE), no
IEC 61850 control model. This is not a gated write — the tools simply do not
exist, so an agent cannot be talked into operating a breaker.
未经授权勿对生产控制系统写入。

## When to route here

Task mentions: IEC 60870-5-104 / IEC-104 / 104规约 / general interrogation /
总召 / IOA, DNP3 / IEEE 1815 / outstation / integrity poll / Class 0/1/2/3,
IEC 61850 / MMS / IED / logical device / logical node / data attribute /
functional constraint, substation / 变电站 / RTU / telecontrol / SCADA gateway,
energy / power / utility telemetry, 遥测 / 遥信 / 电力监控.

**Explicitly out of scope:** IEC 61850 **GOOSE** and **Sampled Values** (layer-2
pub/sub — not supported; MMS client reads only), protection-relay settings
changes, any control/operate action.

**Factory / building / process protocols route elsewhere:** OPC-UA, Modbus,
Siemens S7, Mitsubishi MC, MTConnect, MQTT/Sparkplug B, EtherNet/IP, EtherCAT,
SECS/GEM, PROFINET, HART-IP, BACnet → use the base **iaiops** server
(`pip install iaiops`, then `iaiops-mcp`), not this one.

## Install & run

```bash
pip install 'iaiops-energy[energy]'      # all three protocols
pip install 'iaiops-energy[iec104]'      # or per-protocol extras:
pip install 'iaiops-energy[dnp3]'        #   [iec104] / [dnp3] / [iec61850]
iaiops-energy-mcp                        # brain + energy tools over stdio
```

`iaiops-energy` pulls in the base `iaiops` package (shared core) automatically.
Protocol client libs are lazy optional extras — a missing lib degrades to a
teaching error naming the exact `pip install`, not a crash. Targets live in
`~/.iaiops/config.yaml` (override path via `IAIOPS_CONFIG`):
`protocol: iec104|dnp3|iec61850`, `host`, `port`, plus `common_address` /
`unit_id` as the protocol needs. Credentials go to the encrypted secret store,
unlocked via `IAIOPS_MASTER_PASSWORD` — never into config or chat.

MCP client config (stdio):

```json
{
  "mcpServers": {
    "iaiops-energy": {
      "command": "iaiops-energy-mcp",
      "env": {
        "IAIOPS_CONFIG": "/etc/iaiops/config.yaml",
        "IAIOPS_MASTER_PASSWORD": "<from your secret manager>"
      }
    }
  }
}
```

Every tool takes an optional `endpoint` selecting a named target from that
config; omitted, the sole/default target of the protocol is used.

## Tools by protocol (all `[READ][risk=low]`)

### IEC 60870-5-104 (c104; RTU / substation telemetry — 遥测遥信)
- `iec104_connection_info` — connect and report link status + discovered
  stations (common addresses) — the IEC-104 doctor step
- `iec104_interrogate` — general interrogation (总召): all monitored points of
  one station by ASDU common address, with type / quality / timestamp
- `iec104_read_point` — read ONE monitored point by information-object
  address (IOA)

### DNP3 / IEEE 1815 (pydnp3; outstation monitoring)
- `dnp3_link_status` — bring the DNP3 master online and report link /
  outstation status — the DNP3 doctor step
- `dnp3_integrity_poll` — Class 0/1/2/3 integrity poll: the outstation's
  database grouped by measurement type (binary / analog / counter …)

### IEC 61850 MMS (pyiec61850; substation IED reads — linux-only wheel)
- `iec61850_device_directory` — list the IED's logical devices (optionally
  their logical-node children) — the IEC 61850 doctor step
- `iec61850_browse` — browse immediate model children under a reference
  (LD / LN / DO)
- `iec61850_read` — read one data attribute by object reference + functional
  constraint (e.g. `LD0/MMXU1.TotW.mag.f`, FC `MX`)

### Substation intelligence (pure analysis — no live I/O)
- `substation_event_analysis` — Sequence-of-Events (SOE) protection-trip /
  selectivity analysis: feed injected relay pickups/trips + breaker open/close +
  lockouts (`{ref, timestamp, type}`) and it decides what tripped and whether
  protection coordinated — selective trip vs non-selective backup operation vs
  breaker failure, cite-first, monitor-only（变电事件序列/保护选择性分析：判定
  跳闸与保护配合是否正确——选择性跳闸/后备越级动作/断路器失灵；纯分析、只读，
  不做任何 live I/O）

### Cross-protocol brain (mounted from the base `iaiops` package)
The base brain tools register onto this server too — diagnostics
(`diagnose_dataflow`, `alarm_bad_actors`, `tag_health`, `historian_health`,
`data_quality_scorecard`, downtime root-cause), analytics (OEE / downtime,
`monitor_changes`), asset inventory + unified asset model / alias governance,
and compliance self-assessment (防护指南 / 等保 2.0 / IEC 62443) — plus
`protocols_supported` for the capability map. Same governance harness; see the
base `iaiops` skill for the full brain reference.

## Supported versions (honest matrix)

| Protocol | Lib pin (this release) | Spec / transport | Verification status | CI |
| --- | --- | --- | --- | --- |
| IEC 60870-5-104 | `c104>=2.0,<3` | IEC 60870-5-104 over TCP/2404 | **verified (monitor path)** — real client↔server round-trip vs an in-process `c104` server (`tests/test_iec104_live.py`, passes in a Linux container): general interrogation returns seeded points, bad IOA → no fabricated value, no control ASDU issued; skips on macOS (no `c104` wheel). Live RTU 待核实 | ✅ runs every push |
| DNP3 / IEEE 1815 | `pydnp3>=0.1,<1` | IEEE 1815, TCP; monitor direction only | **verified (monitor path)** — real master↔outstation round-trip vs a live opendnp3 outstation; physical RTU 待核实 | ✅ runs every push ¹ |
| IEC 61850 MMS | `pyiec61850>=1.5.2a1,<2` (linux-only wheel) | MMS over ISO-on-TCP/102; no GOOSE/SV | **verified (monitor path)** — real client↔server round-trip vs an in-process libiec61850 MMS server; physical IED 待核实 | ✅ runs every push |

**¹ All three monitor paths are CI-gated (since 0.1.11)**, and a skipped live test now
**fails** the build — a skip and a pass look identical in a green badge, which is how the
DNP3 gap survived. This block used to say DNP3 and IEC-61850 were not covered by CI.
IEC-61850 had in fact been running there for some time and nobody rechecked; DNP3 was
believed unbuildable on hosted runners, which was wrong — opendnp3 compiles clean and the
2019 binding layer needed three mechanical fixes, scripted in `scripts/build_pydnp3.sh`.

`pydnp3` ships no wheel (opendnp3 is built from source by that script);
`pyiec61850` is a linux-only SWIG wheel — both protocols no-op with a teaching
error elsewhere. **CI coverage is level ② (real library, loopback), never level ③.**
Anything not yet proven against real gear stays marked 待核实 — do not claim otherwise.

## Doctor-first workflow

1. `protocols_supported` — see what this server exposes and what's configured.
2. Prove the link with the protocol's cheap status tool **before** any deep
   read: `iec104_connection_info` / `dnp3_link_status` /
   `iec61850_device_directory`.
3. Only then interrogate: `iec104_interrogate` / `dnp3_integrity_poll` /
   `iec61850_browse` → targeted reads (`iec104_read_point` / `iec61850_read`).
4. Feed results to the brain (e.g. `diagnose_dataflow` for "no data",
   `data_quality_scorecard` for fleet trust, `alarm_bad_actors` for floods).

## Safety

Read-only edition: zero write/control tools, so there is nothing to gate — the
strongest guarantee available. All tools are `risk=low`, audited, and
budget-tracked; errors return the canonical `{error, hint}` shape. Never point
this at production telecontrol gear without authorization; interrogations and
integrity polls do generate real traffic on the operational link. No tool
returns secrets.

Every MCP call is audited with `origin=mcp` and the client's self-reported name
(since 0.2.0). This server shares the base package's audit chain: if it runs
beside `iaiops-mcp` / the CLI on one `IAIOPS_HOME`, every process there must be
on `iaiops>=0.29` — an older one verifying the shared trail reports
`row_hash mismatch` on the newer rows. The server speaks **stdio only**; it has
no HTTP listener, so `IAIOPS_MCP_TOKEN` does not apply to it.
