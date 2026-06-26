# OSPF CLI Reference — Cisco / JunOS / EOS

Commands organized by diagnostic category with all three vendors side by side.
All commands are read-only (show/display only). Cisco commands validated against
IOS-XE 17.3+ and NX-OS 10.2+; JunOS 21.x+; EOS 4.28+.

## Interface and Instance

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| OSPF process overview | `show ip ospf` | `show ospf overview` | `show ip ospf` |
| Interface summary | `show ip ospf interface brief` | `show ospf interface` | `show ip ospf interface brief` |
| Interface detail | `show ip ospf interface [intf]` | `show ospf interface [intf] detail` | `show ip ospf interface [intf]` |
| OSPF-enabled interfaces | `show ip ospf interface brief` (list) | `show ospf interface` (list) | `show ip ospf interface brief` (list) |
| Interface cost | `show ip ospf interface [intf] \| include Cost` | `show ospf interface [intf] \| match "Cost"` | `show ip ospf interface [intf] \| include Cost` |
| Network type | `show ip ospf interface [intf] \| include Network` | `show ospf interface [intf] \| match "Type"` | `show ip ospf interface [intf] \| include Network` |
| Router ID | `show ip ospf \| include Router` | `show ospf overview \| match "Router"` | `show ip ospf \| include Router` |
| Process ID | `show ip ospf \| include Process` | `show ospf overview` (instance name) | `show ip ospf \| include Process` |

### Interface Notes

- **Cisco:** `show ip ospf interface brief` provides a compact view of all OSPF interfaces with area, cost, state, and neighbor count. The full `show ip ospf interface [intf]` adds hello/dead timers, authentication, and DR/BDR status.
- **JunOS:** Uses instance names instead of process IDs. `show ospf interface` shows area, state, and neighbor count. OSPF interfaces are configured under `protocols ospf area [id] interface [intf]`.
- **EOS:** Output closely matches Cisco IOS-XE. Interface configuration uses `ip ospf area [id]` directly on the interface (preferred) or `network` statements under the OSPF process.

## Neighbor and Adjacency

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Neighbor summary | `show ip ospf neighbor` | `show ospf neighbor` | `show ip ospf neighbor` |
| Neighbor detail | `show ip ospf neighbor detail` | `show ospf neighbor detail` | `show ip ospf neighbor detail` |
| Specific neighbor | `show ip ospf neighbor [addr]` | `show ospf neighbor [addr] detail` | `show ip ospf neighbor [addr]` |
| Neighbor state | `show ip ospf neighbor \| include [addr]` | `show ospf neighbor \| match [addr]` | `show ip ospf neighbor \| include [addr]` |
| DR/BDR on segment | `show ip ospf interface [intf] \| include DR` | `show ospf interface [intf] \| match "DR"` | `show ip ospf interface [intf] \| include DR` |
| Neighbor count | `show ip ospf neighbor \| count Full` | `show ospf neighbor \| count Full` | `show ip ospf neighbor \| include Full \| wc -l` |
| Adjacency events | `show ip ospf events \| include ADJ` | `show ospf log` | `show ip ospf neighbor detail \| include state` |

### Neighbor Notes

- **FSM states** in output: Down, Attempt (NBMA), Init, 2-Way, ExStart, Exchange, Loading, Full. Only Full indicates a completed adjacency (except DROther↔DROther which stops at 2-Way on broadcast/NBMA).
- **Cisco:** `show ip ospf neighbor detail` shows DR/BDR addresses, dead timer countdown, retransmit counts, and database summary list. Retransmit count >0 indicates DBD exchange is stalled.
- **JunOS:** `show ospf neighbor detail` includes adjacency options negotiated, area ID, and interface. Neighbor state transitions are logged in `show ospf log`.
- **EOS:** Neighbor output format matches Cisco. `show ip ospf neighbor detail` adds retransmit and request list sizes — non-zero values during steady state indicate sync problems.

## LSDB

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Database summary | `show ip ospf database database-summary` | `show ospf database summary` | `show ip ospf database database-summary` |
| All LSAs | `show ip ospf database` | `show ospf database` | `show ip ospf database` |
| Router LSAs (Type 1) | `show ip ospf database router` | `show ospf database router` | `show ip ospf database router` |
| Network LSAs (Type 2) | `show ip ospf database network` | `show ospf database network` | `show ip ospf database network` |
| Summary LSAs (Type 3) | `show ip ospf database summary` | `show ospf database netsummary` | `show ip ospf database summary` |
| ASBR Summary (Type 4) | `show ip ospf database asbr-summary` | `show ospf database asbrsummary` | `show ip ospf database asbr-summary` |
| External LSAs (Type 5) | `show ip ospf database external` | `show ospf database external` | `show ip ospf database external` |
| NSSA External (Type 7) | `show ip ospf database nssa-external` | `show ospf database nssa` | `show ip ospf database nssa-external` |
| Specific LSA detail | `show ip ospf database router [id] detail` | `show ospf database router lsa-id [id] detail` | `show ip ospf database router [id] detail` |
| LSA by area | `show ip ospf database router area [id]` | `show ospf database area [id]` | `show ip ospf database router area [id]` |
| Self-originated LSAs | `show ip ospf database self-originate` | `show ospf database self` | `show ip ospf database self-originate` |
| MaxAge LSAs | `show ip ospf database \| include MaxAge` | `show ospf database \| match "3600"` | `show ip ospf database \| include MaxAge` |

