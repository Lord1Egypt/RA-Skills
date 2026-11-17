# How Depth Levels Work

**Purpose:** Explains the three-tier adaptive depth system that calibrates every AI-* lifecycle package's output to match project complexity — producing streamlined deliverables for simple projects and comprehensive analysis for complex ones.

---

## What Depth Levels Are

Every lifecycle package in the AI-* Family uses three depth levels to adapt its behavior to project complexity. The workflow adapts to the project — not the other way around.

```
                    SIMPLE                  NORMAL                 COMPLEX
                 ┌───────────┐         ┌───────────┐         ┌───────────┐
                 │  MINIMAL  │         │ STANDARD  │         │COMPREHEN- │
                 │           │         │           │         │   SIVE    │
                 │ Short docs│         │ Full docs │         │ Deep docs │
                 │ 0-2 Q's   │         │ 2-5 Q's   │         │ 5-10 Q's  │
                 │ 1 cycle   │         │ 1-2 cycles│         │ 2-3 cycles│
                 │ Brief opts│         │ 2-3 opts  │         │ 3-5 opts  │
                 └───────────┘         └───────────┘         └───────────┘
                     │                      │                      │
                     ▼                      ▼                      ▼
              Streamlined PIP       Full PIP / AP        Detailed PIP / AP
              5-8 pages total      20-40 pages total     50-80 pages total
```

**Key principle:** Three levels. No more, no fewer. Every package uses the same three names. Depth is assessed once (early in the workflow) and applies to all subsequent stages.

---

## How Depth Is Assessed

### Assessment Point

Depth is determined during the early intake stages:
- **AI-PILC:** Stage 2 (Source Document Ingestion) — based on source completeness + estimated complexity
- **AI-ADLC:** Stage 2 (Requirements Ingestion) — based on input completeness + system complexity

### Complexity Factors (5-8 per package)

Each package defines factors that drive depth. Example for AI-PILC:

| Factor | Low (1) | Medium (2) | High (3) |
|--------|---------|-----------|----------|
| Scale | Small team, single department | Cross-department, multiple teams | Enterprise-wide, global |
| Stakeholder count | ≤5 | 6-15 | 16+ |
| Technical risk | Proven approach | Some unknowns | Novel technology |
| Regulatory requirements | None | Standard compliance | Heavily regulated |
| Integration complexity | ≤2 external systems | 3-5 | 6+ |

### Scoring and Thresholds

Sum all factors and compare against thresholds:

| Score Range (for 5 factors) | Depth Level |
|:---------------------------:|:-----------:|
| 5-8 | Minimal |
| 9-12 | Standard |
| 13-15 | Comprehensive |

### User Override

The AI presents its assessment and recommended depth. The user can:
- Accept the recommendation
- Override to a different level (e.g., "Make this comprehensive even though it scores as standard")
- Adjust specific factors they disagree with

---

## What Changes at Each Depth Level

### Document Length

| Artifact Type | Minimal | Standard | Comprehensive |
|--------------|:-------:|:--------:|:-------------:|
| Analysis reports | 1-3 pages | 5-10 pages | 10-20 pages |
| Templates/forms | Concise | Full | Detailed + appendices |
| Options analysis | Brief or skip | 2-3 options | 3-5 options with deep comparison |
| Diagrams | Optional | 1 per stage | Multiple per stage |

### Interaction Depth

| Aspect | Minimal | Standard | Comprehensive |
|--------|:-------:|:--------:|:-------------:|
| Questions per stage | 0-2 | 2-5 | 5-10 |
| Iteration cycles | 1 | 1-2 | 2-3 |
| Options presented | Skip or brief | 2-3 options | 3-5 with trade-off matrices |
| Cross-references | Light | Standard | Exhaustive traceability |

### Gate Behavior

| Aspect | Minimal | Standard | Comprehensive |
|--------|:-------:|:--------:|:-------------:|
| Gate formality | Auto-proceed (simple confirm) | Standard gate format | Formal gate with checklist |
| Review depth | Summary only | Summary + key items | Full artifact review |
| Stakeholder involvement | Single approver | Primary + 1 | Multiple stakeholders |

---

## Per-Stage Depth Adaptation

Every stage detail file in a package includes a "Depth Adaptation" section that specifies how behavior varies:

```markdown
## Depth Adaptation

| Aspect | Minimal | Standard | Comprehensive |
|--------|---------|----------|---------------|
| Risk identification | 5-8 risks | 10-15 risks | 15-25 risks |
| Mitigation detail | One-liner | Brief paragraph | Full mitigation plan |
| Scoring | Quick assessment | Standard scoring | Detailed scoring + sensitivity |
| Output format | Brief table | Template-driven | Extended with appendices |
```

This ensures depth adaptation is EXPLICIT and consistent — not improvised at runtime.

---

## Depth Propagation Through the Chain

Depth determined in one package influences successors:

| Predecessor | Successor | Propagation |
|------------|-----------|-------------|
| AI-PILC (Standard) | AI-POLC | Reads `Workflow Depth: Standard` from `pilc-state.md` → calibrates to Standard |
| AI-POLC (Standard) | AI-UXD | Reads depth from `polc-state.md` → calibrates to Standard |
| AI-UXD (Standard) | AI-ADLC | Reads depth from `uxd-state.md` → calibrates to Standard |
| AI-ADLC (Comprehensive) | AI-DWG | Comprehensive AP → more conditional steering files generated, deeper operational docs |
| AI-DWG (Standard workspace) | AI-GCE | Standard workspace → Standard derivation depth |

The successor is not bound by predecessor depth — but uses it as a starting calibration. A comprehensive PIP might result in a minimal architecture if the technical complexity is low.

---

## Package-Specific Depth Indicators

### AI-PILC Depth Drivers

| Factor | Drives |
|--------|--------|
| Source completeness | How many questions needed (complete source = fewer questions) |
| Stakeholder count | Depth of stakeholder analysis and communication planning |
| Regulatory weight | Depth of governance and compliance sections |
| Budget scale | Depth of financial analysis in business case |

### AI-ADLC Depth Drivers

| Factor | Drives |
|--------|--------|
| System complexity (component count) | C4 diagram detail, component design depth |
| Integration density | Integration architecture thoroughness |
| Security constraints | Security architecture depth (basic → exhaustive) |
| Team novelty | How much context/reasoning is provided in ADRs |

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Exactly three levels (not two, not five) | Two is too coarse (no middle ground); five creates decision paralysis |
| Same names across all packages | Consistency — users learn the system once |
| Assessed once, applied throughout | Prevents inconsistent depth within a single workflow run |
| User can override | AI might misjudge complexity — user has final authority |
| Propagated to successors | Prevents jarring depth mismatches in the chain |

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|-------------|----------------|
| "Minimal" means skip stages | Depth affects HOW stages run — not WHETHER they run |
| Changing depth mid-workflow | Creates inconsistent artifact quality within one package |
| Ignoring depth in templates | Templates must have depth-specific guidance |
| "Comprehensive for everything" | Over-engineering simple projects wastes time |
| "Minimal for everything" | Under-specifying complex projects causes execution failures |

---

## Related Documents

| Document | Location |
|----------|----------|
| AI-PILC core workflow (depth section) | `ai-pilc/ai-pilc-rules/core-workflow.md` |
| AI-ADLC core workflow (depth section) | `ai-adlc/ai-adlc-rules/core-workflow.md` |
| AI-DWG depth levels | `ai-dwg/ai-dwg-rules/core-generator.md` (Depth Levels table) |
| AI-GCE depth levels | `ai-gce/ai-gce-rules/core-generator.md` (Depth Levels table) |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
