# How AI-FLO Flow Orchestration Works

**Purpose:** Explains how AI-FLO acts as the edge router between the Portfolio and Project layers — detecting workspace topology, building a routing table, carrying dispatch decisions down, relaying status up, coordinating parallel fan-out/fan-in, and flagging conflicts — all while staying advisory and additive to the rest of the family.

---

## What AI-FLO Does

AI-FLO is the nervous system of the AI-* Family. It turns a collection of independent packages into a coordinated pipeline by tracking where every project sits in the chain, carrying decisions to the right place, and surfacing anything that needs a human's attention.

It answers: "Where is each project right now? What's the next hop? Is anything blocked, stalled, or in conflict?"

```
PORTFOLIO LAYER (AI-PPM dispatch authorizations)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-FLO — EDGE ROUTER (sits between the two layers)                  │
│                                                                      │
│  CONFIGURE → ROUTE → MONITOR  (3 phases / 10 stages)                │
│                                                                      │
│  Detects topology · builds routing table · dispatches down ·         │
│  fans out / fans in · tracks position · relays roll-up · flags       │
│  conflicts (flag-and-hold)                                           │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
PROJECT LAYER (AI-ADLC, AI-UXD, AI-POLC → AI-DWG → AI-DLC v1)
        │
        ▲ (status relayed back up to AI-PPM)
```

**Hard boundary:** AI-FLO carries decisions — it does NOT make them. AI-PPM decides what gets built and in what order; the operator decides overrides; AI-FLO routes those decisions and records every hop. It is advisory in v1.0 — it produces routing artifacts for human action, never auto-starting package sessions.

---

## Where AI-FLO Sits: The Edge

Most packages live inside one layer. AI-FLO is different — it sits on the **edge** between two:

- **Portfolio layer** (scope = MANY projects): AI-ILC, AI-PILC, AI-PPM
- **Project layer** (scope = ONE project): AI-ADLC, AI-UXD, AI-POLC, AI-DWG, AI-GCE, AI-TGE, AI-DLC v1

This position is what lets AI-FLO enforce the layered-communication principle: cross-layer messages always travel through AI-FLO, while same-layer messages stay direct.

| Communication | Mechanism |
|---|---|
| AI-PPM reads AI-PILC / AI-ILC output | Direct (same Portfolio layer) |
| AI-PPM dispatches to AI-ADLC / AI-UXD / AI-POLC | **Via AI-FLO** (cross-layer) |
| Project packages report status to AI-PPM | **Via AI-FLO** (cross-layer) |
| AI-ADLC → AI-DWG, AI-POLC → AI-DWG | Direct (same Project layer) |

The reason for the rule is isolation: the Portfolio layer reasons about *many* projects, the Project layer reasons about *one*. Routing all cross-layer traffic through a single edge keeps each layer from having to know the other's internal structure.

---

## The Correlation Key: `projectId`

Every project carries a stable identifier — `projectId` (camelCase) — assigned at initiation by AI-PILC. AI-FLO threads this key through the chain and stamps it on **every routing hop**, so a project can always be traced from its first dispatch to working software.

Example: `PRJ-ACME-2026-001` enters at AI-PILC, gets dispatched to the Project layer, fans out to three design packages, joins at workspace generation — and at each step the routing log records the same `projectId`. When AI-FLO relays status back up to AI-PPM, the portfolio engine recognizes the project by that same key.

Detection is always by marker file (never by parsing prose), keyed on `projectId`.

---

## The Marker File: `flo-state.md`

AI-FLO's own state and marker is `flo-state.md` — a non-negotiable filename. You choose *where* it lives; the file must exist there. It is created in the Configure phase and updated at every routing operation, making it the single source of truth for project positions.

It records:
- Topology mode (1 / 2 / 3)
- One entry per tracked project: `projectId`, workspace reference, current package, status, next hop, priority, dates
- Active toggles (which packages are on/off for each project, with reason)
- Position history (every From → To hop with its trigger)

