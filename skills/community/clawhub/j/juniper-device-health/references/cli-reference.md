# Juniper JunOS CLI Reference

Commands organized by subsystem. All commands are read-only (show/request display
only). Validated against JunOS 23.2+.

## RE and Mastership

| Subsystem | Command | Key Output |
|-----------|---------|------------|
| RE status | `show chassis routing-engine` | CPU, memory, temp, mastership state per RE |
| Mastership detail | `show chassis routing-engine | match "Slot\|Current state\|Mastership"` | Concise mastership check |
| RE switchover history | `show chassis routing-engine mastership` | Mastership change events |
| Switch to master | `request routing-engine login other-routing-engine` | Login to peer RE |
| RE uptime/reboot | `show system uptime` | Boot time, uptime, last config change |
| Reboot reason | `show system boot-messages | match "reason"` | Last reboot cause |

### RE Notes

- `show chassis routing-engine` is the primary RE health command — CPU, memory,
  temperature, and mastership state in one output.
- CPU is reported as idle percentage. Invert for utilization: `100 - idle = used`.
- Load averages follow Unix convention: 1min/5min/15min. Values above 1.0 per core
  indicate sustained load. Most MX/SRX/EX REs have 2–4 cores.
- On dual-RE systems, this command shows both REs. Only the master RE's data
  reflects active forwarding state.

## PFE and FPC

| Subsystem | Command | Key Output |
|-----------|---------|------------|
| FPC summary | `show chassis fpc` | State, CPU, memory per FPC slot |
| FPC detail | `show chassis fpc detail` | Extended per-FPC stats including uptime |
| PFE traffic stats | `show pfe statistics traffic` | Input/output/discard counters per PFE |
| PFE error stats | `show pfe statistics error` | Error counters by category |
| FPC PIC status | `show chassis fpc pic-status` | Per-PIC state within each FPC |
| Hardware detail | `show chassis hardware` | Installed FRUs, serial numbers |

### PFE Notes

- FPC `State` must be `Online`. Other states: `Present` (powered but not booted),
  `Offline` (administratively or fault), `Empty` (no FPC in slot).
- PFE CPU is separate from RE CPU. An FPC with 90% CPU indicates data plane
  saturation on that linecard, not a control plane problem.
- `show pfe statistics traffic` — compare input vs output. The delta is drops.
  Check `fabric input drops` (linecard-to-fabric path) vs `local input drops`
  (punt/exception path) to classify the drop source.
- On MX-series with multiple FPCs, each FPC has independent PFE resources.
  One degraded FPC does not affect others.

## Alarms

| Subsystem | Command | Key Output |
|-----------|---------|------------|
| Chassis alarms | `show chassis alarms` | Active chassis-level alarms with severity |
| System alarms | `show system alarms` | Active system-level alarms (licenses, config) |
| Alarm detail | `show chassis alarm-information` | Extended alarm data |
| Alarm history | `show log messages \| match "ALARM\|alarm"` | Historical alarm events |

### Alarm Notes

- Chassis alarms: hardware-sourced (FPC, PSU, fan, temperature, FRU).
- System alarms: software-sourced (license expiry, rescue config, autorecovery).
- Severity levels: Major (red — service-affecting), Minor (yellow — degraded).
- A "No alarms currently active" message is the healthy state.
- Common minor alarm: "Rescue configuration is not set" — not service-affecting
  but should be resolved with `request system configuration rescue save`.

## System Resources

| Subsystem | Command | Key Output |
|-----------|---------|------------|
| Processes | `show system processes extensive` | Per-process CPU and memory |
| Top processes | `show system processes extensive \| match "PID\|last pid\|%CPU" \| head 20` | Quick CPU consumers list |
| Storage | `show system storage` | Per-partition usage |
| Kernel memory | `show system memory` | Kernel-level memory allocation |
| Core dumps | `show system core-dumps` | Process crash dump files |
| Commit history | `show system commit` | Recent commit log with timestamps |
| Config rollback | `show system rollback compare [n] [m]` | Diff between config versions |
| Task replication | `show task replication` | RE sync state (dual-RE only) |

