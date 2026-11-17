<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Tier 2: Story Elaboration

**Activation:** User-enabled. Off by default in chain mode (AI-DLC v1 Inception handles story creation). Active by user choice in standalone mode.
**Purpose:** Decompose epics into user stories in the user's chosen format — the full PO authoring function for teams without AI-DLC v1.

---

## Activation Rules

| Context | Tier 2 Status | Rationale |
|---------|:---:|---|
| Chain with AI-DLC v1 (default) | ⬜ OFF | DLC Inception creates stories from epics |
| Chain + user explicitly enables | ✅ ON | User wants PO-quality pre-elaboration before DLC |
| Standalone (user enables) | ✅ ON | No DLC — POLC must produce implementation-ready stories |
| Standalone (user declines) | ⬜ OFF | User produces stories themselves or uses another tool |

**Activation trigger:** User says "elaborate stories" / "write user stories" / "I need stories not just epics" / enables Tier 2 in settings.

**Proactive offer (do NOT wait for the trigger):** POLC does not silently assume the default. At the **Stage 5 gate** (once epics are confirmed) it explicitly asks the user whether to keep Tier 2 OFF (epics are the handoff) or turn it ON now — see `strategy/epic-decomposition.md` Step 5.7 (Q-5T). This makes activation an informed, explicit choice rather than a hidden default.

**On-the-fly toggle:** The Tier 2 decision is reversible at any point in the workflow. If the user turns it ON later (any stage), activate Tier 2, record `Tier 2: active` in `polc-state.md`, and return to the epic-decomposition integration point to elaborate the confirmed epics. If they turn it OFF, stop producing new stories (existing story files are retained, not deleted). Log every flip in the Decision Log.

---

## Story Style Selection (Two-Part Question)

When the user activates Tier 2, POLC asks **two** questions before elaborating:

**Q1: "Do you want me to elaborate user stories?"** (yes / no)
- No → POLC stops at epic level. AI-DLC or the user creates stories later.
- Yes → proceed to Q2.

**Q2: "What story format?"**

| Style | Format | Best for (build method) |
|-------|--------|-------------------------|
| **Classic INVEST** (default) | `As a…, I want…, So that…` + Given/When/Then AC | AI-DLC, freestyle |
| **EARS** | `When {trigger} the {system} shall {response}` + INVEST framing | **Spec-driven development (e.g., GitHub Spec Kit)** |
| **Job Story** | `When {situation}, I want {motivation}, so I can {outcome}` | freestyle, AI-DLC |
| **Freestyle** | Any narrative + AC shape the user prefers | freestyle only |
| **Hybrid** | POLC picks the most natural style per story based on content | freestyle, AI-DLC |

**Why this matters:** The story format affects which downstream build method fits best. Spec-driven runners (Spec Kit) expect **EARS**-style acceptance criteria; AI-DLC and freestyle work with INVEST/G-W-T. POLC records the choice in `polc-state.md` (`Story Style:` field) so AI-DWG can surface a build-method advisory to the developer.

**Default:** If the user doesn't specify, use **Classic INVEST** (widest compatibility). If the user mentions spec-driven build or Spec Kit, recommend **EARS**.

### Hybrid Selection Logic

When the user selects **Hybrid**, POLC reads each story's content and picks the most natural style:
- Functional behavior / system response → EARS
- User-centric goal / persona-driven → Classic INVEST
- Situational motivation / job-to-be-done → Job Story
- Complex/exploratory narrative → Freestyle

Each story is tagged with its chosen style in its front-matter.

### State Recording

`polc-state.md` records both fields:
```yaml
Tier 2: active | inactive
Story Style: invest | ears | job-story | freestyle | hybrid
```

---

## De-Duplication Rule (Chain + Tier 2 Active)

When BOTH AI-POLC Tier 2 AND AI-DLC v1 are in play:
- AI-POLC produces stories first (PO-quality, value-framed)
- AI-DLC v1 Inception may further refine or re-elaborate
- **POLC's stories take precedence** on acceptance criteria and value framing
- **DLC's refinement takes precedence** on implementation decomposition (units of work)
- If DLC produces a story that contradicts POLC's AC → flag for PO review

---

## Story Writing Rules

### INVEST Criteria (applies to ALL styles)

Regardless of format, every story must satisfy INVEST:

| Letter | Criterion | Test |
|:---:|---|---|
| **I** | Independent | Can be developed without depending on another story in the same sprint |
| **N** | Negotiable | Details can be discussed; it's not a rigid spec |
| **V** | Valuable | Delivers value to a user or business stakeholder |
| **E** | Estimable | Team can size it (enough clarity to estimate) |
| **S** | Small | Fits in one sprint (if too big → split) |
| **T** | Testable | Clear criteria for pass/fail |

### Story Format — By Selected Style

**Classic INVEST (default):**
```markdown
## Story: {Title}
**Epic:** EPIC-{NNN}  ·  **Priority:** {rank}  ·  **Style:** invest

### User Story
As a {user role}, I want to {action}, So that {benefit}.

### Acceptance Criteria
**AC1:** {Title}
- Given {precondition}
- When {action}
- Then {expected outcome}
(minimum 3 AC: happy path + edge case + error case)

### Size Estimate
- Points: {N} (or T-shirt: {S|M|L})
```

**EARS (for spec-driven build):**
```markdown
## Story: {Title}
**Epic:** EPIC-{NNN}  ·  **Priority:** {rank}  ·  **Style:** ears

### User Story
As a {user role}, I want to {action}, So that {benefit}.

### Acceptance Criteria (EARS)
**AC1:** When {trigger/condition}, the {system} shall {required response}.
**AC2:** While {state}, the {system} shall {continuous behavior}.
**AC3:** If {error condition}, then the {system} shall {error response}.
(EARS keywords: When / While / Where / If-Then / Ubiquitous "shall")

### Size Estimate
- Points: {N} (or T-shirt: {S|M|L})
```

**Job Story:**
```markdown
## Story: {Title}
**Epic:** EPIC-{NNN}  ·  **Priority:** {rank}  ·  **Style:** job-story

### Job Story
When {situation}, I want to {motivation}, so I can {expected outcome}.

### Acceptance Criteria
(Given/When/Then or EARS — author's choice, testable)

### Size Estimate
- Points: {N}
```

**Freestyle:** Author's preferred narrative + testable AC in any shape. Tag `**Style:** freestyle`.

**Hybrid:** Per-story style chosen by content nature (see Hybrid Selection Logic above). Each story tagged with its actual style.

### Acceptance Criteria Rules (all styles)

- **Minimum 3 AC per story** (happy path + edge case + error case)
- **Format matches selected style** — G/W/T for INVEST/Job Story; `shall`-statements for EARS
- **Each AC must be independently testable** — pass/fail deterministic
- **No implementation language** — describe behavior, not code
- **Measurable where possible** — "response within 2 seconds" not "fast response"

---

## Elaboration Process (Per Epic)

### Step T2.1: Identify Stories From Epic

For each epic, ask: "What are the distinct user-facing behaviors this epic delivers?"

```
EPIC-003: Provider Abstraction Layer
├── Story: Configure payment provider via admin panel
├── Story: Process payment through abstraction (provider-agnostic)
├── Story: Handle provider failover transparently
├── Story: View payment provider health status
└── Story: Switch active provider without downtime
```

### Step T2.2: Write Each Story

Apply the format above. Ensure INVEST compliance for each.

### Step T2.3: Validate Story Set

Per epic:
- [ ] Stories cover all epic acceptance criteria
- [ ] No gaps (epic AC not addressed by any story)
- [ ] No overlaps (two stories addressing the same AC)
- [ ] All stories are independent (can be built in any order within the epic)
- [ ] Total size is reasonable (not 20 stories for an M-sized epic)

### Step T2.4: Check Against DoR

Every story must meet the Definition of Ready (Stage 8) before it's considered sprint-ready:
- [ ] Clear description (WHAT, not HOW)
- [ ] AC defined and testable
- [ ] Goal/epic linkage documented
- [ ] No unresolved blocking dependencies
- [ ] Size estimated

---

## Output Location

Stories are stored under the epic folder:
```
epics/
├── EPIC-001_async-processing.md          ← Epic definition
├── EPIC-001_stories/                     ← Tier 2 output
│   ├── STORY-001-01_configure-async.md
│   ├── STORY-001-02_process-async.md
│   └── STORY-001-03_monitor-async.md
├── EPIC-002_stripe-integration.md
├── EPIC-002_stories/
│   └── ...
```

---

## Interaction With Stage 5

When Tier 2 is active, Stage 5 (Epic Decomposition) gains an additional step:
- After each epic is confirmed → immediately elaborate into stories
- Present stories for user review before moving to next epic
- This makes Stage 5 longer but produces a more complete PBP

---

*Tier 2 detail file for AI-POLC | Loaded when Tier 2 is activated*