On resume, AI-FLO reads `flo-state.md` to recover the topology mode and every project's position, then surfaces any pending alerts before handing control back to you.

---

## The Three Topology Modes

AI-FLO detects how your workspaces are arranged before any routing happens, and adapts its scanning accordingly:

| Mode | Name | Arrangement |
|:----:|------|-------------|
| **1** | Co-located | Portfolio and project work live in one workspace (1:1) |
| **2** | Hub-and-spoke | Portfolio lives here; projects live in remote workspaces (1:N) |
| **3** | Portfolio-only | All projects are remote; this workspace tracks them only (1:N distributed) |

Mode is auto-detected by scanning for Portfolio-layer and Project-layer markers — paths are never hardcoded. For Modes 2 and 3, AI-FLO records remote workspace references and updates distributed projects from operator-reported status.

---

## The Three Phases / Ten Stages

### Phase 1: Configure (Stages 1–3)

Scan the workspace, detect topology, build the routing table, and initialize flow state.

| Stage | What Happens |
|:-----:|--------------|
| 1 — Workspace Detection | Detect topology mode, inventory installed packages, find existing projects, create `flo-state.md` |
| 2 — Routing Table Build | Build the canonical routing table, apply per-project profiles + any saved toggles, validate no orphan routes |
| 3 — Flow State Init | Determine each project's current position from package markers, populate `flo-state.md`, start the routing log, produce the route map |

### Phase 2: Route (Stages 4–7)

Execute routing operations — dispatch, fan-out/fan-in, handoff, and exceptions.

| Stage | What Happens |
|:-----:|--------------|
| 4 — Dispatch (Down) | Read AI-PPM dispatch authorizations, create the project entry, route to default targets, produce a dispatch record |
| 5 — Fan-Out / Fan-In | Coordinate sequential routing handoffs and validate presence at join points |
| 6 — Handoff Execution | Produce the handoff instruction (what the successor needs + `projectId` + constraints), update position + history |
| 7 — Exceptions & Overrides | Handle block, cancel, rework, skip, escalate + operator route/toggle/priority overrides |

### Phase 3: Monitor (Stages 8–10)

Track position, relay roll-up, detect conflicts/stalls/health — continuously.

| Stage | What Happens |
|:-----:|--------------|
| 8 — Position Tracking | Scan project markers for progression, detect stalls, refresh the route map |
| 9 — Roll-Up Relay | Compile per-project status into a roll-up report consumable by AI-PPM |
| 10 — Health, Conflicts & Alerts | Detect conflicts (flag-and-hold), stalls, and bottlenecks; alert the operator proactively |

Unlike lifecycle packages that complete and stop, AI-FLO is a **continuous engine**. Projects enter, move through hops, and exit over time — there is no "workflow complete" state.

---

## Sequential Routing and Validation: Coordinating the Project Layer

The Project layer runs sequentially: **AI-POLC → AI-UXD → AI-ADLC → AI-DWG**. Each package feeds the next. AI-FLO routes each handoff as the predecessor completes.

### Sequential Dispatch (Portfolio → Project)

When AI-PPM authorizes a project, AI-FLO dispatches to **AI-POLC** (the entry point of the sequential chain):

```
AI-PPM dispatch ──► AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG
                    (PBP)       (UXP)       (AP)        (workspace)
```

Each step starts when its predecessor completes. AI-FLO routes the next handoff automatically via marker detection.

### Validation Gate at AI-DWG

AI-DWG (workspace generation) is the terminal consumer. By the time AI-ADLC completes, all three inputs (PBP, UXP, AP) are guaranteed present by the sequential model. AI-FLO validates presence before advancing:

```
AI-POLC (PBP) ── completed step ① ──┐
AI-UXD  (UXP) ── completed step ② ──┼── all present ──► AI-DWG
AI-ADLC (AP)  ── completed step ③ ──┘   (sanity check)
```

