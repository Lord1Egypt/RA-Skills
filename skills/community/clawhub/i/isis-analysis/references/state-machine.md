# IS-IS Adjacency State Machine and LSPDB Flooding

Reference for the IS-IS adjacency formation, DIS election, and LSPDB flooding
mechanics. IS-IS adjacency is simpler than OSPF (three states vs seven) but
LSPDB flooding has unique mechanics — CSNP/PSNP exchange, LSP lifetime/refresh,
and level-based flooding scope.

## Adjacency State Overview

### Point-to-Point Links

```
Down ──→ Initializing ──→ Up
  ↑                        │
  └────────────────────────┘
    (hold timer expiry or interface down → back to Down)
```

On P2P links, the adjacency FSM has three states. The transition is direct
without DR/BDR or DIS election. Both sides send IIH (IS-IS Hello) packets.

### Broadcast Links

```
Down ──→ Initializing ──→ Up ──→ [DIS Election]
  ↑                        │
  └────────────────────────┘
    (hold timer expiry or interface down → back to Down)
```

On broadcast links, after adjacency reaches Up, DIS election occurs. Unlike
OSPF where DR election happens at 2-Way, IS-IS elects DIS independently of
adjacency state — all routers on the segment form adjacency with all others
(no DROther↔DROther 2-Way limitation).

## Adjacency States

### Down

**Definition:** No IS-IS Hello (IIH) PDUs have been received from this system
on this interface. The adjacency does not exist.

**Entry conditions:**
- Initial state for all potential adjacencies
- Hold timer expiry (no IIH received within hold time)
- Interface down event
- IS-IS process restart

**Exit transitions:**
- **IIH received** → transition to **Initializing**

**Stuck-state causes:**
- Layer 1/2 failure — physical interface down
- IS-IS not enabled on the remote interface
- IIH packets blocked — ACL, VLAN mismatch, encapsulation mismatch
- Different IS-IS instances configured (IS-IS does not use multicast group
  differentiation like OSPF process IDs — but mismatched instances may have
  different NETs causing level incompatibility)

### Initializing (Init)

**Definition:** An IIH has been received from the neighbor, but the neighbor's
IIH does not contain this system's SNPA (MAC address on broadcast) or local
circuit ID (on P2P). One-way communication confirmed.

**Entry conditions:**
- IIH received in Down state
- IIH received but this system is not listed in the neighbor's IS Neighbors TLV

