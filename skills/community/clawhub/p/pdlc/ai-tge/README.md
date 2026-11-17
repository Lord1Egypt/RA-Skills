# AI-TGE (AI-Driven Test Governance Engine)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**License:** Apache 2.0 with Attribution Addendum — See `LICENSE` and `NOTICE`

---

## The AI-* PDLC Family

AI-TGE is part of **AIFLC** (AI Full Life Cycle) — the AI-* PDLC Family of injectable workflow packages.

The family is organized into two **layers** joined by a **router on the edge**: the
Portfolio layer reasons across MANY projects; the Project layer executes ONE project.

```
╔════════════════ PORTFOLIO LAYER · scope = MANY projects ════════════════╗

   (optional)
    AI-ILC  ⇢  AI-PILC  ⇢  AI-PPM
    Decide it   Initiate it   Govern it (portfolio of N projects)

╚═════════════════════════════════╤═══════════════════════════════════════╝
                                   │
                                AI-FLO   Route it — package-to-package
                                   │     flow on the edge between layers
╔════════════════ PROJECT LAYER · scope = ONE project ════════════════════╗

    AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► AI-DLC v1 (build) ¹
    Own it      Design UX   Design it   Prepare it       ▲
                                                         │
                        AI-POLC ⇄ AI-DLC v1 (back-and-forth)┘
                AI-DLC v1 ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC v1 (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC v1 = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-POLC** ³ | Interactive workflow (lifecycle) | PIP | Product Backlog Package (PBP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP + PBP | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | PIP + PBP + UXP | Architecture Package (AP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC v1** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POLC) | Working Software |

> ¹ **AI-DLC v1** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC v1 consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ All packages in this table are **built**. AI-PPM (portfolio engine), AI-FLO (router), AI-POLC (product ownership lifecycle), and AI-UXD (UX design lifecycle) were the last four — completed June 2026. Within the Project layer, **AI-POLC, AI-UXD, and AI-ADLC run sequentially** (POLC→UXD→ADLC) — each feeds the next, culminating at AI-DWG which receives all three outputs (AP + PBP + UXP). **AI-GCE and AI-TGE run alongside AI-DLC v1** as continuous quality engines; **AI-POLC ⇄ AI-DLC v1** exchange backlog/acceptance throughout delivery; and **AI-DLC v1 runtime feedback flows back to both AI-UXD and AI-POLC**. Feedback loops (ADLC→POLC cost/risk, ADLC→UXD constraints) provide iterative refinement without changing the forward sequence.

> **AI-DFE** ([Data Fabric Engine](../ai-dfe/)) is a family-scoped **companion** — it gathers data from all packages and distributes structured JSON for dashboards and status roll-ups. It runs alongside the chain rather than as a linear step, so it is not shown as a chain row above.

---

## What is AI-TGE?

AI-TGE is an injectable test governance engine that reads architecture decisions (from AI-ADLC) and a development workspace (from AI-DWG), derives a structured test governance layer — strategy, register, coverage tracking, risk scoring — and continuously observes AI-DLC v1 execution to maintain test accountability.

It is the first **companion package** in the AI-* Family. Unlike sequential packages that sit in a linear handoff chain, AI-TGE runs **alongside** AI-DLC v1 together with AI-GCE as a continuous quality engine. It does not produce output for a downstream package — it feeds findings back into project quality.

**Metaphor:** A test governance inspector. It reads everything the architecture promised — API contracts, security decisions, integration maps, component designs — and builds a register of tests that MUST exist to verify those promises were kept. Then it watches the build, tracking what gets tested and what doesn't, scoring the risk of every gap.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Hybrid Engine** | Dual-mode operation: Strategy (derive what to test) + Observation (track what gets tested) |
| **Architecture-Driven** | Test requirements derived from architectural commitments, not invented ad-hoc |
| **Two-Source Model** | Architecture-derived requirements + universal baseline minimums — coverage even when AP is thin |
| **Risk-First Prioritization** | Missing tests scored by 4 factors (Architectural Risk × Blast Radius × Logic Complexity × Change Frequency) |
| **ISTQB-Aligned Taxonomy** | Three-dimensional classification: Level × Type × Technique |
| **Brownfield First-Class** | Existing projects with existing tests get assessment (map → gap → prioritize), not rejection |
| **Non-Destructive** | Reconciliation proposes changes; never auto-applies. Overrides mark, never delete. |
| **Adaptive Input** | Works with whatever exists — full chain, AP only, brownfield, or observation only |
| **Commitment-Based Coverage** | Measures "did we test what we designed?" — not just lines-of-code |
| **Silent When Complete** | Only speaks when gaps exist — no noise when coverage is full |
| **Injectable** | Drop into any workspace and activate — no project-specific setup |
| **Platform-Agnostic** | Works with Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, GitHub Copilot |

---

## What It Produces

All artifacts are generated under `.governance/test/` in the workspace root:

| Artifact | Purpose |
|----------|---------|
| `tge-state.md` | Engine state + progress tracking (marker file) |
| `test-strategy.md` | Test approach, pyramid ratios, tools, coverage goals |
| `test-register.md` | Master list: commitment → required test → status |
| `coverage-report.md` | Multi-view coverage analysis (by commitment, component, type, risk) |
| `debt-scorecard.md` | Prioritized missing tests ranked by architectural risk |
| `defect-log.md` | Structured defect tracking linked to stories/components |

---

## Dual-Mode Operation

### Strategy Phase (Derive what to test)

```
🔵 Stage 1:  Workspace Detection     →  Detect inputs, determine mode and depth
🔵 Stage 2:  Architecture Reading    →  Read AP commitments, DW stack, DLC stories
🔵 Stage 3:  Test Requirement Derivation  →  Two-source: AP-derived + baseline
🔵 Stage 4:  Brownfield Assessment   →  Map existing tests to register (conditional)
🔵 Stage 5:  Test Strategy Generation →  Pyramid, tools, goals, data strategy
🔵 Stage 6:  Risk Scoring            →  Score every missing test by 4 risk factors
```

### Observation Phase (Track what gets tested)

```
🟢 Stage 7:  State Observation       →  Watch AI-DLC v1 progress, update register
🟢 Stage 8:  Story Acceptance Mapping →  Map acceptance criteria to tests (conditional)
🟢 Stage 9:  Coverage Reporting      →  Multi-view coverage analysis
🟢 Stage 10: Architecture Reconciliation →  Detect AP changes, propose updates (conditional)
🟢 Stage 11: Defect Logging          →  Structured defect capture (conditional)
🟢 Stage 12: Debt Reassessment       →  Re-score priorities as context changes
```

---

## Input Modes (Automatic Detection)

AI-TGE adapts to what exists. It never requires the full chain to have run.

| Mode | What Exists | Behavior |
|------|------------|----------|
| **Full Chain** | AP + DW + aidlc-docs (AI-DLC v1 running) | Full strategy + observation |
| **Architecture Only** | AP (from AI-ADLC) but no DW or DLC | Strategy mode only — derive register from AP |
| **Brownfield** | Existing project with existing tests (no AP) | Assessment mode — map tests, identify gaps |
| **Observation Only** | Active AI-DLC v1 with aidlc-docs but no prior TGE run | Jump to observation — register as you go |

**Standalone Usage (OR-input):** AI-TGE never blocks on a missing predecessor. AP alone produces architecture-derived strategy. Existing tests alone produce brownfield assessment. Running AI-DLC v1 alone produces observation-only tracking. Each input is additive enrichment — its absence reduces scope but never halts the engine. You do NOT need to run AI-PILC, AI-ADLC, or AI-DWG first if you have existing code with tests to assess.

---

## Adaptive Depth

AI-TGE calibrates its depth based on project complexity (5 factors scored 1-5):

| Depth | Score Range | Behavior |
|-------|:-----------:|----------|
| **Minimal** | 5–10 | Strategy + register only |
| **Standard** | 11–18 | + coverage reports + debt scoring + brownfield |
| **Comprehensive** | 19–25 | + full traceability + reconciliation + story mapping |

You can override the depth at any time: "Change depth to Comprehensive"

---

## Risk Scoring

Not all missing tests are equal. Each is scored on 4 factors (1–5 each):

| Factor | What It Measures |
|--------|-----------------|
| **Architectural Risk** | Impact if this goes untested |
| **Blast Radius** | How many things break if this fails |
| **Logic Complexity** | How likely a bug exists here |
| **Change Frequency** | How often this code changes |

**Composite:** Risk × Blast × Complexity × Frequency = 1–625

| Bucket | Score | Action |
|--------|:-----:|--------|
| **Critical** | 400–625 | Test immediately |
| **High** | 150–399 | Test within current sprint |
| **Medium** | 50–149 | Test within next 2 sprints |
| **Low** | 1–49 | Test when convenient |

---

## Session Continuity

AI-TGE supports multi-session workflows:

- Progress is saved in `.governance/test/tge-state.md` after every stage
- On new session start, the engine detects existing state and offers to resume
- You can safely close and return at any time
- All register entries, coverage data, and risk scores are preserved

---

## Activation

**Explicit key:** type `_TGE_` in any prompt to activate AI-TGE unambiguously — even when other AI-* packages share the workspace. The status key `_ACTIVE_` reports which package is currently active. A package switch never happens without your explicit key or confirmation, and any switch is announced on the first line of the response (`Active package: AI-TGE`). See [`../TRIGGER_KEYS_REFERENCE.md`](../TRIGGER_KEYS_REFERENCE.md) for the full family key table.

---

## Installation

1. Download or clone this repository
2. The package contains two key directories:
   - `ai-tge-rules/` — the core engine (always loaded by the AI)
   - `ai-tge-rule-details/` — phase details and templates (loaded on demand)
3. Follow the platform-specific instructions in [setup/INSTALL.md](./setup/INSTALL.md)

---

## Usage

1. Open your workspace in your IDE with the AI assistant active
2. Start a chat and say:

   ```
   Using AI-TGE, derive a test governance strategy for this project
   ```

   Or for brownfield:

   ```
   Using AI-TGE, assess my existing test coverage against the architecture
   ```

3. The engine activates, detects your input mode, and guides you from there
4. Review and approve the test strategy and register at gates
5. During development, invoke observation: "Check test coverage now"
6. All artifacts are generated in `.governance/test/`

---

## Boundary Statement

**AI-TGE is NOT:**
- A test runner (doesn't execute tests)
- A test writer (doesn't generate test code)
- A CI/CD tool (doesn't connect to pipelines)
- A replacement for AI-GCE (GCE governs code compliance; TGE governs test completeness)
- A replacement for AI-DLC v1's Build-and-Test stage (that generates test instructions; TGE governs whether those instructions are sufficient)

**AI-TGE IS:**
- A test governance engine that knows what tests SHOULD exist
- A coverage tracker that measures architectural commitment verification
- A risk scorer that prioritizes which missing tests matter most
- An observer that watches the build and maintains test accountability

---

## Differences from AI-GCE

| Aspect | AI-GCE | AI-TGE |
|--------|--------|--------|
| **Domain** | Code compliance & governance rules | Test completeness & coverage governance |
| **Question** | "Does the code follow the rules?" | "Do tests exist for what was designed?" |
| **Mechanism** | Hooks + rules that enforce standards | Register + risk scoring that tracks gaps |
| **Trigger** | File changes (automatic) | User invocation + DLC state observation |
| **Output** | Compliance log, enforcement actions | Test register, coverage report, debt scorecard |
| **Overlap** | None — different concerns | None — complementary quality engines |

---

## File Structure

```
ai-tge/
├── README.md                          ← This file
├── LICENSE                            ← Apache 2.0 (unmodified)
├── NOTICE                             ← Attribution requirement
├── ai-tge-rules/
│   └── core-engine.md                 ← Master orchestration (always loaded)
├── ai-tge-rule-details/
│   ├── common/
│   │   ├── process-overview.md        ← High-level process map
│   │   ├── session-continuity.md      ← Resume/state management rules
│   │   ├── question-format-guide.md   ← Structured question formatting
│   │   ├── content-validation.md      ← Deliverable quality checks
│   │   ├── welcome-message.md         ← One-time welcome display
│   │   ├── test-taxonomy.md           ← ISTQB-based classification
│   │   └── two-source-model.md        ← Architecture + baseline derivation
│   ├── strategy/                      ← Phase 1 stage details (Stages 1-6)
│   │   ├── workspace-detection.md     ← Stage 1: Detect inputs, mode, depth
│   │   ├── architecture-reading.md    ← Stage 2: Read AP commitments
│   │   ├── test-requirement-derivation.md ← Stage 3: Two-source derivation
│   │   ├── brownfield-assessment.md   ← Stage 4: Map existing tests
│   │   ├── test-strategy-generation.md ← Stage 5: Pyramid, tools, goals
│   │   └── risk-scoring.md            ← Stage 6: 4-factor risk scoring
│   ├── observation/                   ← Phase 2 stage details (Stages 7-12)
│   │   ├── state-observation.md       ← Stage 7: Watch DLC progress
│   │   ├── story-acceptance-mapping.md ← Stage 8: AC → test mapping
│   │   ├── coverage-reporting.md      ← Stage 9: Multi-view analysis
│   │   ├── architecture-reconciliation.md ← Stage 10: AP change detection
│   │   ├── defect-logging.md          ← Stage 11: Structured defect capture
│   │   └── debt-reassessment.md       ← Stage 12: Re-score priorities
│   └── templates/
│       ├── test-strategy.md           ← Test strategy output template
│       ├── test-register.md           ← Test register output template
│       ├── coverage-report.md         ← Coverage report output template
│       ├── debt-scorecard.md          ← Debt scorecard output template
│       ├── defect-log.md              ← Defect log output template
│       ├── tge-state.md               ← Engine state marker template
│       ├── management-framework.md    ← Governance spine contribution
│       ├── quality-dashboard-template.md ← TGE quality dashboard
│       └── agents/
│           ├── test-governance-agent.md   ← TGV__ agent template
│           ├── coverage-review-agent.md   ← CVR__ agent template
│           ├── shortcut-rules-block.md    ← Shortcut trigger definitions
│           └── agent-guide.md             ← Agent installation guide
└── setup/
    ├── INSTALL.md                     ← Platform installation instructions (6 platforms)
    └── TEST_MODE_USER_GUIDE.md        ← Testing mode documentation
