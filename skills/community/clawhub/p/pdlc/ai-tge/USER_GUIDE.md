# AI-TGE — User Guide

**Package:** AI-TGE (AI-Driven Test Governance Engine)
**Version:** 1.0.0
**Audience:** QA Leads, Test Architects, Test Engineers, Senior Developers, Engineering Leads

---

## What is AI-TGE?

AI-TGE is an injectable test governance engine that reasons and writes as a senior QA engineer / test architect. It reads architecture decisions (from AI-ADLC) and a development workspace (from AI-DWG), derives a structured test governance layer — strategy, register, coverage tracking, risk scoring — and continuously observes AI-DLC v1 execution to maintain test accountability. It does NOT write or run tests; it governs whether the right tests exist and surfaces the risk of every gap.

**In one sentence:** AI-TGE is the continuous quality companion that answers *what must be tested, whether it has been, and how much the gaps cost*.

It is the first **companion package** in the AI-* Family. Unlike sequential packages that hand off in a linear chain, AI-TGE runs *alongside* AI-DLC v1 together with AI-GCE as a continuous quality engine — it is not a stage you pass through.

---

## When to Use AI-TGE

| Scenario | AI-TGE helps you... |
|----------|---------------------|
| Starting a build with an architecture in hand | Derive test requirements from every architectural commitment before a line is written |
| Inheriting a codebase with patchy tests | Map existing tests to commitments, expose uncovered and orphaned tests |
| AI-DLC v1 is actively building | Observe progress, register what should be tested, track coverage as units complete |
| Need to know which gaps matter most | Risk-score every missing test by impact and blast radius, not by raw count |
| Architecture changed mid-build | Reconcile the register — register new tests, deprecate removed ones, flag changed contracts |
| Reporting quality to stakeholders | Produce a commitment-based coverage view and quality dashboard, not just a line-coverage number |

---

## How It Works (5 Minutes)

1. **Install** — Copy package files into your IDE's steering folder (see `setup/INSTALL.md`)
2. **Start a session** — Say: *"Using AI-TGE, derive a test governance strategy for this project"*
3. **Let it detect context** — AI-TGE finds your architecture, workspace, and build state, then picks a mode
4. **Approve at strategy gates** — Each Strategy stage produces deliverables requiring your sign-off
5. **Get your governance layer** — Test strategy, register, coverage tracking, and risk-scored debt in `.governance/test/`

---

## Input Modes

AI-TGE detects what you already have and adapts — it never requires the full chain to have run:

| What You Have | Mode | Behavior |
|---------------|------|----------|
| AP + DW + `aidlc-docs/` (AI-DLC v1 running) | Full Chain | Richest context — full strategy derivation + continuous observation |
| Architecture Package only (from AI-ADLC) | Architecture Only | Strategy mode only — derive the register directly from the AP |
| Existing project with existing tests (no AP) | Brownfield | Assessment mode — map existing tests, identify gaps, prioritize |
| Active AI-DLC v1 with `aidlc-docs/` but no prior TGE run | Observation Only | Jump straight to observation — register what should be tested as you go |

**Detection order:** check for `.governance/test/tge-state.md` (resume) → check for the AP marker `adlc-state.md` (full chain or architecture-only) → check for `aidlc-docs/` (observation possible) → check for existing test directories (brownfield) → if none found, ask what you have.

You do NOT need to run AI-PILC, AI-ADLC, or AI-DWG first. AI-TGE reads the AP directly for test derivation (in parallel to AI-DWG), so an architecture package alone is enough to start. Each input is additive enrichment — its absence reduces scope but never halts the engine.

---

## The Workflow (2 Phases, 12 Stages)

### Phase 1: Strategy (Stages 1–6) — *gated*

Determines WHAT must be tested and WHY. Each stage requires your approval before proceeding.

| Stage | What Happens | What You Decide |
|-------|-------------|-----------------|
| 1 — Workspace Detection | Detects inputs, selects mode, scores depth, initializes `tge-state.md` | Confirm mode (Full Chain / Architecture Only / Brownfield / Observation Only) |
| 2 — Architecture Reading | Reads AP commitments, DW tech stack, and `aidlc-docs/` stories into a Commitment Inventory | Confirm "Is this what was designed?" |
| 3 — Test Requirement Derivation | Two-source derivation: AP-derived requirements + universal baseline → Test Register | Confirm "Are these the right tests?" |
| 4 — Brownfield Assessment | (Conditional) Maps existing tests to register entries: covered / uncovered / orphaned | Confirm "Does this match reality?" |
| 5 — Test Strategy Generation | Produces strategy: pyramid ratios, tools, coverage goals, data strategy, entry/exit criteria | Approve the strategy |
| 6 — Risk Scoring | Scores every missing test on 4 factors → Debt Scorecard | Review the prioritized debt |

