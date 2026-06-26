# OSPF Neighbor Finite State Machine (FSM)

Reference for the OSPF neighbor state machine as defined in RFC 2328. Each
state describes the adjacency formation progress, what events cause transitions,
and what commonly causes a neighbor to become stuck in that state.

## State Overview

```
Down ──→ Attempt ──→ Init ──→ 2-Way ──→ ExStart ──→ Exchange ──→ Loading ──→ Full
  ↑                    ↑                    │            │          │          │
  └────────────────────┴────────────────────┴────────────┴──────────┴──────────┘
                        (any fatal error → back to Down)
```

The FSM is per-neighbor. Each OSPF neighbor relationship has an independent FSM
instance. On broadcast and NBMA networks, DR/BDR election at the 2-Way stage
determines which pairs proceed to Full — DROther-to-DROther pairs remain in
2-Way by design.

## States

### Down

**Definition:** No OSPF hello packets have been received from this neighbor. The
neighbor relationship does not exist or has been torn down.

**Entry conditions:**
- Initial state for all neighbors
- Neighbor hello not received within Dead Interval (timeout)
- KillNbr event (interface down, OSPF process restart)

**Exit transitions:**
- **HelloReceived** → transition to **Init**
- On NBMA networks: **Start event** → transition to **Attempt** (send unicast hello)

**Stuck-state causes:**
- Layer 1/2 failure — physical interface down, no link
- OSPF not enabled on the remote interface
- ACL or firewall blocking OSPF multicast (224.0.0.5 for AllSPFRouters,
  224.0.0.6 for AllDRouters)
- Remote interface in a different OSPF instance or process
- Hello packets being sent but not received (one-way link failure)

### Attempt

**Definition:** NBMA networks only. A unicast hello has been sent to the
neighbor, but no hello has been received in return.

**Entry conditions:**
- Start event on NBMA interface for a configured neighbor
- Only applicable to NBMA and Point-to-Multipoint-NonBroadcast network types

**Exit transitions:**
- **HelloReceived** → transition to **Init**
- **Dead Interval expires** → back to **Down**

**Stuck-state causes:**
- Neighbor address incorrect in NBMA neighbor statement
- Layer 2 circuit down (PVC not established, DLCI incorrect)
- Unicast hellos not reaching peer — routing or switching issue in underlay
- Neighbor not configured for this network on its side

**Note:** Attempt state is never seen on broadcast or point-to-point networks.

### Init

**Definition:** A hello packet has been received from the neighbor, but
bidirectional communication has not been confirmed. The received hello does
not contain this router's Router ID in the neighbor list.

**Entry conditions:**
- HelloReceived event in Down or Attempt state
- This router sees the neighbor's hello but the neighbor has not yet listed
  this router in its hello's neighbor field

**Exit transitions:**
- **2-WayReceived** → transition to **2-Way** (this router's RID seen in
  neighbor's hello)
- **Dead Interval expires** → back to **Down**

**Stuck-state causes:**
- **One-way communication:** Hellos are arriving from the neighbor, but this
  router's hellos are not reaching the neighbor (or the neighbor is not
  processing them). Causes:
  - Area ID mismatch — both sides must have the same area ID on the shared link
  - Authentication mismatch — type (none/simple/MD5) or key mismatch
  - Hello/Dead interval mismatch — both sides must agree
  - Subnet mismatch — interfaces must be on the same IP subnet
  - MTU issue causing this router's hellos to be too large
  - ACL on neighbor blocking inbound OSPF from this router's IP

**Diagnostic:** If neighbor stays in Init, check that both routers list each
other in their hello packets. One-way hellos are the hallmark of Init stuck
state.

### 2-Way

**Definition:** Bidirectional communication confirmed. Both routers see each
other's Router ID in hello packets. DR/BDR election occurs at this stage on
broadcast and NBMA networks.

**Entry conditions:**
- 2-WayReceived event in Init state (this router's RID appears in neighbor's
  hello)
- Adjacency decision: on broadcast/NBMA, only DR↔DROther and BDR↔DROther
  pairs proceed past 2-Way; DROther↔DROther pairs remain in 2-Way permanently.
  On point-to-point and point-to-multipoint, all neighbors proceed to ExStart.

**Exit transitions:**
- **AdjOK? = True** → transition to **ExStart** (this pair should form a full
  adjacency — at least one side is DR or BDR, or it is a point-to-point link)
- **AdjOK? = False** → stay in **2-Way** (both are DROther on broadcast/NBMA —
  this is normal and not a failure)
- **1-WayReceived** → back to **Init** (neighbor removed this router from its
  hello)
- **Dead Interval expires** → back to **Down**

**Stuck-state causes (when Full is expected but 2-Way persists):**
- DR/BDR election not completing — check OSPF priority values
- Both sides have priority 0 on a broadcast segment — no DR elected, no
  adjacencies form beyond 2-Way
- Race condition after DR failure — BDR should promote but if both neighbors
  have priority 0, no new DR is elected

**Note:** 2-Way between two DROther routers on a broadcast network is
**expected behavior**, not a failure. Only investigate if 2-Way persists
between a router and the segment's DR or BDR.

