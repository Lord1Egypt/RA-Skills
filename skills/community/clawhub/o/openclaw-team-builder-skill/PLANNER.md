# Planner — Job Analysis & Team Proposal

The Planner receives a task, classifies its domain, and proposes the optimal team composition from all three rosters. This is the first step in any team-builder workflow.

Draws from: Agency's **Senior Project Manager** (spec-to-task methodology) and **Sprint Prioritizer** (prioritization framework).

## Planner Workflow

### Step 1: Classify the Domain

Read the task and identify which domains it touches:

| Domain | Indicators | Primary Roster |
|--------|-----------|----------------|
| Trading / Markets | IG, positions, strategies, backtest, P&L | Core (IG) + Research Lab |
| Engineering / Code | Build, implement, fix, API, database, frontend | Core (CEO pipeline) + Agency Engineering |
| Visual / Creative | Image, design, generate, logo, chart, photo | Core (Artist) + Agency Design |
| Research / Optimization | Experiment, optimize, tune, analyze, iterate | Research Lab + relevant specialists |
| Marketing / Growth | Launch, campaign, content, social, audience | Agency Marketing |
| Operations / Support | Monitor, report, compliance, finance | Agency Support |
| Spatial / Immersive | AR, VR, XR, Vision Pro, spatial | Agency Spatial Computing |
| Multi-domain | Complex project touching 3+ domains | CEO orchestrates, mix all rosters |

### Step 2: Propose the Team

For each classified domain, select the right specialists:

#### Small Task (1-3 agents, Micro mode)
- One primary specialist from the relevant division
- Evidence Collector or Reality Checker for review
- CEO oversight if cross-domain

#### Medium Task (5-10 agents, Sprint mode)
- Domain specialist team (2-4 from relevant divisions)
- Senior PM for scoping
- Evidence Collector + Reality Checker for QA
- CEO as orchestrator

#### Large Project (10+ agents, Full mode)
- Full NEXUS pipeline activation
- Agents Orchestrator or CEO as controller
- Specialists from multiple divisions
- Complete QA team
- Support division for operations

### Step 3: Define the Activation Order

Specialists activate in phases, not all at once:

```
Phase 1: SCOPE
  → Senior PM breaks the task into sub-tasks with acceptance criteria
  → Sprint Prioritizer orders by impact and dependencies

Phase 2: BUILD
  → Domain specialists execute sub-tasks
  → Dev↔QA loops: specialist implements → Evidence Collector validates
  → Maximum 3 retries per sub-task before escalation

Phase 3: REVIEW
  → Evidence Collector does first-pass QA on each deliverable
  → Reality Checker does final production-readiness assessment
  → CEO gives final sign-off

Phase 4: DELIVER
  → Results compiled and presented
  → Experiment ledger saved (if Research Lab was involved)
  → Lessons learned documented
```

### Step 4: Output the Team Roster

Format the proposal as:

```
## Team Proposal

### Task
[One-line task description]

### Classification
- Domain: [Primary domain]
- Mode: [Micro / Sprint / Full]
- Estimated effort: [Time estimate]

### Proposed Team

| Role | Agent | Roster | Activation Phase |
|------|-------|--------|-----------------|
| Leader | CEO | Core | Phase 1 |
| Planner | Senior PM | Agency PM | Phase 1 |
| [Role] | [Agent] | [Roster] | Phase [N] |
| QA | Evidence Collector | Agency Testing | Phase 3 |
| Gate | Reality Checker | Agency Testing | Phase 3 |

### Execution Plan
1. [Phase 1 actions]
2. [Phase 2 actions]
3. [Phase 3 actions]

### Handoff Chain
[Agent A] → [Agent B] → [Agent C] → [Reviewer]

### Risks
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]
```

## Example: Trading Chart Analysis Task

**Task**: "Analyze this silver futures chart, identify patterns, and suggest entry points"

```
## Team Proposal

### Task
Analyze silver futures chart for patterns and entry points

### Classification
- Domain: Trading + Visual Analysis
- Mode: Micro
- Estimated effort: 1-2 hours

### Proposed Team

| Role | Agent | Roster | Activation Phase |
|------|-------|--------|-----------------|
| Market Context | IG | Core | Phase 1 |
| Image Analysis | Artist | Core | Phase 2 |
| Pattern Iteration | Research Lab | Research | Phase 2 |
| Review | Evidence Collector | Agency Testing | Phase 3 |

### Execution Plan
1. IG provides live market data + historical context for silver
2. Artist analyzes chart image, identifies visual patterns
3. Research Lab runs iterative analysis loop on pattern detection
4. Evidence Collector validates findings against actual market data

### Handoff Chain
IG (context) → Artist (analysis) → Research Lab (iteration) → Evidence Collector (validation)
```

## Example: Full Dashboard Feature

**Task**: "Build a new portfolio allocation view with pie charts and rebalancing suggestions"

```
## Team Proposal

### Task
Build portfolio allocation view with pie charts and rebalancing

### Classification
- Domain: Engineering + Trading + Visual
- Mode: Sprint
- Estimated effort: 1-2 weeks

### Proposed Team

| Role | Agent | Roster | Activation Phase |
|------|-------|--------|-----------------|
| Leader | CEO | Core | Phase 1 |
| Scoping | Senior PM | Agency PM | Phase 1 |
| UX Design | UX Architect | Agency Design | Phase 1 |
| Frontend | Frontend Developer | Agency Engineering | Phase 2 |
| Data | IG | Core | Phase 2 |
| Visuals | Artist | Core | Phase 2 |
| QA | Evidence Collector | Agency Testing | Phase 3 |
| Gate | Reality Checker | Agency Testing | Phase 3 |

### Execution Plan
1. Senior PM breaks into tasks; UX Architect creates wireframes
2. Frontend Developer builds the UI; IG provides portfolio data; Artist generates chart visuals
3. Evidence Collector screenshots every viewport; Reality Checker certifies production readiness

### Risks
- Portfolio data format may need transformation (IG → chart library)
- Pie chart library selection — recommend using existing dashboard charting stack
```
