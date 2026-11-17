<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 8: Position Tracking

## Purpose

Continuously monitor package state files to detect when projects advance, stall, or regress. Keep `flo-state.md` accurate as the single source of truth for project positions.

---

## Trigger

This stage runs:
- On every session start (resume scan)
- When operator asks `status` or `route map`
- Periodically during active routing sessions
- When explicitly requested: `check positions`

---

## Steps

### Step 1: Scan All Known Project Markers

For each project in `flo-state.md`, read its relevant state files:

```
Position scan: {date}

  PRJ-ERP-2026-001:
    Recorded position: AI-POLC (In Progress)
    Current markers:
      pilc-state.md  → Complete ✅
      adlc-state.md  → Complete ✅
      uxd-state.md   → Not found (toggled OFF)
      polc-state.md  → Complete ✅ ← CHANGED
    
    → Position ADVANCED: AI-POLC → waiting-for-fan-in (DWG)
```

### Step 2: Detect Changes

Compare current marker state against recorded position:

| Change Type | Detection | Action |
|-------------|-----------|--------|
| **Advance** | Package status changed to Complete that matches current position | Update position → next hop; check routing table |
| **Regression** | Package status BEHIND recorded position | Alert (unexpected — possible manual intervention or rework) |
| **Stall** | No change AND days-in-stage > threshold | Flag stall warning |
| **New marker** | State file appears where none existed | Project may have started a new package |

### Step 3: Update Flow State

For each detected change:
- Update `flo-state.md` project entry: Current Package, Status, Next Hop, Last Activity
- Append to Position History
- If advance triggers a routing decision → queue for Stage 6 (Handoff)

### Step 4: Stall Detection

```
Stall check:

  | Project ID | Position | Days | Threshold | Status |
  |------------|----------|:----:|:---------:|--------|
  | PRJ-ERP-2026-001 | AI-DWG | 3 | 7 | ✅ OK |
  | PRJ-CRM-2026-002 | AI-ADLC | 12 | 7 | ⚠️ STALLED |
  | PRJ-MOB-2026-003 | AI-PILC | 2 | 7 | ✅ OK |
```

For stalled projects:
- Flag with stall warning (Info severity first time; Warning if >2x threshold)
- Include in next roll-up report
- Log: FLO-I-{NNN} if first detection

### Step 5: Remote Project Updates (Mode 2/3)

For remote projects, FLO cannot actively scan:
- Display: "Remote projects last updated: {date}. Update now?"
- If operator provides updated status → update `flo-state.md`
- If no update available → mark as "Last known: {date}" (no false stall alerts for remote)

```
Remote project status:

  PRJ-EXT-2026-004 (remote: /path/to/workspace/):
    Last known: AI-ADLC In Progress (reported 2026-06-10)
    Days since update: 5
    
    [U] Update status now | [S] Skip (keep last known)
```

### Step 6: Produce Route Map

On request (`status` or `route map`), generate the visual:

```
📊 Route Map: {date}

  PRJ-ERP-2026-001 (#1):
    PILC ✅ → POLC ✅ → UXD ✅ → ADLC ✅ → [DWG ⚡] → DLC
                                            ↑ all inputs ready

  PRJ-CRM-2026-002 (#2):
    PILC ✅ → POLC ✅ → [UXD ⚡ ⚠️12d] → ADLC → DWG → DLC
                          ↑ stalled

  PRJ-MOB-2026-003 (#3):
    [PILC ⚡] → POLC → UXD → ADLC → DWG → DLC

  Legend: ✅ complete | ⚡ in progress | 🚫 skipped | ⚠️ stalled | ⏸ blocked
  
  Summary: 3 active | 1 stalled | 0 blocked | 0 conflicts
```

---

## Drift Detection (On Resume)

When FLO resumes after being offline:

| Drift Type | Meaning | Action |
|-----------|---------|--------|
| Marker AHEAD of state | Project moved while FLO was offline | Update state (catch up) + log |
| Marker BEHIND state | Unexpected regression | Alert (possible rework or data issue) |
| New markers for unknown project | Someone ran a package without dispatch | Alert (orphan project — add to tracking?) |

```
Drift detected on resume:

  PRJ-ERP-2026-001: Marker advanced (POLC → Complete while FLO offline)
    → State updated. Routing triggered for next hop.
  
  PRJ-CRM-2026-002: No drift. Position unchanged.
```

---

## No Gate

Position tracking is continuous. No explicit approval needed — it's observational. When tracking detects a routing trigger (advance), it queues a handoff (Stage 6) which DOES have a gate.

---

*Part of AI-FLO v1.0.0*