### Phase 2: Observation (Stages 7–12) — *continuous*

Tracks WHAT gets tested as features are built. Runs autonomously — informs, does not block.

| Stage | What Happens | When |
|-------|-------------|------|
| 7 — State Observation | Reads `aidlc-docs/aidlc-state.md`, checks whether completed units' required tests now exist, updates the register | As AI-DLC v1 completes units |
| 8 — Story Acceptance Mapping | (Conditional) Maps acceptance criteria from user stories to acceptance-test entries | When user stories exist |
| 9 — Coverage Reporting | Multi-view coverage: by commitment, by component, by test type, by risk level | On request or after observation |
| 10 — Architecture Reconciliation | (Conditional) Detects AP changes; registers new tests, deprecates removed, flags changed contracts | When the AP changed since last read |
| 11 — Defect Logging | (Conditional) Structured defect capture linked to test, component, and story | When defects are reported |
| 12 — Debt Reassessment | Re-scores missing tests as context changes; highlights priority shifts | After coverage report or reconciliation |

---

## The Relationship with AI-DLC v1

AI-TGE is a **continuous companion** to AI-DLC v1, not a one-shot handoff and not a sequential stage:

```
AI-ADLC (AP) ──┐
AI-DWG (DW) ───┼──► AI-TGE ──(observes)──► AI-DLC v1 (build)
               │        ▲                        │
               └────────┴──(test accountability)─┘
```

| Direction | What Flows | When |
|-----------|-----------|------|
| ADLC → TGE | Architecture Package (contracts, ADRs, security, integrations, data models, NFRs) | At strategy derivation — read directly, parallel to AI-DWG |
| DWG → TGE | Development workspace (tech stack, frameworks, steering rules) | At strategy generation |
| DLC → TGE | Build progress via `aidlc-docs/aidlc-state.md` (completed units/stages) | Continuously during observation |
| TGE → project | Coverage gaps, risk-scored debt, quality dashboard | Whenever gaps exist |

**Who does what:**
- AI-TGE = *what* must be tested, *whether* it has been, and *how risky* the gaps are
- AI-DLC v1 = *how* the software is built and its tests written
- AI-TGE does NOT write test code, execute tests, or connect to CI/CD
- AI-DLC v1 does NOT decide test sufficiency or score test debt

**Runs alongside AI-GCE:** AI-GCE governs code/process compliance ("does the code follow the rules?"); AI-TGE governs test completeness ("do tests exist for what was designed?"). Complementary, non-overlapping.

---

## Risk Scoring

Not all missing tests are equal. AI-TGE scores every gap on 4 factors (1–5 each) so you fix what matters first:

| Factor | What It Measures |
|--------|-----------------|
| **Architectural Risk** | Impact if this goes untested |
| **Blast Radius** | How many things break if this fails |
| **Logic Complexity** | How likely a bug exists here |
| **Change Frequency** | How often this code changes |

**Composite:** Architectural Risk × Blast Radius × Logic Complexity × Change Frequency = 1–625

| Bucket | Score | Action |
|--------|:-----:|--------|
| **Critical** | 400–625 | Test immediately |
| **High** | 150–399 | Test within current sprint |
| **Medium** | 50–149 | Test within next 2 sprints |
| **Low** | 1–49 | Test when convenient |

---

## Adaptive Depth

AI-TGE auto-calibrates based on project complexity (5 factors scored 1–5: component count, integration count, security surface, data complexity, team size):

| Depth | When Applied | What Changes |
|-------|-------------|--------------|
| **Minimal** | Score 5–10 — simple project, clear scope | Strategy + register only |
| **Standard** | Score 11–18 — typical complexity | + coverage reports + debt scoring + brownfield |
| **Comprehensive** | Score 19–25 — enterprise, multi-team, heavy compliance | + full traceability + reconciliation + story mapping |

Override anytime: *"Change depth to Comprehensive"*

---

## Brownfield Mode

Already have a codebase with tests? AI-TGE doesn't force a restart:

1. **Scan** — Locates existing test directories and files
2. **Map** — Matches found tests to register entries by name, path, and imports
3. **Classify** — Marks each entry covered / uncovered / orphaned (test exists but no matching commitment)
4. **Prioritize** — Risk-scores the uncovered gaps so remediation is ordered, not flat

It maps without modifying — non-destructive by design. Say: *"Using AI-TGE, assess my existing test coverage against the architecture"* to activate brownfield mode.

---

## Governance Agents

After the Strategy phase, AI-TGE installs two governance agents into your workspace automatically — no manual setup:

| Agent | ID | Shortcut | Role |
|-------|----|----------|------|
| `test-governance-agent` | TGE-AG-01 | `TGV__` | On-demand test governance review — derivation, register integrity, coverage status |
| `coverage-review-agent` | TGE-AG-02 | `CVR__` | Coverage-focused review — surfaces gaps and risk-scored debt |

Both agents read `projectId` from `rules/workspace-rules.md` to correlate every finding to your project for an auditable trail. Type the shortcut (e.g., `TGV__`) in any prompt to invoke the agent.

---

## Session Continuity

AI-TGE saves progress in `.governance/test/tge-state.md`. You can:
- Close your session at any time
- Resume later — AI-TGE reads state and picks up where you left off
- Switch depth mid-workflow
- Re-enter observation whenever the build advances ("Check test coverage now")

---

## What You Get (Output Artifacts)

All artifacts are generated under `.governance/test/` in your workspace root:

| Artifact | Purpose |
|----------|---------|
| `tge-state.md` | Engine state + progress tracking (marker file) |
| `test-strategy.md` | Test approach, pyramid ratios, tools, coverage goals |
| `test-register.md` | Master list: commitment → required test → status |
| `coverage-report.md` | Multi-view coverage analysis (by commitment, component, type, risk) |
| `debt-scorecard.md` | Prioritized missing tests ranked by architectural risk |
| `defect-log.md` | Structured defect tracking linked to stories/components |
| `quality-dashboard.md` | Project-facing test quality dashboard for monitoring |

Coverage calculations exclude Deprecated and Overridden entries — they measure what genuinely remains.

---

## Quick Start Examples

**Full chain (richest context):**
```
Using AI-TGE, derive a test governance strategy for this project.
I have an Architecture Package from AI-ADLC and a workspace from AI-DWG.
```

**Architecture only (no workspace yet):**
```
Using AI-TGE, derive test requirements from my architecture package.
AI-DLC v1 hasn't started building yet.
```

**Brownfield (existing tests):**
```
Using AI-TGE, assess my existing test coverage against the architecture.
Show me what's uncovered and rank the gaps by risk.
```

**Observation (build in progress):**
```
Using AI-TGE, check test coverage now.
AI-DLC v1 just completed two more units.
```

---

## Tips for Best Results

1. **Feed it the architecture** — The richer the AP, the more specific the derived tests. Architecture-derived requirements beat baseline-only coverage.
2. **Approve the Commitment Inventory carefully** — Everything downstream traces back to it. A missed commitment is a missed test.
3. **Trust the risk order** — Fix Critical and High gaps first. Raw coverage percentage hides where the real exposure is.
4. **Don't expect it to write tests** — AI-TGE governs; it never generates or runs test code. That boundary is deliberate.
5. **Re-enter observation often** — Coverage is a moving target. Run a check after each batch of completed units.
6. **Let reconciliation propose, not impose** — When the architecture changes, review the proposed register delta; nothing is auto-applied or deleted.

---

## What AI-TGE Is NOT

- NOT a test runner (doesn't execute tests)
- NOT a test writer (doesn't generate test code)
- NOT a CI/CD tool (doesn't connect to pipelines)
- NOT a replacement for AI-GCE (GCE governs code compliance; TGE governs test completeness)
- NOT a replacement for AI-DLC v1's Build-and-Test stage (that generates test instructions; TGE governs whether those instructions are sufficient)

AI-TGE is the **test governance companion** — it answers *what must be tested, whether it has been, and how much each gap costs*.

---

## Platform Support

AI-TGE works on: Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot — plus any AI-assisted IDE that supports steering/rules files via the Universal Setup.

See `setup/INSTALL.md` for detailed platform instructions.

---

*AI-TGE v1.0.0-beta.1 | Part of [AIFLC](../README.md) — the AI-* PDLC Family*