### ExStart

**Definition:** Master/slave relationship is being negotiated for the database
exchange process. The router with the higher Router ID becomes the master and
controls the DBD sequence numbering.

**Entry conditions:**
- AdjOK? evaluated True in 2-Way state
- Both routers begin sending empty DBD (Database Description) packets with
  the Init, More, and Master bits set

**Exit transitions:**
- **NegotiationDone** → transition to **Exchange** (master/slave agreed, DBD
  sequence number established)
- **AdjOK? = False** → back to **2-Way**
- **Dead Interval expires** → back to **Down**

**Stuck-state causes:**
- **MTU mismatch** — The most common cause of ExStart stuck state. DBD packets
  include the interface MTU. If the receiving router sees a DBD with an MTU
  larger than its own interface MTU, it drops the packet. Both sides keep
  retransmitting DBDs, never completing negotiation.
  - **Fix:** Match MTU on both sides of the link.
  - **Workaround:** `ip ospf mtu-ignore` (Cisco/EOS) disables the MTU check.
    JunOS: no equivalent toggle — must fix MTU at interface level.
- **DBD packet drops:** Interface errors, CRC failures, or QoS dropping OSPF
  packets. DBD retransmissions without progress indicate packet loss.
- **Router ID conflict:** Two neighbors with the same Router ID create
  ambiguity in the negotiation.

**Diagnostic:** ExStart is the most actionable stuck state. First check: compare
MTU on both sides. If MTU matches, check for interface errors and packet drops.

### Exchange

**Definition:** Database Description packets are being exchanged. Each router
sends a summary of its LSDB (LSA headers) to the neighbor. Each side builds a
request list of LSAs it needs from the other.

**Entry conditions:**
- NegotiationDone in ExStart (master/slave agreed)
- The master sends DBD packets; the slave acknowledges each with its own DBD

**Exit transitions:**
- **ExchangeDone** → transition to **Loading** (all DBD packets exchanged,
  request list built)
- **ExchangeDone with empty request list** → transition to **Full** (DBDs
  exchanged and no LSAs needed — LSDSBs already in sync)
- **AdjOK? = False** → back to **2-Way**
- **Dead Interval expires** → back to **Down**

**Stuck-state causes:**
- **LSDB too large:** Very large databases (tens of thousands of LSAs) may
  cause DBD exchange to time out. Reduce area scope or add summarization to
  limit per-area LSDB size.
- **DBD retransmissions:** Lost DBD packets cause retransmissions. The
  RxmtInterval timer (default 5s) controls retransmission frequency. Persistent
  retransmissions indicate unreliable transport or CPU overload.
- **Sequence number mismatch:** If a DBD arrives with an unexpected sequence
  number, the exchange fails. Usually caused by a stale neighbor entry after
  a rapid flap.

### Loading

**Definition:** Link-State Request (LSR) packets are being sent to the neighbor
to request full copies of LSAs identified during Exchange. The neighbor responds
with Link-State Update (LSU) packets. Each received LSA is acknowledged with
Link-State Acknowledgment (LSAck).

**Entry conditions:**
- ExchangeDone in Exchange state with non-empty request list

**Exit transitions:**
- **LoadingDone** → transition to **Full** (all requested LSAs received)
- **AdjOK? = False** → back to **2-Way**
- **Dead Interval expires** → back to **Down**

**Stuck-state causes:**
- **Unstable LSDB:** A neighbor is withdrawing or updating LSAs faster than
  they can be synchronized. The request list keeps changing, preventing
  LoadingDone.
- **LSR timeout:** LSR sent but LSU not received within RxmtInterval. The
  neighbor may be too busy to respond or the LSU is being dropped.
- **Slow link:** On low-bandwidth links, large LSU packets may be delayed.
  Increase RxmtInterval for WAN links.

### Full

**Definition:** Adjacency is fully established. LSDSBs are synchronized. The
neighbor relationship is operational and routes are being calculated via SPF
using the synchronized LSDB.

**Entry conditions:**
- LoadingDone in Loading state (all LSAs received)
- ExchangeDone with empty request list in Exchange state (LSDB already in sync)

**Exit transitions:**
- **KillNbr / LLDown** → back to **Down** (interface failure)
- **InactivityTimer** → back to **Down** (no hellos received within Dead
  Interval)
- **1-WayReceived** → back to **Init** (neighbor removed this router from its
  hello)
- **SeqNumberMismatch** → back to **ExStart** (LSDB resynchronization needed)
- **BadLSReq** → back to **ExStart** (invalid LSR received)

**Causes of leaving Full:**
- Hold timer expiry: hellos not arriving (CPU overload, interface issue, QoS)
- Interface flap: brief link down/up causes KillNbr → Down → re-adjacency
- LSDB corruption: SeqNumberMismatch triggers resync from ExStart
- Process restart: OSPF process clear or crash resets all adjacencies

## DR/BDR Election

On broadcast and NBMA networks, DR (Designated Router) and BDR (Backup DR)
election occurs at the 2-Way stage and directly affects which adjacencies form.

### Election Rules

1. **Priority:** Highest OSPF priority wins. Default priority is 1 (all
   vendors). Priority 0 means the router is ineligible to be DR or BDR.