**Exit transitions:**
- **Two-way confirmed** → transition to **Up** (this system's SNPA or circuit
  ID seen in neighbor's IIH IS Neighbors TLV)
- **Hold timer expiry** → back to **Down**

**Stuck-state causes:**
- **Level mismatch:** L1 requires matching area address. If one side is L1-only
  and the other has a different area, no L1 adjacency forms. L2 adjacency
  requires both sides to have L2 enabled but does not require area match.
- **Circuit type mismatch:** One side configured as P2P, other as broadcast.
  The IIH PDU format differs (P2P IIH vs LAN IIH) — mismatched types cannot
  parse each other's hellos.
- **Authentication mismatch:** IIH authentication key or type mismatch.
  IS-IS authenticates hellos separately from LSPs — hello auth failure prevents
  adjacency; LSP auth failure blocks flooding but not adjacency.
- **MTU issue:** IS-IS does not have an explicit MTU negotiation like OSPF
  ExStart. However, if IIH PDUs are too large (many area addresses, large TLVs),
  they may be silently dropped.
- **Three-way handshake:** RFC 5303 defines a three-way handshake for P2P
  adjacency. If one side supports it and the other does not, adjacency may
  remain in Init. Modern implementations all support it — check for legacy
  routers.

### Up

**Definition:** Bidirectional IIH exchange confirmed. This system's identifier
appears in the neighbor's IIH. The adjacency is fully operational, LSPDB
synchronization is in progress or complete, and routes are computed via SPF.

**Entry conditions:**
- Two-way communication confirmed in Initializing state

**Exit transitions:**
- **Hold timer expiry** → back to **Down** (no IIH received within hold time)
- **Interface down** → back to **Down**
- **Level removal** → adjacency removed for that level

**Causes of leaving Up:**
- Hold timer expiry: IIHs not arriving — CPU overload, interface errors, QoS
  deprioritizing IS-IS PDUs
- Interface flap: brief down/up causes adjacency drop and re-formation
- IS-IS process restart: all adjacencies reset
- Configuration change: disabling IS-IS on the interface or changing level

**Note:** Unlike OSPF, IS-IS does not have ExStart/Exchange/Loading/Full states.
LSPDB synchronization happens after the adjacency is Up, using CSNP/PSNP
exchange. The adjacency remains Up during LSPDB sync — there is no state that
indicates "adjacency up but LSDB not yet synchronized."

## DIS Election

On broadcast (multi-access) segments, IS-IS elects a Designated Intermediate
System (DIS) per level. The DIS is functionally similar to OSPF's DR but with
important differences.

### Election Rules

1. **Priority:** Highest IS-IS interface priority wins (default 64 on all
   vendors, range 0–127). Priority 0 does NOT make a router ineligible (unlike
   OSPF where priority 0 means no DR eligibility).
2. **SNPA tiebreaker:** If priorities are equal, highest SNPA (MAC address) on
   the segment wins.
3. **Preemptive:** Unlike OSPF DR, the IS-IS DIS election IS preemptive. If a
   new router joins the segment with a higher priority, it takes over as DIS
   immediately. This simplifies the protocol but causes brief reconvergence
   whenever a higher-priority router joins.
4. **No BDR:** IS-IS has no Backup DIS. If the DIS fails, a new election occurs
   immediately among remaining routers.

### DIS Responsibilities

- **Pseudonode LSP:** The DIS originates a pseudonode LSP that represents the
  broadcast segment. All routers on the segment advertise adjacency to the
  pseudonode, and the pseudonode LSP lists all routers on the segment. This
  reduces the O(n²) full-mesh LSP problem to O(n).
- **CSNP generation:** The DIS sends Complete Sequence Number PDUs (CSNPs) every
  10 seconds on the broadcast segment. CSNPs list all LSPs in the DIS's LSPDB,
  allowing other routers to detect missing or outdated LSPs.
- **Faster hellos:** The DIS sends IIH packets at 1/3 of the configured hello
  interval (default: every ~3.3 seconds if hello is 10s). This allows faster
  detection of DIS failure.

### DIS vs OSPF DR Comparison

| Aspect | IS-IS DIS | OSPF DR |
|--------|-----------|---------|
| Election | Preemptive | Non-preemptive |
| Backup | None (no BDR) | BDR exists |
| Priority 0 | Eligible (lowest priority) | Ineligible |
| Default priority | 64 | 1 |
| Adjacency model | All↔All (full mesh) | DR/BDR↔DROther only |
| Reconvergence on failure | New election + new pseudonode LSP | BDR promotes to DR |

### DIS Election Failures

- **Frequent DIS changes:** A router with high priority flapping causes
  repeated DIS elections. Each change regenerates the pseudonode LSP, triggering
  SPF on all routers in the level.
- **No adjacencies forming after DIS change:** The new DIS must originate the
  pseudonode LSP. If it fails to do so (process bug, resource exhaustion),
  routes through that segment are lost.
- **Priority misconfiguration:** All routers at default priority (64) means DIS
  is chosen by MAC address — this is non-deterministic across reboots if MAC
  assignments change. Set explicit priorities for stable DIS placement.

## LSPDB Flooding Mechanics

IS-IS uses a reliable flooding mechanism based on three PDU types: LSP, CSNP,
and PSNP. Flooding is per-level — L1 LSPs flood only within the area, L2 LSPs
flood across the L2 backbone.

### PDU Types

| PDU | Type | Purpose | Scope |
|-----|------|---------|-------|
| IIH (IS-IS Hello) | Hello | Adjacency discovery, DIS election, keepalive | Per-interface |
| LSP (Link-State PDU) | Update | Carry topology and reachability information | Per-level |
| CSNP (Complete SNP) | Sync | List all LSPs in database — DIS sends periodically | Per-level, broadcast |
| PSNP (Partial SNP) | Request/Ack | Request missing LSPs or acknowledge received LSPs | Per-level |

### LSP Generation and Refresh

```
Router originates LSP → floods to all neighbors in same level
    ↓
LSP lifetime starts at max (1200s default) → counts down
    ↓
At refresh interval (900s default) → router re-originates with new sequence number
    ↓
If router goes down → LSP ages to 0 → purge floods to all routers
    ↓
All routers remove purged LSP from LSPDB
```

**Key parameters:**
- **Max LSP lifetime:** 1200 seconds (20 minutes). This is shorter than OSPF's
  3600 seconds. IS-IS LSPs age faster and require more frequent refresh.
- **LSP refresh interval:** 900 seconds (15 minutes). The originating router
  refreshes its LSPs before they expire. A healthy LSP should have remaining
  lifetime between 300 and 1200 seconds.
- **Sequence number:** 32-bit, starts at 1, increments with each re-origination.
  Monotonically increasing — a higher sequence number always supersedes a lower
  one.
- **Checksum:** IS-IS LSPs include a Fletcher checksum. A checksum failure
  causes the LSP to be discarded — check for memory corruption or transmission
  errors.

### CSNP/PSNP Exchange

**On broadcast segments (DIS-driven):**
```
DIS sends CSNP (every 10s) listing all LSPs
    ↓
Other routers compare CSNP against their LSPDB
    ↓
Missing LSPs? → Router sends PSNP requesting the missing LSPs
    ↓
DIS (or any router with the LSP) responds with the full LSP
    ↓
Receiver acknowledges with PSNP (implicit on broadcast)
```

**On point-to-point links:**
```
After adjacency Up → both sides exchange CSNPs (one-time)
    ↓
Each side compares CSNP against its LSPDB
    ↓
Missing LSPs? → Send PSNP requesting them
    ↓
Neighbor responds with full LSP
    ↓
Receiver sends PSNP as explicit acknowledgment
    ↓
Ongoing: new LSPs flooded immediately, acknowledged by PSNP
```

**Key difference from OSPF:** OSPF uses DBD/LSR/LSU/LSAck with a master/slave
negotiation. IS-IS uses CSNP/PSNP without master/slave — both sides
independently compare and request missing LSPs. This is simpler but relies on
the DIS for periodic CSNP on broadcast segments.

### LSP Purge

An LSP with remaining lifetime = 0 and no TLV content is a **purge**. Purges
propagate through the level to remove stale information.

**Normal purge scenarios:**
- Router gracefully shuts down IS-IS — it originates a purge for its own LSPs
- Administrator removes an interface from IS-IS — the router re-originates its
  LSP without that interface's reachability

**Abnormal purge scenarios:**
- LSP ages to 0 without refresh → the router that originated it is unreachable
- System ID conflict → two routers purge each other's LSPs in a continuous cycle
- Corruption → checksum failure causes receiving router to purge and request a
  new copy

### LSP Fragmentation

A single router's IS-IS information may not fit in one LSP (due to MTU
constraints). IS-IS supports LSP fragmentation:

- **Fragment numbering:** `systemID.00-XX` where XX is the fragment number
  (00 to FF, max 256 fragments per pseudonode ID)
- **Pseudonode extension:** If 256 fragments are insufficient, additional
  pseudonode IDs can be used (systemID.01, .02, etc.)
- **MTU dependency:** LSP size is limited by the smallest MTU in the flooding
  domain. If one link has a small MTU, all LSPs must fit within it or they
  will be dropped on that link, causing LSPDB inconsistency

## Level 1/2 Interaction

IS-IS uses a two-level hierarchy for scalable routing. Understanding the
interaction between levels is critical for diagnosing inter-area routing issues.

### Level Roles

| Router Type | L1 Role | L2 Role | Typical Placement |
|------------|---------|---------|-------------------|
| L1-only | Area routing only | None | Stub/access routers |
| L2-only | None | Backbone routing only | Core backbone |
| L1/L2 | Area routing + ABR | Backbone routing | Area border |

### Attached Bit

L1/L2 routers set the **Attached (ATT) bit** in their L1 LSP. This signals to
L1-only routers that this L1/L2 router is a gateway to the rest of the network.
L1-only routers install a default route toward the nearest L1/L2 router with
the ATT bit set.

**Diagnostic implications:**
- **No ATT bit in any L1 LSP:** L1-only routers have no default route and
  cannot reach destinations outside their area.