```

---

## Tenets

1. **Govern, don't write.** Identify what tests must exist — never generate test code.
2. **Architecture-driven.** Derive from commitments, not assumptions.
3. **Risk-aware.** Prioritize by impact, not by count.
4. **Non-destructive.** Propose, don't auto-apply. Mark, don't delete.
5. **Adaptive.** Work with whatever input exists — never block on missing predecessors.
6. **Silent when complete.** Only speak when gaps exist.
7. **Commitment-based.** Measure "did we test what we designed?" — not code coverage percentages.
8. **Observable.** Everything tracked in `.governance/test/` — fully auditable.
9. **Agnostic.** No dependency on specific IDE, model, or vendor.
10. **Professional.** ISTQB-aligned terminology. Quality engineering standards.

---

## Methodology Alignment

AI-TGE draws from:

- **ISTQB** — Test levels, types, and techniques taxonomy
- **IEEE 829** — Test documentation standards (adapted for agile governance)
- **Risk-Based Testing** — Prioritization by architectural and business risk
- **AIDLC** — Adaptive workflow structure and interaction patterns (inspired by [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows))

---

## Contributing

Contributions welcome. When modifying:

- Core engine changes affect all users — test thoroughly
- Stage detail files can be enhanced independently
- Templates can be customized per organization
- Always maintain zero project-specific content in the framework

---

## Author

Created by **Maheri** — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)

Designed to bridge the gap between architecture promises and test accountability — ensuring that what was designed gets tested, and what isn't tested is visible and risk-scored.

---

## License

**Apache License 2.0 with Attribution Addendum**

- **Free to use:** Personal, commercial, educational, and organizational use — all permitted
- **Modify and distribute:** Create derivative works, redistribute, sublicense — all permitted
- **Attribution required:** Any distributed product substantially based on this work must include:

> *"Built on AIFLC by Mohammad Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)"*

- **No warranty:** Provided "AS IS" without warranties of any kind

See `LICENSE` and `NOTICE` in this directory for full terms.

**Copyright:** © 2026 Mohammad Maheri

> **Note:** AI-DLC v1 (Development Life Cycle) is NOT part of the AI-* Family — it is a separate AWS product ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) licensed under MIT-0.

---

*Part of [AIFLC](../README.md) — the AI-* PDLC Family*
