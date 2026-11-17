# Reference Map: AI-DWG Input → Destination Workspace

**Purpose:** Complete lookup table of what AI-DWG reads from each design-time peer input (AI-ADLC, AI-POLC, AI-UXD) and exactly where the result lands in the generated development workspace. Use this to answer "if I run AI-DWG with these inputs, what files will I get and where?"

---

## How to Read This

AI-DWG is a **convergence-point generator**. It accepts any non-empty subset of three peer inputs and generates only the **output clusters** whose input is present:

| Peer Input | Producer | Marker File | Output Cluster |
|-----------|----------|-------------|----------------|
| **AP** — Architecture Package | AI-ADLC | `adlc-state.md` | Technical (steering, configs, source structure) |
| **PBP** — Product Backlog Package | AI-POLC | `polc-state.md` | Product (vision, backlog, traceability, value) |
| **UXP** — UX Design Package | AI-UXD | `uxd-state.md` | UX (design system, navigation, content, theming) |

**Key rules:**
- **One input → one output cluster.** Every generated file traces to exactly one peer input. If that input is absent, its cluster is skipped (with a quality-impact disclosure to you before generation).
- **Conditional within a cluster.** Even when an input is present, some outputs only appear if the input actually contains the relevant artefact (e.g. theming only if the design defined multiple brands or dark mode).
- **Paths shown are relative to the generated dev-workspace root.** Steering files land in `.kiro/steering/`; AI-DLC v1 input documents and operational docs land at the workspace root.

---

## AI-ADLC (AP) → Technical Cluster

Present when `adlc-state.md` is detected.

| AP Source Artifact | Destination File | Type | Always / Conditional |
|--------------------|------------------|------|----------------------|
| Architecture vision + project identity | `.kiro/steering/workspace-rules.md` | Steering (identity) | Always (when ADLC present) |
| Architecture principles | `.kiro/steering/architecture-principles.md` | Steering | Always |
| Technology stack + ADRs | `.kiro/steering/tech-stack.md` + project configs (`.editorconfig`, `.gitignore`, etc.) | Steering + config | Always |
| Security & identity architecture | `.kiro/steering/security-rules.md` | Steering | Always |
| API architecture | `.kiro/steering/api-standards.md` | Steering | Always |
| Data architecture | `.kiro/steering/database-rules.md` | Steering | Always |
| Component design (C4 L3) | `.kiro/steering/module-structure.md` + **`src/` folder structure** | Steering + scaffold | Always |
| Component design (domain) | `.kiro/steering/domain-context.md` | Steering | Always |
| Component design (errors) | `.kiro/steering/error-handling.md` | Steering | Always |
| Naming conventions | `.kiro/steering/naming-conventions.md` | Steering | Always |
| Git/branching strategy | `.kiro/steering/git-workflow.md` | Steering | Always |
| Infrastructure → observability | `.kiro/steering/observability-logging.md` + `observability-sensitive.md` | Steering | Always |
| Infrastructure → CI/CD | CI/CD config files | Config | Always |
| Infrastructure → environment | Environment config files | Config | Always |
| Quality attributes | `.kiro/steering/testing-strategy.md` | Steering | Conditional (skipped if AI-TGE is activated — TGE owns it) |
| Quality attributes (performance) | `.kiro/steering/performance-standards.md` | Steering | Conditional (performance-critical) |
| Integration patterns | `.kiro/steering/resilience-standards.md` | Steering | Conditional (≥3 integrations or Resilience extension) |
| Multi-tenancy ADR | `.kiro/steering/multi-tenancy.md` | Steering | Conditional (multi-tenant) |
| Module ownership | `CODEOWNERS` | Config | Always |
| Tech stack + quality + UXP frontend | `technical-environment.md` | AI-DLC v1 input doc | Always (root) |
| Security rules + a11y baseline + testing | `aidlc-rules/extensions/` | AI-DLC v1 input bundle | Always (root) |
| Active AI-ADLC v1.1 extension (DDD / Microservices / Event Sourcing / Feature Flags) | Extension-specific steering + structure | Steering + scaffold | Conditional (extension active in AP) |

---

## AI-POLC (PBP) → Product Cluster

Present when `polc-state.md` is detected.

| PBP Source Artifact | Destination File | Type | Always / Conditional |
|---------------------|------------------|------|----------------------|
| Product vision (+ UXP personas/journeys if UXD present) | `vision.md` | AI-DLC v1 input doc | Always (when POLC present) |
| Definition of Ready / Done | `DEFINITION_OF_DONE.md` | Quality doc | Always |
| Roadmap + release plan | Planning templates (`sprint-planning.md`, `session-planning.md`) | Templates | Always |
| Risk register + assumption log | `.kiro/steering/scope-and-risks.md` | Steering | Always |
| Traceability linkage | `traceability-matrix.md` (intent → epic → story → release) | Operational doc | Conditional (PBP has traceability artefact) |
| Value & KPI model | `value-metrics.md` (+ KPI relay into observability if ADLC present) | Operational doc | Conditional (PBP has value/KPI artefact) |
| Epic decomposition | `epics-and-backlog.md` + `backlog/EPIC-*.md` (one stub per epic) | Backlog scaffold | Conditional (PBP has epics) |
| Tier 2 INVEST stories (Given/When/Then) | `user-stories.md` + `examples/acceptance/*.feature.md` | Stories + test skeletons | Conditional (POLC Tier 2 was activated) |

---

## AI-UXD (UXP) → UX Cluster

Present when `uxd-state.md` is detected.