2. **Router ID tiebreaker:** If priorities are equal, highest Router ID wins.
3. **Non-preemptive:** Once a DR is elected, a new router with higher priority
   does NOT take over. The current DR remains until it fails. This prevents
   unnecessary adjacency churn.
4. **BDR promotion:** When the DR fails, the BDR immediately promotes to DR. A
   new BDR is elected from the remaining routers.

### Adjacency Formation Based on DR Role

| Relationship | Adjacency? | Final State |
|-------------|-----------|-------------|
| DR ↔ DROther | Yes | Full |
| BDR ↔ DROther | Yes | Full |
| DROther ↔ DROther | No | 2-Way (normal) |
| DR ↔ BDR | Yes | Full |
| Point-to-Point (any pair) | Yes | Full |

### DR Election Failures

- All routers with priority 0 → no DR elected → no adjacencies past 2-Way
- DR crash with no BDR → new election occurs but adjacency reform takes time
- Network partition → two DRs elected (split segment) → LSDB inconsistency

## LSDB Synchronization Process

The LSDB sync process uses four packet types after ExStart completes:

### Packet Exchange Sequence

```
ExStart: Empty DBDs with I/M/MS bits (negotiate master/slave)
    ↓
Exchange: DBDs with LSA headers (LSDB summary exchange)
    ↓
Loading: LSR → LSU → LSAck (request missing LSAs, receive updates, acknowledge)
    ↓
Full: Synchronized — ongoing LSU flooding for changes
```

### Packet Types

| Packet | Type | Purpose | Direction |
|--------|------|---------|-----------|
| Hello | 1 | Neighbor discovery, keepalive, DR election | Multicast/Unicast |
| DBD (Database Description) | 2 | LSDB summary exchange (LSA headers) | Unicast (neighbor) |
| LSR (Link-State Request) | 3 | Request full LSA copy | Unicast (neighbor) |
| LSU (Link-State Update) | 4 | Carry full LSA(s) | Unicast/Multicast |
| LSAck (Link-State Ack) | 5 | Acknowledge received LSAs | Unicast/Multicast |

### Flooding Mechanics

- **Intra-area flooding:** LSAs are flooded to all neighbors within the same
  area. Each router that receives a new or updated LSA floods it to all other
  OSPF neighbors (except the one it received it from).
- **DR optimization:** On broadcast networks, routers send LSUs to
  AllDRouters (224.0.0.6). The DR then refloods to AllSPFRouters (224.0.0.5).
  This reduces flooding traffic on multi-access segments.
- **Reliable flooding:** Every LSU must be acknowledged with an LSAck. If an
  LSAck is not received within RxmtInterval, the LSU is retransmitted unicast
  to the non-acknowledging neighbor.

## Timer Reference

| Timer | Purpose | Default | Notes |
|-------|---------|---------|-------|
| HelloInterval | Interval between hello packets | 10s (broadcast/P2P), 30s (NBMA) | Must match all neighbors on segment |
| RouterDeadInterval | Time before declaring neighbor down | 4× HelloInterval (40s or 120s) | Must match all neighbors on segment |
| RxmtInterval | Retransmit interval for LSU/DBD/LSR | 5s | Increase for WAN links |
| InfTransDelay | Estimated LSA propagation delay | 1s | Added to LSA age during flooding |
| LSRefreshTime | Interval for self-originated LSA refresh | 1800s (30min) | Fixed by RFC, not configurable |
| MaxAge | Maximum LSA lifetime | 3600s (60min) | LSAs at MaxAge are flushed |
| MinLSInterval | Minimum time between LSA originations | 5s (varies) | Prevents LSA storms |
| MinLSArrival | Minimum time between accepting same LSA | 1s | Prevents processing storms |
| SPFDelay | Initial delay before SPF run | 200ms (Cisco), varies | Start of SPF throttle |
| SPFHoldTime | Delay between subsequent SPF runs | 5000ms (Cisco), varies | Increases exponentially |

## Event-Driven Transitions Summary

| Event | In State | Transition To | Action |
|-------|----------|---------------|--------|
| HelloReceived | Down | Init | Record neighbor |
| Start (NBMA) | Down | Attempt | Send unicast hello |
| HelloReceived | Attempt | Init | Record neighbor |
| 2-WayReceived | Init | 2-Way | DR/BDR election |
| AdjOK? = True | 2-Way | ExStart | Begin DBD exchange |
| NegotiationDone | ExStart | Exchange | Exchange DBD packets |
| ExchangeDone (LSAs needed) | Exchange | Loading | Send LSRs |
| ExchangeDone (no LSAs) | Exchange | Full | Adjacency complete |
| LoadingDone | Loading | Full | Adjacency complete |
| KillNbr / LLDown | Any | Down | Interface failure |
| InactivityTimer | Any (>Down) | Down | Dead interval expired |
| 1-WayReceived | Full/2-Way | Init | Bidirectionality lost |
| SeqNumberMismatch | Full/Exchange | ExStart | Resync LSDB |
| BadLSReq | Full/Exchange | ExStart | Resync LSDB |
