# How State Files Work

**Purpose:** Explains the state file mechanism that enables session continuity, chain handoff, and workflow tracking across all AI-* Family lifecycle packages.

---

## What State Files Are

Every lifecycle package in the AI-* Family maintains a persistent state file that tracks workflow progress, decisions made, and configuration choices. State files enable three critical capabilities:

1. **Session continuity** — any AI session can resume exactly where the previous one left off
2. **Chain handoff** — successor packages read state to understand predecessor output
3. **Workflow tracking** — auditable record of what happened and when

```
┌─────────────────────────────────────────────────────────────────────┐
│  STATE FILE (e.g., pilc-state.md)                                    │
│                                                                      │
│  Identity:     PRJ-ACME-2026-001                                     │
│  Phase:        PLANNING                                              │
│  Stage:        11 (Scope Definition)                                 │
│  Completed:    Stages 1-10 [with timestamps]                         │
│  Depth:        Standard                                              │
│  Structure:    numbered                                              │
│  Decisions:    6 logged                                              │
│  Extensions:   [DDD Tactical, Microservices]  (AI-ADLC only)         │
│  Status:       In Progress                                           │
│                                                                      │
│  Used by:                                                            │
│  ├── Same package (resume) ← load state, continue from last stage   │
│  └── Successor package (handoff) ← read identity, status, config    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## State File Registry

Each package has its own marker/state file:

| Package | State File | Type | Purpose |
|---------|-----------|------|---------|
| AI-ILC | `ilc-state.md` | Lifecycle state | Tracks idea evaluation progress |
| AI-PILC | `pilc-state.md` | Lifecycle state | Tracks project initiation progress |
| AI-ADLC | `adlc-state.md` | Lifecycle state | Tracks architecture design progress |
| AI-POLC | `polc-state.md` | Lifecycle state | Tracks product ownership progress |
| AI-UXD | `uxd-state.md` | Lifecycle state | Tracks UX design progress |
| AI-DWG | — (no state file) | Generator | Marker is `.kiro/steering/workspace-rules.md` |
| AI-GCE | `.compliance-state.json` | Engine state | Tracks compliance tier, scores, audit dates |

**Note:** Generators (AI-DWG) and engines (AI-GCE) use different marker mechanisms because they don't have multi-phase linear progress to track.

---

## What State Files Contain

### Common Fields (All Lifecycle Packages)

| Field | Purpose | Updated When |
|-------|---------|-------------|
| Project ID | Family-wide correlation key (e.g., `PRJ-ACME-2026-001`) | Set at Stage 1, never changed |
| Project Name | Human-readable identifier | Set at Stage 1 |
| Current Phase | Which phase is active | Every stage transition |
| Current Stage | Which stage is active | Every stage transition |
| Completed Stages | List with timestamps | After each stage gate passes |
| Workflow Depth | Minimal / Standard / Comprehensive | Set at ingestion, rarely changed |
| Output Structure | numbered / flat / custom | Set at Stage 1 |
| Status | In Progress / Complete / Abandoned | At workflow milestones |

### Package-Specific Fields

**AI-PILC adds:**
- Pending Decisions (decisions awaiting stakeholder input)
- Register Counts (how many entries in each management register)
- Source Type (document / verbal / brownfield / ILC brief)

**AI-ADLC adds:**
- Enabled Extensions (which opt-in patterns are active)
- ADR Register (list of all ADRs produced with status)
- Architecture Workbook items (open questions, resolved items)
- Input Mode (Full PIP / Raw Requirements / Brownfield)

**AI-GCE (`.compliance-state.json`):**
- `complianceTier`: Current tier (1, 2, or 3)
- `lastAudit`: Timestamp of last audit run
- `score`: Current compliance percentage
- `nextTierReadiness`: Object tracking readiness criteria
- `applicableRules`: Count of active rules
- `currentPhase`: Project phase for phase-aware enforcement

---

## How Session Continuity Works

When a user returns to continue a workflow:

```
1. AI loads core-workflow.md for the package
2. AI checks for state file in the output directory
3. State file found → parse current position
4. Present resume prompt:

   "Found existing workflow state:
    Project: {name}
    Phase: {phase} — Stage {n} ({stage_name})
    Last activity: {timestamp}
    
    Resume from Stage {n}? [Yes / Start over / Go to different stage]"

5. User confirms → AI loads the relevant stage detail file and continues
```

**Cold resume guarantee:** The state file contains EVERYTHING needed to resume. No context from the previous AI session is required. A completely new session with a completely different AI model can pick up where the last one left off.

---

## How Chain Handoff Uses State Files

Successor packages read specific fields from predecessor state files:

### AI-ADLC reads from `pilc-state.md`:

| Field | What AI-ADLC Does With It |
|-------|---------------------------|
| Project ID | Copies into `adlc-state.md` (correlation key) |
| Status | Must be `Complete` for full PIP handoff |
| Workflow Depth | Calibrates its own depth level accordingly |
| Output Structure | Knows which naming pattern to expect (`01_*.md` vs. flat) |
| Project Name | Uses as default system name |

### AI-DWG reads from `adlc-state.md`:

| Field | What AI-DWG Does With It |
|-------|--------------------------|
| Output Structure | Knows which naming pattern to expect for AP files |
| Enabled Extensions | Triggers extension-enrichment mappings |
| Completed Stages | Confirms AP is complete (or flags partial) |
| ADR Register | Inventory of all decisions to cross-reference |

---

## Update Protocol

State files are updated immediately after EVERY stage completion:

```
Stage N completes successfully
  → User approves gate
  → AI updates state file:
      • Move stage N to "Completed" list with timestamp
      • Advance "Current Stage" to N+1
      • Log any decisions made in this stage
      • Update register counts (if applicable)
  → THEN transition to next stage
```

**Critical rule:** State update happens BEFORE presenting the next stage. If the session crashes between stages, the state reflects the last completed stage — enabling clean resume.

---

## State File Location

State files live alongside the package's output, in the user-chosen output folder:

```
{user-chosen-path}/
├── pilc-state.md           ← AI-PILC state
├── 01_Requirement_Intake_Form.md
├── 02_Requirements_Analysis.md
└── ...
```

For AI-GCE, the state file lives at the workspace root:
```
{workspace-root}/
├── .compliance-state.json  ← AI-GCE state
├── .kiro/
│   ├── hooks/
│   └── steering/
└── .governance/
```

---

## Marker File vs. State File

| Concept | Definition | Example |
|---------|-----------|---------|
| **State file** | Tracks progress within a workflow | `pilc-state.md` with phases, stages, decisions |
| **Marker file** | Enables detection by successor packages | Same file (`pilc-state.md`) — it serves both roles |

For lifecycle packages, the state file IS the marker file. For generators/engines, the marker is a different artifact (e.g., AI-DWG's marker is `workspace-rules.md`, not a state file).

---

## Related Documents

| Document | Location |
|----------|----------|
| AI-PILC session continuity | `ai-pilc/ai-pilc-rule-details/common/session-continuity.md` |
| AI-ADLC session continuity | `ai-adlc/ai-adlc-rule-details/common/session-continuity.md` |
| Chain Handoff (how detection works) | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
