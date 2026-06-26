# IS-IS CLI Reference — Cisco / JunOS / EOS

Commands organized by diagnostic category with all three vendors side by side.
All commands are read-only (show/display only). Cisco commands validated against
IOS-XE 17.3+ and NX-OS 10.2+; JunOS 21.x+; EOS 4.28+.

## Instance and Process

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| IS-IS overview | `show isis protocol` | `show isis overview` | `show isis summary` |
| NET address | `show isis protocol \| include NET` | `show isis overview \| match "NET"` | `show isis summary \| include NET` |
| System ID | `show isis protocol \| include System` | `show isis overview \| match "System"` | `show isis summary \| include System` |
| Level configuration | `show isis protocol \| include Level` | `show isis overview \| match "Level"` | `show isis summary \| include Level` |
| Process status | `show isis protocol` | `show isis overview` | `show isis summary` |
| Hostname mapping | `show isis hostname` | `show isis hostname` | `show isis hostname` |
| IS-IS counters | `show isis statistics` | `show isis statistics` | `show isis counters` |

### Instance Notes

- **Cisco:** Uses `show isis` (not `show clns` for most modern diagnostics). Legacy `show clns` commands still work but `show isis` provides more structured output. IS-IS instance is identified by a tag (e.g., `router isis CORE`).
- **JunOS:** IS-IS configuration lives under `protocols isis`. The `show isis overview` command provides a comprehensive summary including NET, system ID, levels, and global settings.
- **EOS:** Uses `show isis summary` for the overview (not `show isis protocol`). Interface-level IS-IS configuration can be applied under the interface or under the IS-IS instance.
- **Cisco `show clns` vs `show isis`:** `show clns neighbors` shows CLNS-level adjacencies (includes ES-IS and manual entries). `show isis neighbors` shows IS-IS adjacencies only — prefer `show isis` for IS-IS diagnostics.

## Adjacency

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Neighbor summary | `show isis neighbors` | `show isis adjacency` | `show isis neighbors` |
| Neighbor detail | `show isis neighbors detail` | `show isis adjacency detail` | `show isis neighbors detail` |
| Specific neighbor | `show isis neighbors [intf]` | `show isis adjacency [intf]` | `show isis neighbors [intf]` |
| Adjacency state | `show isis neighbors \| include [sysid]` | `show isis adjacency \| match [sysid]` | `show isis neighbors \| include [sysid]` |
| DIS on segment | `show isis interface [intf] \| include DIS` | `show isis interface [intf] \| match "DIS"` | `show isis interface [intf] \| include DIS` |
| Adjacency count | `show isis neighbors \| count UP` | `show isis adjacency \| count Up` | `show isis neighbors \| count UP` |
| Adjacency events | `show isis adjacency-log` | `show isis log` | `show isis adjacency-log` |

### Adjacency Notes

- **States:** IS-IS adjacency has three states: Down, Initializing (Init), Up. This is simpler than OSPF's seven-state FSM. On P2P links, adjacency transitions directly Down→Init→Up. On broadcast links, DIS election occurs after adjacency forms.
- **Cisco:** `show isis neighbors detail` shows hold time, SNPA (MAC address), circuit ID, area addresses, and IP addresses. The circuit ID is critical for identifying which pseudonode LSP corresponds to which segment.
- **JunOS:** Uses `show isis adjacency` (not `show isis neighbors`). Detail output includes hold timer, priority, topology, and level. Adjacency events are logged in `show isis log`.
- **EOS:** Neighbor output format matches Cisco. `show isis neighbors detail` adds adjacency uptime, topology type, and BFD status if configured. DIS role is shown per interface per level.

## LSPDB

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Database summary | `show isis database` | `show isis database` | `show isis database` |
| Database detail | `show isis database detail` | `show isis database extensive` | `show isis database detail` |
| L1 database | `show isis database level-1` | `show isis database level 1` | `show isis database level-1` |
| L2 database | `show isis database level-2` | `show isis database level 2` | `show isis database level-2` |
| Specific LSP | `show isis database detail [lspid]` | `show isis database [lspid] extensive` | `show isis database detail [lspid]` |
| Self-originated | `show isis database detail \| include local` | `show isis database \| match "self"` | `show isis database detail \| include local` |
| LSP count | `show isis database \| count LSP` | `show isis database \| count` | `show isis database \| count LSP` |
| Overload bit | `show isis database detail \| include OL` | `show isis database extensive \| match "Overload"` | `show isis database detail \| include OL` |
| LSP lifetime | `show isis database detail \| include Lifetime` | `show isis database extensive \| match "Remaining"` | `show isis database detail \| include Lifetime` |

### LSPDB Notes