For brownfield/partial scenarios (where a package was skipped via profile), AI-FLO warns, shows each predecessor's status, and requires explicit user approval to proceed with fewer than three. AI-FLO records presence validation in a readiness check.

---

## Flag-and-Hold: The Conflict Model

Because data flows in both directions — decisions down, telemetry up — the two layers can collide. The Portfolio layer might rebalance a project's priority at the same moment the Project layer reports "this is bigger than expected." AI-FLO never silently picks a winner.

The protocol:

1. **Detect** — compare the timestamps of an up-signal vs. a down-signal for the same `projectId` + field
2. **Flag** — produce a conflict alert showing both signals, their timestamps, and the affected field
3. **Hold** — pause routing for that project (critical conflicts only); never advance or retreat
4. **Alert** — surface to the operator with resolution options
5. **Resume** — the operator resolves; AI-FLO updates state and resumes routing

A conflict on one project never blocks other projects.

### The Anti-Deadlock Guarantee

No hold lasts forever. Every hold carries a configurable timeout with a deterministic fallback resolution, and the operator can force-through at any time:

| Hold Reason | Default Timeout | Fallback if Unresolved |
|-------------|:--------------:|------------------------|
| Signal collision | 5 business days | Escalate; if still silent, upstream-wins |
| Dependency deadlock | 3 business days | Break the highest-priority project free |
| Fan-in (optional feed) | Configurable | Proceed without the optional feed |
| Unresolved conflict | 7 business days | Latest signal wins, logged as auto-resolved |

The authority chain is simple: AI-FLO ships defaults → the operator configures them → the operator always has the final say. Escape hatches like `force`, `dismiss`, and `timeout` are available at any time. Even an automatic timeout resolution is logged with the rule that was applied — nothing happens silently.

---

## Advisory in v1.0

AI-FLO records routing decisions as artifacts for human action. When a project is ready for its next hop, AI-FLO produces a handoff instruction and surfaces it — it does **not** automatically start the next package's session. The human stays in the loop on every transition.

This keeps AI-FLO predictable and auditable: every hop, override, toggle, conflict, and exception lands in the append-only routing log, and governance-relevant events (decisions and issues) also land in the governance spine. Routine hops stay in the log only, so the spine doesn't fill with noise.

---

## Additive, Never a Single Point of Failure

AI-FLO is optional. The family still works without it:

- **Same-layer communication** (e.g., AI-ADLC → AI-DWG) works regardless, via direct marker detection.
- **Cross-layer communication** degrades gracefully to manual coordination — the human bridges the gap by hand.

AI-FLO *adds* coordination; it never becomes a dependency that breaks the chain when absent. Install it when you want automatic position tracking, dispatch relay, and conflict detection; skip it and the packages still hand off through their markers.

---

## Output Artifacts

| Artifact | Purpose | Produced |
|----------|---------|----------|
| `flo-state.md` | Marker + per-project positions | ALWAYS |
| `routing-table.md` | Active routes + per-project profiles | ALWAYS |
| `routing-log.md` | Append-only audit trail of every routing event | ALWAYS |
| Route map | Multi-project flow visualization (in status output) | ALWAYS |
| `dispatch-record.md` | Per-dispatch record (PPM authorization → Project layer) | When AI-PPM dispatches |
| `readiness-check.md` | Fan-in evaluation (which feeds ready / pending) | When fan-in is evaluated |
| `conflict-alert.md` | Flag-and-hold conflict report | When a conflict is detected |
| `roll-up-report.md` | Project status compiled for AI-PPM | On request or schedule |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| Lifecycle of a Project Through the Chain | `knowledge_docs/LIFECYCLE_OF_A_PROJECT_THROUGH_THE_CHAIN.md` |
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |
| How POLC Product Ownership Works | `knowledge_docs/HOW_POLC_PRODUCT_OWNERSHIP_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-06-13 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