- **Multiple L1/L2 routers with ATT bit:** L1-only routers use the nearest one
  (lowest metric). This may cause suboptimal routing if the nearest exit is not
  the best path to the destination.
- **ATT bit incorrectly clear:** If an L1/L2 router loses all L2 adjacencies,
  it clears the ATT bit. This is correct behavior — it should not attract L1
  traffic if it cannot forward it. Check L2 adjacency status on that router.

### Route Leaking

| Direction | Default Behavior | Configuration Required |
|-----------|-----------------|----------------------|
| L1 → L2 | Automatic (L1/L2 routers redistribute) | None (default) |
| L2 → L1 | Not automatic | Explicit route-leak policy required |

**L2→L1 route leaking** provides L1-only routers with specific routes from the
L2 domain, enabling optimal path selection instead of relying on the default
route to the nearest L1/L2 router. This is analogous to OSPF inter-area
summarization but in the reverse direction.

### Area Boundaries

IS-IS area boundaries exist on the **link**, not on the **router** (unlike
OSPF where ABRs have interfaces in multiple areas). An L1/L2 router maintains
separate L1 and L2 LSPDBs. L1 information is redistributed into L2 at the
router level.

```
[L1 Area 49.0001]         [L1 Area 49.0002]
  L1-only ── L1/L2 ══════ L1/L2 ── L1-only
              │    L2 backbone    │
              └───────────────────┘
```

The L2 backbone must be contiguous. If L2 connectivity is broken, inter-area
routing fails — there is no IS-IS equivalent of OSPF virtual links.

## Timer Reference

| Timer | Purpose | Default | Notes |
|-------|---------|---------|-------|
| IIH Interval (broadcast) | Hello interval on LAN | 10s (Cisco/EOS), 9s (JunOS) | Per-level configurable |
| IIH Interval (P2P) | Hello interval on P2P | 10s (Cisco/EOS), 9s (JunOS) | Per-level configurable |
| IIH Hold Multiplier | Dead = hello × multiplier | 3× | Hold time = hello × multiplier |
| DIS IIH rate | DIS sends hellos faster | 1/3 of hello interval | Only DIS uses this rate |
| CSNP Interval | DIS CSNP generation rate | 10s | Only DIS sends CSNPs on broadcast |
| PSNP Interval | PSNP transmission interval | 2s | Request/acknowledge interval |
| LSP Max Lifetime | Maximum LSP age | 1200s (20 min) | Shorter than OSPF (3600s) |
| LSP Refresh Interval | Self-LSP re-origination | 900s (15 min) | Must be < max lifetime |
| LSP Generation Interval | Min time between LSP originations | 50ms initial, 5s max | Throttled to prevent storms |
| SPF Initial Delay | Delay before first SPF | 50–200ms | Start of SPF throttle |
| SPF Secondary Delay | Delay for subsequent SPFs | 200–5000ms | Exponential backoff |
| SPF Max Hold | Maximum SPF interval | 5000–10000ms | Cap on backoff |

## Event-Driven Transitions Summary

| Event | In State | Transition To | Action |
|-------|----------|---------------|--------|
| IIH received | Down | Initializing | Record neighbor |
| Two-way confirmed | Initializing | Up | Begin LSPDB sync |
| Hold timer expiry | Init/Up | Down | Remove adjacency |
| Interface down | Any | Down | Remove adjacency |
| DIS election change | Up | Up (DIS role changes) | New pseudonode LSP |
| Level disabled | Up | Down (for that level) | Remove level adjacency |
| Area address change | Up (L1) | Down (L1) | L1 requires area match |
