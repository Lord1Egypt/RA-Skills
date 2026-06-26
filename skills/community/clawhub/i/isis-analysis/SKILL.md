---
name: isis-analysis
description: >-
  IS-IS protocol analysis with adjacency diagnosis, LSPDB analysis, level 1/2
  routing validation, and NET address verification. Multi-vendor coverage for
  Cisco IOS-XE, Juniper JunOS, and Arista EOS with protocol-first diagnostic
  reasoning.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔍","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["isis","routing","protocol"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# IS-IS Protocol Analysis

Protocol-reasoning-driven analysis skill for IS-IS adjacency formation, LSPDB
integrity, level 1/2 routing, and NET address validation. Unlike device health
checks that compare counters against thresholds, IS-IS analysis requires
interpreting adjacency state machines, validating NET addressing, verifying DIS
election, and assessing LSP flooding across the link-state domain.

Commands are labeled **[Cisco]**, **[JunOS]**, or **[EOS]** where syntax
diverges. Unlabeled statements apply to all three vendors.

## When to Use

- IS-IS adjacency not forming or stuck in Init state
- Unexpected route changes or missing routes in the IS-IS domain
- Level 1/2 boundary issues — suboptimal routing, missing L1 default, route
  leaking not working as intended
- LSPDB inconsistency — LSP count mismatch between neighbors, unexpected purges,
  sequence number anomalies
- NET address conflict or system ID duplication causing LSP wars
- Post-change verification of IS-IS configuration (new interfaces, area changes,
  metric style migration, authentication rollout)
- DIS election not converging on broadcast segments

## Prerequisites

- SSH or console access to the router (read-only privilege sufficient)
- IS-IS process running on the device with at least one active interface
- Knowledge of expected level topology: which routers are L1-only, L2-only, or
  L1/L2, and which areas (area addresses) are in use
- System IDs and NETs known or documented — NET format is
  `AFI.areaID.systemID.NSEL` (e.g., `49.0001.1921.6800.1001.00`)
- Awareness of configured authentication per level and interface (none, MD5,
  HMAC-SHA)

## Procedure

Follow this diagnostic flow sequentially. Each step builds on data from
prior steps, moving from broad inventory to targeted diagnosis.

### Step 1: IS-IS Instance and Interface Inventory

Verify IS-IS is running and confirm which interfaces participate at each level.

**[Cisco]**
```
show isis interface brief
```

**[JunOS]**
```
show isis interface
```

**[EOS]**
```
show isis interface brief
```

Record each interface: level enablement (L1, L2, or L1/L2), circuit type
(point-to-point or broadcast), metric, hello interval, and hold time. Compare
against expected design — every interface that should participate must appear.
An interface missing from output means IS-IS is not enabled on it (missing
under the IS-IS router config or interface config). Verify the NET address with
`show isis protocol` (Cisco), `show isis overview` (JunOS), or
`show isis summary` (EOS) — the NET must be correctly formed and unique.

### Step 2: Adjacency Assessment

List all IS-IS adjacencies and interpret their state.

**[Cisco]**
```
show isis neighbors
```

**[JunOS]**
```
show isis adjacency
```

**[EOS]**
```
show isis neighbors
```

Compare the neighbor list against expected topology. For each adjacency, verify:
- **State:** Up is healthy; Init means one-way (hellos received but this
  router's SNPA/system ID not in the neighbor's hello). Down means no hellos
  received.
- **Level match:** L1 neighbors must share at least one area address. L2
  neighbors can be in different areas — only system ID uniqueness is required.
  An L1-only router will not form L2 adjacency with an L2-only router.
- **Circuit type:** On broadcast segments, check DIS (Designated Intermediate
  System) election. Unlike OSPF DR/BDR, IS-IS DIS election is preemptive — a
  new router with higher priority takes over immediately.
- **DIS status:** On broadcast segments, identify which router is DIS for each
  level. DIS sends CSNPs every 10 seconds and creates the pseudonode LSP.

### Step 3: NET Address Validation

Verify NET format and system ID uniqueness across the domain.

**[Cisco]**
```
show isis protocol | include NET|System
```

**[JunOS]**
```
show isis overview | match "NET|System"
```

**[EOS]**
```
show isis summary | include NET|System
```

Validate NET structure:
- **AFI (Authority and Format Identifier):** Typically `49` for private IS-IS
  domains. Must be consistent within the domain.
- **Area ID:** Variable length. All L1 neighbors must share at least one area
  address to form L1 adjacency. L1/L2 and L2-only routers can have different
  area addresses and still form L2 adjacency.
- **System ID:** 6 bytes, must be globally unique within the IS-IS domain.
  Duplicate system IDs cause LSP wars — both routers originate LSPs with the
  same system ID but different content, causing continuous purge/regenerate
  cycles.
- **NSEL (N-Selector):** Must be `00` for the router itself. A non-zero NSEL
  identifies an upper-layer protocol endpoint, not the router.

### Step 4: LSPDB Analysis

Examine the Link-State Protocol Data Unit database for integrity.

**[Cisco]**
```
show isis database detail | include LSP|Lifetime|Sequence
```

**[JunOS]**
```
show isis database extensive | match "LSP|Lifetime|Sequence"
```

**[EOS]**
```
show isis database detail | include LSP|Lifetime|Sequence
```

Assess LSPDB health:
- **LSP count:** Compare across neighbors in the same level — counts must match
  (LSPDB synchronization invariant). A mismatch indicates flooding failure or
  partition.
- **Remaining lifetime:** Default maximum is 1200 seconds. Originating routers
  refresh at 900 seconds (default). An LSP with lifetime near 0 that is not
  refreshed indicates the originator is unreachable. Lifetime at 0 means the
  LSP is being purged.
- **Sequence numbers:** Must increase monotonically. If the same system ID's
  LSP sequence number jumps backward, a router has restarted and is re-
  originating from a lower sequence number — or there is a system ID conflict.
- **LSP purges:** An LSP with remaining lifetime of 0 and empty TLV content is
  a purge. Frequent purges for the same system ID indicate instability — either
  the originator is flapping or two routers share the system ID (LSP war).
- **Overload bit (OL):** If set, SPF will not use this router for transit
  traffic. Check whether OL is intentional (maintenance, startup delay) or
  indicates a problem (memory exhaustion).

### Step 5: Level 1/2 Routing and Route Leaking

Verify inter-level routing behavior at L1/L2 boundaries.

**[Cisco]**
```
show isis rib | include L1|L2|leak
```

**[JunOS]**
```
show isis route | match "L1|L2|leak"
```

**[EOS]**
```
show isis route | include L1|L2|leak
```

Validate inter-level behavior:
- **L1→L2 redistribution:** L1/L2 routers automatically redistribute L1 routes
  into L2 by default. Verify L1 prefixes appear in the L2 LSPDB. If missing,
  check for redistribution filters or route policies on the L1/L2 router.
- **L2→L1 route leaking:** Not automatic — requires explicit configuration.
  If configured, verify leaked L2 routes appear in the L1 RIB. Missing leaked
  routes indicate policy misconfiguration or the leak filter is too restrictive.
- **Attached bit:** L1/L2 routers set the Attached bit in their L1 LSP. L1-only
  routers use this to install a default route toward the nearest L1/L2 router.
  If no L1/L2 router has the Attached bit set, L1-only routers have no path
  out of the area. Verify with LSPDB detail — check the ATT flag on L1/L2
  router LSPs.
- **Suboptimal routing:** L1-only routers always route toward the nearest
  L1/L2 router (default route). If there are multiple L1/L2 exit points,
  traffic may take a suboptimal path. Route leaking L2→L1 with specific
  prefixes fixes this by giving L1 routers more specific routing information.

## Threshold Tables

Operational parameter norms for IS-IS — protocol-level expectations by network
type and deployment scale.

**Hello and Hold Timer Defaults:**

| Parameter | Cisco Default | JunOS Default | EOS Default | Notes |
|-----------|--------------|---------------|-------------|-------|
| Hello (broadcast) | 10s | 9s | 10s | Per-level configurable |
| Hello (P2P) | 10s | 9s | 10s | Per-level configurable |
| Hold multiplier | 3× hello | 3× hello | 3× hello | Dead = hello × multiplier |
| CSNP interval (DIS) | 10s | 10s | 10s | Only DIS sends CSNPs |
| PSNP interval | 2s | 2s | 2s | Request missing LSPs |

**LSPDB Norms:**

| Parameter | Normal | Warning | Critical |
|-----------|--------|---------|----------|
| LSP max lifetime | 1200s | — | — |
| LSP refresh | 900s | Missed refresh | Lifetime < 300s |
| LSP remaining lifetime | 300–1200s | 60–300s | < 60s (near purge) |
| LSP purge rate | 0/hour | 1–5/hour | > 5/hour |
| LSPDB mismatch (neighbors) | 0 LSP diff | 1–3 diff | > 3 diff |
| Overload bit | Clear | Set (intentional) | Set (unintentional) |

**SPF Norms:**

| Parameter | Normal | Warning | Critical |
|-----------|--------|---------|----------|
| SPF runs (per hour) | 1–5 | 6–20 | > 20 |
| SPF initial delay | 50–200ms | < 50ms | > 5000ms |
| SPF max hold | 5000–10000ms | < 2000ms | > 50000ms |
| Convergence (single link) | < 1s | 1–5s | > 10s |

**Metric Norms:**

| Metric Style | Range | Notes |
|-------------|-------|-------|
| Narrow (original) | 1–63 per link | 10-bit path metric max (1023) |
| Wide (extended) | 1–16777215 per link | 32-bit path metric — preferred |
| Transition | Both | During narrow→wide migration |

## Decision Trees

### Adjacency Not Forming

```
IS-IS adjacency not reaching Up state
├── State: Down (no hellos received)
│   ├── Interface up? → Check Layer 1/2 status
│   ├── IS-IS enabled on interface? → Check IS-IS config on both sides
│   ├── Correct circuit type? → P2P interface must match both sides
│   └── Hello reaching peer? → Check ACLs, VLAN, encapsulation
│
├── State: Init (one-way hellos)
│   ├── Level mismatch?
│   │   ├── L1 needs same area → Compare area addresses in NETs
│   │   └── L2 allows different areas → Check both have L2 enabled
│   ├── Hello parameters?
│   │   ├── Authentication mismatch → Verify key/type per level
│   │   └── Hello interval incompatible → Not required to match but
│   │       hold time must exceed remote hello interval
│   ├── Interface type mismatch?
│   │   ├── P2P vs broadcast → Must agree on circuit type
│   │   └── Broadcast → DIS election proceeds after adjacency forms
│   ├── MTU issue? → IS-IS PDUs may be dropped if oversized
│   │   ├── Check interface MTU both sides
│   │   └── IS-IS does not negotiate MTU like OSPF — silent drop
│   └── Circuit type mismatch?
│       ├── L1-only ↔ L2-only → No common level → no adjacency
│       └── L1/L2 ↔ L1 → L1 adjacency forms; L2 does not
│
├── DIS election issue (broadcast only)
│   ├── DIS not elected? → Check priority (highest wins, then SNPA)
│   ├── DIS preemption → New higher-priority router takes DIS immediately
│   │   └── Unlike OSPF DR — IS-IS DIS is preemptive
│   └── Pseudonode LSP missing? → DIS must originate pseudonode LSP
│
└── Adjacency flapping (Up↔Down cycling)
    ├── Hello hold expiry → Check for packet loss or CPU overload
    ├── Authentication key rollover → Verify key transition timing
    └── Interface errors → Check CRC, input errors, drops
```

### LSPDB Inconsistency

```
LSPDB mismatch or instability detected
├── LSP purge seen (lifetime = 0)
│   ├── System ID conflict? → Two routers with same system ID
│   │   ├── Both originate LSPs → Continuous purge/regenerate cycle
│   │   ├── Sequence numbers jump erratically → Confirms conflict
│   │   └── Fix: assign unique system IDs, check NET addresses
│   ├── Router departed gracefully? → Normal purge after shutdown
│   └── Router crashed? → LSP ages out (1200s) then purges
│
├── LSPDB count mismatch between neighbors
│   ├── MTU preventing LSP flooding? → Large LSPs dropped
│   │   ├── Check interface MTU across path
│   │   └── Enable LSP fragmentation or increase MTU
│   ├── Partition? → L2 backbone split → two independent LSPDBs
│   │   ├── Verify L2 connectivity between all L2 routers
│   │   └── Check for failed L2 link isolating a segment
│   └── Flooding blocked? → Authentication mismatch on one link
│       └── Adjacency up but LSPs rejected due to auth failure
│
├── Overload bit (OL) set
│   ├── Intentional? → Maintenance mode or on-startup timer
│   ├── Memory exhaustion? → Router cannot hold full LSPDB
│   └── Startup delay? → OL set for N seconds after process restart
│
└── Sequence number anomaly
    ├── Backward jump? → Router restarted, re-originating from lower seq
    ├── Rapid increment? → Frequent topology changes triggering re-origination
    └── Stuck at max? → Sequence wrap — extremely rare, requires process restart
```

## Report Template

```
IS-IS ANALYSIS REPORT
======================
Device: [hostname]
Vendor: [Cisco | JunOS | EOS]
IS-IS Instance: [tag/instance name]
System ID: [system-id]
NET: [full NET address]
Check Time: [timestamp]
Performed By: [operator/agent]

ADJACENCY STATUS:
- Total adjacencies expected: [n]
- Up: [n] | Init: [n] | Down: [n]
- DIS role: [DIS for L1/L2 on segment X, or none]
- Adjacencies requiring attention: [list with states and levels]

LEVEL TOPOLOGY:
- Levels configured: [L1, L2, L1/L2]
- Area addresses: [list]
- Attached bit: [set/clear on L1 LSP]

FINDINGS:
1. [Severity] [Category] — [Description]
   Neighbor/Interface: [identifier]
   Observed: [state or metric]
   Expected: [normal state or value]
   Root Cause: [diagnosis from decision tree]
   Action: [recommended remediation]

LSPDB SUMMARY:
- L1 LSP count: [n] | L2 LSP count: [n]
- LSP purges in last hour: [count — 0 is healthy]
- Overload bit: [set/clear]
- Lifetime anomalies: [any near-expiry LSPs]

ROUTE ANALYSIS:
- L1 routes: [count] | L2 routes: [count]
- Route leaking: [configured/not configured — expected behavior]

RECOMMENDATIONS:
- [Prioritized action list]

NEXT CHECK: [CRITICAL: 1hr, WARNING: 8hr, HEALTHY: 24hr]
```

## Troubleshooting

### System ID Conflict (LSP War)

Two routers with the same system ID cause an LSP war — each router originates
an LSP with the same system ID but different content. Each purges the other's
LSP and regenerates its own, creating continuous churn. Symptoms: rapidly
incrementing sequence numbers, frequent purge events, unstable routing.
Detect by checking for the same system ID with two different SNPAs or source
addresses in adjacency tables. Fix: assign unique system IDs.

### Area Mismatch Preventing L1 Adjacency

L1 adjacency requires at least one matching area address in the NET. If two
routers have different area addresses and are both L1-only, no adjacency forms.
L1/L2 routers with different areas can still form L2 adjacency but not L1.
Verify area addresses on both sides. Fix: correct the area address or change
one router to L2-only if inter-area routing is the goal.

### Metric Style Mismatch (Narrow vs Wide)

A router using narrow metrics (1–63) and a neighbor using wide metrics
(1–16777215) may form adjacency but routes may not compute correctly if one
side cannot interpret the other's TLVs. During migration, configure both sides
for transition mode (advertise both narrow and wide TLVs). Verify with LSPDB
detail — check for both old-style and extended IP reachability TLVs.

### Authentication Mismatch

IS-IS supports per-level and per-interface authentication. A mismatch prevents
adjacency formation (hellos rejected) or LSP flooding (LSPs rejected). Unlike
OSPF where auth mismatch stops hellos, IS-IS can have adjacency up but LSP
flooding blocked if hello auth succeeds but LSP auth fails. Check auth config
at both hello and LSP levels independently.

### LSPDB Overload from Excessive Redistribution

Redistributing large external route tables into IS-IS generates many LSPs,
increasing LSPDB size, SPF computation time, and flooding overhead. Use route
policies to limit redistribution scope. Consider setting the overload bit on
non-transit routers that cannot handle the full LSPDB. Monitor LSP fragment
count — each router can originate up to 256 LSP fragments (0–255).