| UXP Source Artifact | Destination File | Type | Always / Conditional |
|---------------------|------------------|------|----------------------|
| Design system + design tokens | `.kiro/steering/design-system.md` | Steering | Always (when UXD present) |
| Component / state / pattern inventory | `.kiro/steering/frontend-standards.md` | Steering | Always (also generated if ADLC has UI containers) |
| Wireframe spec + user flows | `ui-implementation-spec.md` | AI-DLC v1 input doc | Always (root) |
| Accessibility baseline (WCAG target) | Relay → AI-GCE `accessibility-compliance` rule + a11y section in `frontend-standards.md` | Relay + steering | Always |
| Personas + user journeys | Enrichment to `vision.md` Target Users section | Enrichment | Conditional (POLC also present) |
| Information architecture (site map, navigation, taxonomy, search) | `.kiro/steering/navigation-structure.md` | Steering | Conditional (UXP has IA) |
| Design QA framework (drift rules, severity) | `.kiro/steering/design-qa.md` (+ relay → AI-GCE `design-fidelity` rule) | Steering + relay | Conditional (UXP has Design QA framework) |
| Voice & tone guidelines | `.kiro/steering/content-guidelines.md` (microcopy + terminology) | Steering | Conditional (UXP has voice & tone) |
| Multi-brand + dark-mode tokens | `.kiro/steering/theming.md` | Steering | Conditional (multiple brands or color modes) |
| i18n / RTL / localization tokens | `.kiro/steering/i18n-standards.md` | Steering | Conditional (more than one locale) |

---

## Always Generated (Regardless of Inputs)

These are produced no matter which inputs are present (a minimal workspace is always coherent):

| Destination File | Type |
|------------------|------|
| `.kiro/steering/workspace-rules.md` | Core rules + identity + Project ID correlation key (minimal version with a single input) |
| Operational docs (`PROJECT_INSTRUCTIONS`, `CONTRIBUTING`, `ONBOARDING`, etc.) | Operational |
| `.github/` PR template | Config |

---

## Destination Layout (Where Things Land)

```
{slug}-workspace/
├── .kiro/steering/          ← all steering files (technical + UX clusters)
│   ├── workspace-rules.md            (always)
│   ├── tech-stack.md … etc.          (IF ADLC)
│   ├── design-system.md              (IF UXD)
│   ├── navigation-structure.md       (IF UXD + IA)
│   ├── content-guidelines.md         (IF UXD + voice & tone)
│   ├── theming.md                    (IF UXD + multi-brand/mode)
│   ├── i18n-standards.md             (IF UXD + multi-locale)
│   ├── design-qa.md                  (IF UXD + Design QA)
│   └── scope-and-risks.md            (IF POLC)
├── vision.md                ← AI-DLC v1 Vision Document (IF POLC)
├── technical-environment.md ← AI-DLC v1 Technical Environment Document (IF ADLC)
├── ui-implementation-spec.md← AI-DLC v1 UI spec (IF UXD)
├── traceability-matrix.md   ← (IF POLC + traceability)
├── value-metrics.md         ← (IF POLC + value/KPIs)
├── epics-and-backlog.md     ← (IF POLC + epics)
├── backlog/EPIC-*.md        ← epic stubs (IF POLC + epics)
├── user-stories.md          ← (IF POLC Tier 2)
├── examples/acceptance/     ← Given/When/Then skeletons (IF POLC Tier 2)
├── DEFINITION_OF_DONE.md    ← (IF POLC or ADLC)
├── aidlc-rules/extensions/  ← AI-DLC v1 extension bundle (IF ADLC security + UXD a11y)
├── CODEOWNERS               ← (IF ADLC)
├── src/                     ← source structure from C4 L3 (IF ADLC)
└── [operational docs, configs, PR template]   (always)
```

---

## Notes on Shared Outputs

Some outputs draw from more than one input — they are still anchored to one **primary** cluster:

| Output | Primary Input | Secondary Contributor |
|--------|---------------|-----------------------|
| `vision.md` | POLC (vision, scope, metrics) | UXD (personas, journeys → Target Users) |
| `technical-environment.md` | ADLC (stack, security, quality) | UXD (frontend patterns, design tokens) |
| `frontend-standards.md` | UXD (component/pattern inventory) | ADLC (UI container architecture) |
| `value-metrics.md` | POLC (KPIs) | ADLC (instrumentation relay into observability) |
| `aidlc-rules/extensions/` | ADLC (security extension) | UXD (accessibility), AI-TGE/DWG (testing) |

When a contributing input is absent, the output is still generated from its primary input; the secondary section is omitted with a note.

---

## Related Documents

| Document | Location |
|----------|----------|
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How Project-Layer Collaboration Works | `knowledge_docs/HOW_PROJECT_LAYER_COLLABORATION_WORKS.md` |
| Reference Map: Conditional Generation Triggers | `knowledge_docs/REFERENCE_MAP_TRIGGERS.md` |
| Reference Map: Marker Files | `knowledge_docs/REFERENCE_MAP_MARKERS.md` |
| Reference Map: Downstream Signals | `knowledge_docs/REFERENCE_MAP_SIGNALS.md` |
| Pattern: Conditional Generation | `knowledge_docs/PATTERN_CONDITIONAL_GENERATION.md` |
| How To Prepare a Development Workspace | `knowledge_docs/HOW_TO_PREPARE_A_DEVELOPMENT_WORKSPACE.md` |

*Knowledge Document | Created: 2026-06-17 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
