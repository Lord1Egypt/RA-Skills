<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-FLO — Routing Conventions

**Purpose:** The rules governing how FLO addresses packages, resolves paths, detects markers, and applies routing logic. This is the technical foundation for all routing operations.

---

## 1. Marker-Based Addressing

FLO identifies packages by their **marker files** — non-negotiable filenames that prove a package's output exists.

### Package Marker Registry

| Package | Marker File | Type | Layer |
|---------|-------------|------|-------|
| AI-ILC | `ilc-state.md` | State file | Portfolio |
| AI-PILC | `pilc-state.md` | State file | Portfolio |
| AI-PPM | `ppm-state.md` | State file | Portfolio |
| AI-FLO | `flo-state.md` | State file | Edge |
| AI-ADLC | `adlc-state.md` | State file | Project |
| AI-UXD | `uxd-state.md` | State file | Project |
| AI-POLC | `polc-state.md` | State file | Project |
| AI-DWG | `.kiro/steering/workspace-rules.md` | Generated file | Project |
| AI-GCE | `.compliance-state.json` | Engine state | Project |
| AI-TGE | _(TBD — pending TGE build)_ | — | Project |

### Detection Strategy

1. User provides path → check for marker there
2. Scan common locations: `./`, `./output/`, `./projects/{name}/`, `./portfolio/`
3. If Mode 2/3: check `workspace_ref` paths for remote markers
4. If not found: ask operator

---

## 2. Path Resolution

### Local Paths (Mode 1 and Mode 2 local)

All paths are **relative** to the workspace root:
```
./projects/erp/architecture/adlc-state.md
./projects/erp/ux-design/uxd-state.md
./portfolio/ppm-state.md
```

### Remote Paths (Mode 2 remote and Mode 3)

Remote projects use **absolute paths** or workspace references:
```yaml
workspace_ref: {absolute-workspace-root}\{project-name}\    # Windows
workspace_ref: {absolute-workspace-root}/{project-name}/    # Linux/macOS
```

FLO constructs the full path: `{workspace_ref}/{relative-marker-path}`

### Path Storage Rules

