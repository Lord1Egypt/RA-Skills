---
name: ospf-analysis
description: >-
  OSPF protocol analysis with adjacency diagnosis, area design validation, LSA
  interpretation, and SPF convergence assessment. Multi-vendor coverage for
  Cisco IOS-XE, Juniper JunOS, and Arista EOS with protocol-first diagnostic
  reasoning.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔍","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["ospf","routing","protocol"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# OSPF Protocol Analysis

Protocol-reasoning-driven analysis skill for OSPF adjacency formation, area
design, LSDB integrity, and SPF convergence. Unlike device health checks that
compare counters against thresholds, OSPF analysis requires interpreting the
neighbor FSM, walking the LSA flooding scope, and validating area topology
across the control plane.

Commands are labeled **[Cisco]**, **[JunOS]**, or **[EOS]** where syntax
diverges. Unlabeled statements apply to all three vendors.

## When to Use

- OSPF neighbor adjacency not forming or stuck in a non-Full state
- Unexpected route changes or missing routes in the OSPF domain
- Area design review — backbone connectivity, stub/NSSA configuration audit
- SPF algorithm running too frequently (unstable link, flapping interface)
- Post-change verification of OSPF configuration (new interfaces, area changes,
  redistribution updates)
- LSDB growing unexpectedly or LSA age anomalies indicating flooding issues
- Convergence too slow after planned maintenance or unplanned link failure

## Prerequisites

- SSH or console access to the router (read-only privilege sufficient)
- OSPF process running on the device with at least one active interface
- Knowledge of expected area topology: which routers are ABRs/ASBRs, which
  interfaces belong to which areas, expected neighbor relationships
- Awareness of configured authentication type per area (none, simple, MD5)
- Router IDs known or deterministic (explicit configuration preferred over
  auto-selection from loopback/interface addresses)

## Procedure

Follow this diagnostic flow sequentially. Each step builds on data from
prior steps, moving from broad inventory to targeted diagnosis.

### Step 1: OSPF Instance and Interface Inventory

Verify OSPF is running and confirm which interfaces participate in each area.

**[Cisco]**
```
show ip ospf interface brief
```

**[JunOS]**
```
show ospf interface
```

**[EOS]**
```
show ip ospf interface brief
```

Record each interface: area assignment, network type (broadcast, point-to-point,
NBMA), state (DR, BDR, DROther, Point-to-Point), cost, and hello/dead timers.
Compare against expected design — every interface that should participate must
appear. An interface missing from output means OSPF is not enabled on it (missing
`network` statement or `ip ospf` configuration). Verify area assignments match
the design — a misassigned area creates a separate adjacency domain.

### Step 2: Neighbor State Assessment

List all OSPF neighbors and interpret their FSM state.

**[Cisco]**
```
show ip ospf neighbor
```

**[JunOS]**
```
show ospf neighbor
```

**[EOS]**
```
show ip ospf neighbor
```

Compare the neighbor list against expected topology. Every directly connected
OSPF router should appear. For each neighbor not in **Full** state, the FSM
state reveals the failure domain:

- **Down** → No hellos received from this neighbor. Causes: interface down,
  OSPF not enabled on remote interface, ACL blocking multicast 224.0.0.5/6.
- **Attempt** → (NBMA only) Unicast hello sent, no reply. The neighbor is
  configured but not responding.
- **Init** → Hellos received but this router's RID is not in the neighbor's
  hello. Causes: one-way communication — area ID mismatch, authentication
  mismatch, hello/dead timer mismatch, or MTU preventing return hellos.
- **2-Way** → Bidirectional communication confirmed. On broadcast/NBMA
  networks, non-DR/BDR routers remain in 2-Way with each other — this is
  normal. Only DR/BDR pairs proceed to Full.
- **ExStart** → DR/BDR election complete, attempting to establish master/slave
  for database exchange. Stuck here = **MTU mismatch** (most common cause) or
  DBD packet issues.
- **Exchange** → Database Description (DBD) packets being exchanged. Stuck
  here = LSDB too large to synchronize or DBD retransmission failures.
- **Loading** → LSR/LSU exchange in progress, retrieving missing LSAs. Stuck
  here = unstable LSA flooding or peer withdrawing LSAs during sync.

Reference: `references/state-machine.md` for full FSM detail.

### Step 3: Area Design Validation

Verify OSPF area topology matches the intended design.

**[Cisco]**
```
show ip ospf | include Area|router
```

**[JunOS]**
```
show ospf overview
```

**[EOS]**
```
show ip ospf | include Area|router
```

Validate these design invariants:
- **Backbone connectivity:** Area 0 must be contiguous. If an ABR has area 0
  interfaces that cannot reach other area 0 routers, a virtual link is required.
  Verify virtual links are up if configured.
- **ABR identification:** Any router with interfaces in multiple areas is an
  ABR. Confirm ABR count matches design — unexpected ABRs indicate area
  misconfiguration.
- **ASBR identification:** Routers performing redistribution into OSPF. Verify
  only intended routers are ASBRs — unplanned redistribution causes routing
  instability.
- **Stub/NSSA consistency:** All routers in a stub or NSSA area must agree on
  the area type. A mismatch prevents adjacency formation. NSSA areas generate
  Type 7 LSAs that ABRs translate to Type 5 — verify translation is occurring.

### Step 4: LSDB Analysis

Examine the Link-State Database for integrity and anomalies.

**[Cisco]**
```
show ip ospf database database-summary
```

**[JunOS]**
```
show ospf database summary
```

**[EOS]**
```
show ip ospf database database-summary
```

Check LSA types and counts per area:
- **Type 1 (Router):** One per router per area. Count should match router count.
- **Type 2 (Network):** One per broadcast/NBMA segment with a DR. Count should
  match multi-access segment count.
- **Type 3 (Summary):** Generated by ABRs. High count in stub areas indicates
  summarization not configured.
- **Type 4 (ASBR Summary):** Generated by ABRs to advertise ASBR reachability.
- **Type 5 (External):** Generated by ASBRs. Should not appear in stub areas.
  Unexpected Type 5 LSAs indicate redistribution issues.
- **Type 7 (NSSA External):** NSSA equivalent of Type 5. Translated to Type 5
  by the ABR at the NSSA boundary.

Check LSA age: maximum age is 3600 seconds, LSAs are refreshed at 1800 seconds.
LSAs with age near 3600 that are not being refreshed indicate an originating
router has lost reachability. LSAs with age stuck at 3600 (MaxAge) are being
flushed from the LSDB — excessive MaxAge LSAs indicate instability.

### Step 5: SPF Convergence Assessment

Evaluate SPF calculation frequency and convergence behavior.

**[Cisco]**
```
show ip ospf | include SPF
```

**[JunOS]**
```
show ospf statistics
```

**[EOS]**
```
show ip ospf | include SPF
```

Check SPF run count and last execution time. Frequent SPF runs (more than once
per minute sustained) indicate network instability — a flapping link or
interface causing repeated LSA updates. Identify the trigger by checking the
LSDB for recently updated LSAs (low age values).

Review SPF throttle timers: initial delay, secondary delay, and maximum hold
time. Aggressive timers (low initial delay) provide faster convergence but
increase CPU load during instability. Conservative timers protect the CPU but
delay convergence.

After a planned change, measure time from the change event to the last SPF run.
Compare against the convergence target for the deployment type.

## Threshold Tables

Operational parameter norms for OSPF — protocol-level expectations by network
type and deployment scale.

**Hello and Dead Interval Defaults:**

| Network Type | Hello Interval | Dead Interval | Notes |
|-------------|---------------|---------------|-------|
| Broadcast | 10s | 40s | Default for Ethernet |
| Point-to-Point | 10s | 40s | Default for serial/P2P |
| NBMA | 30s | 120s | Requires neighbor statements |
| Point-to-Multipoint | 30s | 120s | No DR election |

All routers on a segment must agree on hello and dead intervals — mismatch
prevents adjacency.

**LSA Norms:**

| Parameter | Normal | Warning | Critical |
|-----------|--------|---------|----------|
| LSA age | 0–1800s | 1800–3500s | 3600s (MaxAge) |
| LSA refresh | Every 1800s | Missed refresh | Persistent MaxAge |
| Type 1 count per area | = router count | >2x routers | Indicates duplicate RID |
| Type 5 count (enterprise) | 10–500 | >1000 | >5000 |
| Type 5 in stub area | 0 | Any (design violation) | — |

**SPF Norms:**

| Parameter | Normal | Warning | Critical |
|-----------|--------|---------|----------|
| SPF runs (per hour) | 1–5 | 6–20 | >20 |
| SPF initial delay | 50–200ms | <50ms (too aggressive) | >5000ms (too slow) |
| SPF max hold | 5000–10000ms | <2000ms | >50000ms |
| Convergence (single link) | <1s | 1–5s | >10s |

## Decision Trees

### Adjacency Not Forming

```
Neighbor not reaching Full state
├── State: Down
│   ├── Interface up? → Check Layer 1/2 status
│   ├── OSPF enabled on interface? → Check network statement or ip ospf config
│   ├── Correct area? → Compare area ID both sides
│   └── Multicast reachable? → Check ACLs for 224.0.0.5/224.0.0.6
│
├── State: Init (one-way)
│   ├── Hello timer mismatch? → Compare hello/dead intervals both sides
│   ├── Area ID mismatch? → Must match exactly on shared segment
│   ├── Authentication mismatch? → Verify type and key both sides
│   ├── Subnet mismatch? → Interfaces must be on same subnet
│   └── MTU blocking return hellos? → Check interface MTU both sides
│
├── State: 2-Way (expected on broadcast for DROther↔DROther)
│   ├── Both routers DROther? → Normal — Full only with DR/BDR
│   ├── DR/BDR election stuck? → Check priority values, verify DR is up
│   └── Unexpected? → Force DR election: clear ospf process (disruptive)
│
├── State: ExStart (most actionable stuck state)
│   ├── MTU mismatch? → Compare MTU both sides (most common cause)
│   │   ├── Cisco: ip mtu vs ip ospf mtu-ignore
│   │   ├── JunOS: interface MTU settings
│   │   └── Fix: match MTU or enable mtu-ignore (workaround)
│   └── DBD packet issues? → Check for packet drops, interface errors
│
├── State: Exchange
│   ├── LSDB too large? → Reduce area scope, add summarization
│   ├── DBD retransmissions? → Check interface reliability, CRC errors
│   └── CPU overloaded? → Check process CPU during exchange
│
└── State: Loading
    ├── LSAs being withdrawn during sync? → Check for flapping neighbor
    ├── Incomplete LSR responses? → Verify peer stability
    └── Timeout? → Increase retransmit interval if link is slow
```

### Missing or Unexpected Routes

```
Route not in routing table (or unexpected route present)
├── Missing route?
│   ├── LSA in LSDB? → show ip ospf database [type] [id]
│   │   ├── LSA present → SPF did not install
│   │   │   ├── Better route via another protocol? → Check admin distance
│   │   │   ├── Filtered by distribute-list? → Check outbound filters
│   │   │   └── Next-hop unreachable? → Verify forwarding address
│   │   └── LSA absent → Not being advertised
│   │       ├── In stub area? → Type 5 filtered by design — use NSSA or default
│   │       ├── ABR not summarizing? → Check area range / summary config
│   │       ├── Redistribution missing? → Verify ASBR redistribute config
│   │       └── Originator down? → Check originating router's OSPF status
│   └── Check area boundaries → ABR filtering or summarization may exclude
│
└── Unexpected route?
    ├── Unexpected Type 5 LSA? → Identify ASBR → check redistribution scope
    ├── Unexpected Type 7 → Type 5 translation? → Check NSSA ABR behavior
    ├── Route from wrong area? → Verify area assignments on originator
    └── Duplicate router ID? → Two routers with same RID cause LSA conflicts
```

## Report Template

```
OSPF ANALYSIS REPORT
=====================
Device: [hostname]
Vendor: [Cisco | JunOS | EOS]
OSPF Process ID: [process-id]
Router ID: [router-id]
Check Time: [timestamp]
Performed By: [operator/agent]

ADJACENCY STATUS:
- Total neighbors expected: [n]
- Full: [n] | Non-Full: [n]
- Neighbors requiring attention: [list with FSM states]

AREA TOPOLOGY:
- Areas configured: [list with types — backbone, stub, NSSA, standard]
- ABR count: [n] | ASBR count: [n]
- Backbone contiguous: [yes/no]

FINDINGS:
1. [Severity] [Category] — [Description]
   Neighbor/Area: [identifier]
   Observed: [state or metric]
   Expected: [normal state or value]
   Root Cause: [diagnosis from decision tree]
   Action: [recommended remediation]

LSDB SUMMARY:
- LSA counts by type: [Type 1: n, Type 2: n, ...]
- MaxAge LSAs: [count — 0 is healthy]
- LSA age anomalies: [any near-expiry LSAs]

SPF STATUS:
- Last SPF run: [timestamp]
- SPF runs in last hour: [count]
- Convergence assessment: [healthy/warning/critical]

RECOMMENDATIONS:
- [Prioritized action list]

NEXT CHECK: [CRITICAL: 1hr, WARNING: 8hr, HEALTHY: 24hr]
```

## Troubleshooting

### MTU Mismatch (ExStart Stuck)

The most common OSPF adjacency failure. Neighbors reach ExStart but cannot
proceed because DBD packets exceed the smaller MTU and are dropped. Fix by
matching MTU on both sides. Workaround: `ip ospf mtu-ignore` (Cisco/EOS) skips
the check but may cause fragmentation issues. On JunOS, set matching MTU values
at the interface level.

### Duplicate Router IDs

Two routers with the same Router ID cause LSA conflicts — each router's Type 1
LSA overwrites the other's in the LSDB. Symptoms: routes flapping, intermittent
reachability. Fix: assign unique router IDs explicitly. Detect by checking for
Type 1 LSAs with the same Link State ID but different advertising routers.

### Area 0 Discontinuity

If area 0 is split, inter-area routing breaks — ABRs cannot flood Type 3 LSAs
across the gap. Fix: restore physical backbone connectivity or configure virtual
links through a transit area. Virtual links are temporary solutions — long-term
design should maintain contiguous backbone.

### Excessive Redistribution

Redistributing too many external routes into OSPF floods the LSDB with Type 5
LSAs, increasing SPF computation time and memory usage. Use route-maps with
prefix-lists to limit redistribution scope. Consider stub or NSSA areas to
shield non-edge routers from external LSAs.

### Type 7 to Type 5 Translation

In NSSA areas, the ABR with the highest Router ID translates Type 7 LSAs to
Type 5 for flooding into area 0. If translation fails, external routes from the
NSSA are invisible to the rest of the OSPF domain. Verify the translator ABR
is healthy and the forwarding address in the Type 7 LSA is reachable.