### System Notes

- `show system processes extensive` is the JunOS equivalent of `top`. Filter to
  CPU-heavy processes. Key daemons: `rpd` (routing), `chassisd` (chassis),
  `snmpd` (SNMP), `mgd` (management), `kmd` (key management/IPsec).
- Storage: `/var` partition is most critical — it holds logs, core dumps, and
  temporary files. Full `/var` prevents commits and syslog.
- Core dumps: presence of files less than 7 days old warrants investigation.
  The process name in the filename identifies what crashed.

## Interfaces

| Subsystem | Command | Key Output |
|-----------|---------|------------|
| Interface summary | `show interfaces terse` | One-line state per interface |
| Error filter | `show interfaces terse \| match "down\|err"` | Down and error interfaces |
| Interface detail | `show interfaces extensive [name]` | Full counters and statistics |
| Error counters | `show interfaces extensive [name] \| match "error\|drop\|CRC\|carrier"` | Error fields only |
| Optics DOM | `show interfaces diagnostics optics [name]` | Tx/Rx power, temp, voltage |
| AE/LAG state | `show lacp interfaces` | LACP member state |
| IP brief | `show interfaces terse routing` | Interfaces with IP addresses |

### Interface Notes

- JunOS names interfaces as `type-fpc/pic/port` (e.g., `ge-0/0/0`, `xe-1/0/3`).
- `show interfaces extensive` provides full counters including error detail.
  Use `match` to filter — the full output for a single interface is extensive.
- Optics DOM: `show interfaces diagnostics optics` provides Tx/Rx power in dBm,
  laser bias current, temperature. Low Rx power is the most common L1 indicator.
- Carrier transitions: high count indicates link flap. Correlate with optics DOM.

## Routing

| Subsystem | Command | Key Output |
|-----------|---------|------------|
| Route summary | `show route summary` | Per-protocol route counts and Router ID |
| BGP summary | `show bgp summary` | Neighbor state, prefix count, uptime |
| BGP neighbor detail | `show bgp neighbor [addr]` | Session state, timers, messages |
| OSPF neighbors | `show ospf neighbor` | Neighbor ID, state, priority, dead time |
| ISIS adjacencies | `show isis adjacency` | System ID, state, interface, level |
| Route table size | `show route summary \| match "total"` | Total routes across all tables |

### Routing Notes

- BGP: `show bgp summary` — State column shows "Establ" when healthy. Any other
  text (Active, Connect, Idle) means the session is not established.
- OSPF: only `Full` state is healthy (except `2-Way` for non-DR on broadcast).
- ISIS: `Up` is the healthy state.
- Route table deviation > 10% from baseline warrants investigation.
- On SRX: check security zones routing instances separately if multi-VR is in use.

## Environment

| Subsystem | Command | Key Output |
|-----------|---------|------------|
| Environment summary | `show chassis environment` | Temp, fans, power per component |
| Temperature detail | `show chassis temperature-thresholds` | Per-sensor thresholds |
| Power detail | `show chassis power` | PSU status, wattage, redundancy |
| Fan detail | `show chassis fan` | Per-fan RPM and status |
| LED status | `show chassis led` | Front panel LED indicators |
| FRU inventory | `show chassis hardware` | Installed hardware with serial numbers |

### Environment Notes

- Temperature thresholds vary by platform and sensor location. Use
  `show chassis temperature-thresholds` for exact values rather than assuming.
- Power: `show chassis power` reports per-PSU status and total capacity.
  If total load exceeds remaining capacity after a PSU failure, the system
  may shed FPCs — check `show chassis power budget` on supported platforms.
- Fans: failed fans trigger Major chassis alarm. Even a single fan failure
  reduces cooling capacity and should be addressed promptly.