- `flo-state.md` stores the `workspace_ref` per project (absolute for remote, `./` for local)
- Routing log stores relative paths (from the project root) for portability
- Dispatch records store both (workspace_ref + relative, so they're self-contained)

---

## 3. Status Detection

FLO reads the `Status` field from each package's state file to determine position:

| Status Value | Meaning for FLO |
|-------------|-----------------|
| `In Progress` | Project is at this package — no routing action |
| `Complete` | Project has finished this package — eligible for routing to successor |
| `Blocked` | Project is stuck — flag as potential stall |
| `Cancelled` | Project was terminated — remove from active routing |

### Completion Detection Rule

A project is considered "complete at Package X" when:
- The marker file exists AND
- The `Status` field (or equivalent) = `Complete`

FLO does NOT infer completion from other signals (partial output, folder existence, etc.) — only the explicit status field in the marker.

---

## 4. Routing Logic

### Default Route Resolution

```
Given: Project P completed Package X
Do:
  1. Look up X in routing table → find successor(s)
  2. Check project profile for P → remove any skipped packages
  3. Check toggles for P → remove any OFF packages
  4. Remaining successor(s) = routing targets
  5. If fan-out: route to ALL remaining targets in parallel
  6. If fan-in target: run readiness check before routing
  7. Produce handoff instruction for each target
```

### Fan-Out Rules

When routing produces multiple targets (e.g., Project-layer opening → POLC + UXD + ADLC):
- All targets receive the handoff; **AI-POLC leads** as the Project-layer entry (problem/value gradient), with AI-UXD and AI-ADLC concurrent
- Each is tracked independently in `flo-state.md`
- POLC-first is an **advisory information gradient, not a blocking prerequisite** — a project may start ADLC/UXD before POLC completes; they converge at the AI-DWG fan-in

### Fan-In Rules (AI-DWG)

When a target requires multiple predecessor outputs:
- **Default gate = all three feeds complete** (AP + PBP + UXP) before FLO recommends AI-DWG start
- **Proceeding with fewer than three is a user-approved exception** — warn, show each peer's status, obtain explicit approval acknowledging reduced coverage; never auto-proceed on a partial trio
- A feed toggled OFF in the profile is excluded from the gate (not counted as missing)

### Readiness Formula for AI-DWG

```
ALL_READY = (polc-state.md Status=Complete)
        AND (uxd-state.md  Status=Complete)
        AND (adlc-state.md Status=Complete)

If ALL_READY:
  → "Full readiness met. All three feeds available — recommend proceed."
If NOT ALL_READY (1–2 of 3 present, none toggled OFF):
  → "Default gate waits for all three. Show peer statuses + reduced-coverage
     warning. Proceed only with explicit user approval (exception)."
```

> The DWG *capability* still generates from any non-empty subset; this formula governs the **default routing gate**, not DWG's ability to produce from a partial trio.

---

## 5. Project Profile Convention

Each project carries a routing profile stored in `flo-state.md`:

```yaml
profile:
  mode: full | skip | custom
  skip: [AI-UXD]                # Packages bypassed entirely
  toggles:
    - package: AI-POLC
      status: on                 # Currently active
      toggled: null              # Never changed
    - package: AI-UXD
      status: off
      toggled: 2026-06-15
      reason: "Backend service"
      operator: "@maheri"
```

### Profile Rules

1. **Default is "full"** — all canonical packages apply
2. **Skip is permanent for the dispatch** — set at dispatch time; changing later requires a new dispatch or explicit toggle
3. **Toggle is runtime** — can be switched on/off at any time by the operator
4. **Toggle overrides skip** — if a skipped package is toggled ON, it becomes active
5. **Every toggle is logged** — routing log + spine (FLO-D-)

---

## 6. Cross-Layer Communication Rule

| Direction | Mechanism | Example |
|-----------|-----------|---------|
| Same-layer → Same-layer | Direct marker detection | AI-PPM reads `pilc-state.md` directly |
| Portfolio → Project | Via FLO (dispatch down) | AI-PPM → FLO → AI-ADLC |
| Project → Portfolio | Via FLO (roll-up) | AI-ADLC status → FLO → AI-PPM |

**FLO is the ONLY governed cross-layer channel.** Same-layer packages never need FLO.

---

## 7. Routing Log Format

Append-only. Each entry is one row:

```markdown
| # | Timestamp | Project ID | From | To | Type | Trigger | Operator | Notes |
```

### Type Values

| Type | Meaning |
|------|---------|
| `Hop` | Normal routing from A to B |
| `Hold` | Routing paused (fan-in wait or conflict) |
| `Skip` | Package bypassed (profile or toggle) |
| `Override` | Operator changed the default route |
| `Toggle` | Package switched on/off |
| `Cancel` | Project flow terminated |
| `Rework` | Routed backward (quality gate failure) |
| `Dispatch` | New project entered the flow |
| `Escalate` | Conflict/issue escalated to PPM |
| `Auto-resolve` | Timeout expired; fallback rule applied |

---

## 8. Naming Conventions

| Artifact | Pattern | Example |
|----------|---------|---------|
| Dispatch record | `DR-{project-id}.md` | `DR-PRJ-ERP-2026-001.md` |
| Readiness check | `RC-{project-id}.md` | `RC-PRJ-ERP-2026-001.md` |
| Conflict alert | `CA-{project-id}-{NNN}.md` | `CA-PRJ-ERP-2026-001-001.md` |
| Roll-up report | `RU-{YYYY-MM-DD}.md` | `RU-2026-06-15.md` |
| Spine decision | `FLO-D-{NNN}` | `FLO-D-001` |
| Spine issue | `FLO-I-{NNN}` | `FLO-I-001` |

---

*Part of AI-FLO v1.0.0*