### LSDB Notes

- **LSA Age:** Ranges from 0 to 3600 seconds (MaxAge). Originating routers refresh their LSAs every 1800 seconds (LSRefreshTime). An LSA at MaxAge is being flushed from the LSDB. Excessive MaxAge LSAs indicate a router has gone down without gracefully withdrawing its LSAs.
- **JunOS:** Uses different names for some LSA queries: `netsummary` for Type 3 (not `summary` which would be ambiguous), `asbrsummary` for Type 4, and `nssa` for Type 7.
- **Cisco/EOS:** `database-summary` gives a per-area count of each LSA type — the fastest way to assess LSDB size. Compare counts across routers in the same area — they should match exactly (LSDB synchronization invariant).
- **LSA correlation:** The number of Type 1 LSAs in an area should equal the number of OSPF routers in that area. Type 2 LSAs should equal the number of broadcast/NBMA segments with a DR. Mismatches indicate stale LSAs or synchronization issues.

## SPF and Routes

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| SPF statistics | `show ip ospf \| include SPF` | `show ospf statistics` | `show ip ospf \| include SPF` |
| SPF log | `show ip ospf statistics detail` | `show ospf log \| match spf` | `show ip ospf statistics detail` |
| OSPF routes in RIB | `show ip route ospf` | `show route protocol ospf` | `show ip route ospf` |
| OSPF route detail | `show ip route [prefix] \| include OSPF` | `show route [prefix] detail` | `show ip route [prefix] \| include OSPF` |
| Inter-area routes | `show ip route ospf \| include IA` | `show route protocol ospf \| match "Inter"` | `show ip route ospf \| include IA` |
| External routes | `show ip route ospf \| include E1\|E2` | `show route protocol ospf \| match "Ext"` | `show ip route ospf \| include E1\|E2` |
| Route count | `show ip route ospf \| count /` | `show route protocol ospf \| count` | `show ip route ospf \| count /` |
| SPF throttle timers | `show ip ospf \| include throttle` | `show ospf overview \| match "SPF"` | `show ip ospf \| include throttle` |

### SPF Notes

- **SPF throttle:** Cisco and EOS use three timers: initial-delay (ms before first SPF after trigger), secondary-delay (ms between second and subsequent runs), max-hold (maximum interval between runs during sustained instability). JunOS uses `spf-delay` and `spf-holddown` with similar semantics.
- **Route types:** O = intra-area, O IA = inter-area (via ABR), O E1 = external with cumulative metric, O E2 = external with fixed metric (default for redistribution). JunOS labels differ: OSPF internal, OSPF AS external.
- **Convergence measurement:** Compare SPF run timestamps with the triggering event (link down, config change) to measure convergence time. Sub-second convergence requires tuned SPF timers and fast hello (BFD preferred for fast failure detection).

## Area Configuration

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Area summary | `show ip ospf \| section Area` | `show ospf overview` | `show ip ospf \| section Area` |
| Area type | `show ip ospf \| include Area\|stub\|NSSA` | `show ospf overview \| match "Area\|Stub\|NSSA"` | `show ip ospf \| include Area\|stub\|NSSA` |
| Virtual links | `show ip ospf virtual-links` | `show ospf virtual-link` | `show ip ospf virtual-links` |
| ABR status | `show ip ospf border-routers` | `show ospf route abr` | `show ip ospf border-routers` |
| ASBR status | `show ip ospf border-routers` (includes ASBRs) | `show ospf route asbr` | `show ip ospf border-routers` |
| Area range/summary | `show ip ospf \| include summary-address` | `show ospf overview \| match "range"` | `show ip ospf \| include summary-address` |
| Stub area config | `show running \| section ospf \| include stub` | `show configuration protocols ospf area [id]` | `show running-config \| section ospf \| include stub` |

### Area Configuration Notes

- **Cisco:** `show ip ospf border-routers` lists all ABRs and ASBRs known to this router with their Router IDs and the area through which they are reachable. Useful for verifying inter-area and external route paths.
- **JunOS:** Separates ABR and ASBR route queries. `show ospf route abr` and `show ospf route asbr` provide next-hop and metric for reaching each border router.
- **EOS:** `show ip ospf border-routers` output matches Cisco format. Virtual link status is shown via `show ip ospf virtual-links` — a virtual link in "down" state means the transit area path to the remote ABR is broken.
- **Stub area invariant:** All routers in a stub or NSSA area must agree on the area type. A single router misconfigured as standard (non-stub) in a stub area will fail to form adjacencies with all stub routers in that area.