- **LSP naming:** LSPs are identified as `systemID.pseudonodeID-fragmentNumber` (e.g., `1921.6800.1001.00-00`). Fragment `00` is the first fragment. Pseudonode ID `00` is the router itself; non-zero pseudonode IDs are generated by the DIS for broadcast segments.
- **Lifetime:** Default max is 1200 seconds (20 minutes). Routers refresh their own LSPs at 900 seconds (15 minutes) by default. An LSP with lifetime near 0 that is not refreshed will be purged — the router that originated it is likely down.
- **Cisco:** `show isis database detail` shows TLVs including IP reachability (narrow and/or wide), IS reachability, hostname, and authentication. Use `level-1` or `level-2` to filter by level.
- **JunOS:** Uses `extensive` instead of `detail`. Output includes all TLVs, sequence number, checksum, and remaining lifetime. The `show isis database` without `extensive` gives a summary with LSP ID, sequence, checksum, lifetime, and attributes.
- **EOS:** Database output matches Cisco format. `show isis database detail` includes full TLV decode with metric style (narrow/wide) visible in the IP reachability TLVs.
- **LSPDB consistency check:** All routers in the same level should have identical LSP sets. Compare `show isis database` output across neighbors — any LSP present on one but absent on another indicates a flooding failure.

## Interface

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Interface summary | `show isis interface brief` | `show isis interface` | `show isis interface brief` |
| Interface detail | `show isis interface [intf]` | `show isis interface [intf] detail` | `show isis interface [intf]` |
| Interface metric | `show isis interface [intf] \| include Metric` | `show isis interface [intf] \| match "Metric"` | `show isis interface [intf] \| include Metric` |
| Hello interval | `show isis interface [intf] \| include Hello` | `show isis interface [intf] \| match "Hello"` | `show isis interface [intf] \| include Hello` |
| Circuit type | `show isis interface [intf] \| include Circuit` | `show isis interface [intf] \| match "Circuit"` | `show isis interface [intf] \| include Circuit` |
| Authentication | `show isis interface [intf] \| include Auth` | `show isis interface [intf] \| match "Auth"` | `show isis interface [intf] \| include Auth` |
| BFD status | `show isis interface [intf] \| include BFD` | `show isis interface [intf] \| match "BFD"` | `show isis interface [intf] \| include BFD` |

### Interface Notes

- **Cisco:** `show isis interface brief` gives a compact table of all IS-IS interfaces with circuit type, level, metric, and state. Full detail adds hello/hold timers, authentication, priority, DIS status, and adjacency count.
- **JunOS:** Interface level enablement is configured per interface under `protocols isis interface [intf]`. Default is L1/L2 on all interfaces. Use `level 1 disable` or `level 2 disable` to restrict.
- **EOS:** Supports both passive and active interfaces. Passive interfaces are advertised in LSPs but do not form adjacencies. `show isis interface brief` output matches Cisco format with circuit type and metric per level.

## Route and Topology

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| IS-IS routes | `show isis rib` | `show isis route` | `show isis route` |
| L1 routes | `show isis rib \| include L1` | `show isis route \| match "L1"` | `show isis route \| include L1` |
| L2 routes | `show isis rib \| include L2` | `show isis route \| match "L2"` | `show isis route \| include L2` |
| IS-IS in RIB | `show ip route isis` | `show route protocol isis` | `show ip route isis` |
| Route detail | `show isis rib [prefix]` | `show isis route [prefix] detail` | `show isis route [prefix]` |
| Topology | `show isis topology` | `show isis spf topology` | `show isis topology` |
| SPF log | `show isis spf-log` | `show isis spf log` | `show isis spf-log` |
| SPF statistics | `show isis spf-log \| include SPF` | `show isis spf log \| match "Duration"` | `show isis spf-log \| include SPF` |
| Route leaking | `show isis rib \| include leak` | `show isis route \| match "leak"` | `show isis route \| include leak` |

### Route and Topology Notes

- **Cisco:** `show isis rib` shows the IS-IS RIB (routes computed by SPF before installation into the global RIB). `show ip route isis` shows IS-IS routes that were installed into the IP routing table. Compare both to detect routes computed but not installed (e.g., better route via another protocol).
- **JunOS:** `show isis route` shows computed IS-IS routes. `show route protocol isis` shows installed routes. `show isis spf topology` gives the SPF tree from this router's perspective — useful for verifying the shortest path computation.
- **EOS:** Route output closely matches JunOS style. `show isis topology` provides the SPF tree. `show isis spf-log` shows timestamps and trigger events for each SPF run — critical for convergence analysis.
- **Route leaking:** L2→L1 route leaking is vendor-specific in configuration but the result is visible in the IS-IS RIB as L2 routes injected into the L1 domain. Not all vendors label leaked routes identically — check vendor documentation for output format.
