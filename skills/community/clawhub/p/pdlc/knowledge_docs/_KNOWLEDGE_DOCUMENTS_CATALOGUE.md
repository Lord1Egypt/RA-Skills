# Knowledge Documents Catalogue

**Purpose:** Master registry of all knowledge documents for the AI-* Family — covering technical mechanics (HOW), operational practices (HOW TO), and impact rationale (WHY). Together these form the institutional knowledge base that serves builders, practitioners, and stakeholders.

**Created:** 2026-06-11 | **Updated:** 2026-07-05

---

## Ground Rules

> Ground rules, document types, naming conventions, and content standards are maintained in the steering file:
> **`.kiro/steering/knowledge-docs-rules.md`** (auto-loaded when working in this folder).

---

## Status Legend

| Symbol | Meaning |
|:------:|---------|
| ✅ | Created — document exists |
| ⏸️ | Under review — moved to `_review/` pending decision |
| 📋 | Planned — ready to write (feature is built) |
| 💡 | Future — tied to an idea not yet approved |

---

## Category 1: Package Mechanics (How Packages Work)

How the AI-* packages function internally — their engines, modes, and behaviors.

| # | Document Name | Package(s) | Status |
|---|--------------|------------|:------:|
| 1 | [`HOW_PILC_WORKFLOW_ENGINE_WORKS.md`](HOW_PILC_WORKFLOW_ENGINE_WORKS.md) | AI-PILC | ✅ |
| 2 | [`HOW_ADLC_PROGRESSIVE_DECOMPOSITION_WORKS.md`](HOW_ADLC_PROGRESSIVE_DECOMPOSITION_WORKS.md) | AI-ADLC | ✅ |
| 3 | [`HOW_ADLC_EXTENSIONS_WORK.md`](HOW_ADLC_EXTENSIONS_WORK.md) | AI-ADLC | ✅ |
| 4 | [`HOW_DWG_GENERATION_ENGINE_WORKS.md`](HOW_DWG_GENERATION_ENGINE_WORKS.md) | AI-DWG | ✅ |
| 5 | [`HOW_DWG_BROWNFIELD_DETECTION_WORKS.md`](HOW_DWG_BROWNFIELD_DETECTION_WORKS.md) | AI-DWG | ✅ |
| 6 | [`HOW_GCE_DERIVATION_PIPELINE_WORKS.md`](HOW_GCE_DERIVATION_PIPELINE_WORKS.md) | AI-GCE | ✅ |
| 7 | [`HOW_GCE_COMPLIANCE_AUDIT_WORKS.md`](HOW_GCE_COMPLIANCE_AUDIT_WORKS.md) | AI-GCE | ✅ |
| 8 | [`HOW_GCE_REDERIVATION_WORKS.md`](HOW_GCE_REDERIVATION_WORKS.md) | AI-GCE | ✅ |
| 9 | [`HOW_TGE_TEST_GOVERNANCE_WORKS.md`](HOW_TGE_TEST_GOVERNANCE_WORKS.md) | AI-TGE | ✅ |
| 10 | [`HOW_ILC_IDEA_LIFECYCLE_WORKS.md`](HOW_ILC_IDEA_LIFECYCLE_WORKS.md) | AI-ILC | ✅ |
| 11 | [`HOW_POLC_PRODUCT_OWNERSHIP_WORKS.md`](HOW_POLC_PRODUCT_OWNERSHIP_WORKS.md) | AI-POLC | ✅ |
| 117 | [`HOW_DFE_DATA_FABRIC_WORKS.md`](HOW_DFE_DATA_FABRIC_WORKS.md) | AI-DFE | ✅ |
| 110 | [`HOW_PACKAGE_ARCHETYPES_WORK.md`](HOW_PACKAGE_ARCHETYPES_WORK.md) | Family-wide | ✅ |

---

## Category 2: Family Chain & Orchestration (How Packages Connect)

How packages hand off to each other, share contracts, and maintain coherence.

| # | Document Name | Scope | Status |
|---|--------------|-------|:------:|
| 12 | [`HOW_CHAIN_HANDOFF_WORKS.md`](HOW_CHAIN_HANDOFF_WORKS.md) | Family-wide | ✅ |
| 13 | [`HOW_STATE_FILES_WORK.md`](HOW_STATE_FILES_WORK.md) | Family-wide | ✅ |
| 14 | [`HOW_DEPTH_LEVELS_WORK.md`](HOW_DEPTH_LEVELS_WORK.md) | Family-wide | ✅ |
| 15 | [`HOW_GATES_AND_APPROVALS_WORK.md`](HOW_GATES_AND_APPROVALS_WORK.md) | Family-wide | ✅ |
| 16 | [`HOW_FLOW_ORCHESTRATOR_WORKS.md`](HOW_FLOW_ORCHESTRATOR_WORKS.md) | AI-FLO | ✅ |
| 17 | [`HOW_PORTFOLIO_MANAGEMENT_WORKS.md`](HOW_PORTFOLIO_MANAGEMENT_WORKS.md) | AI-PPM | ✅ |
| 18 | `HOW_LIFECYCLE_CHANGE_PROPAGATION_WORKS.md` | Cross-cutting | 📋 |
| 19 | [`HOW_TEST_STRATEGY_WORKS.md`](HOW_TEST_STRATEGY_WORKS.md) | AI-TGE / Family-wide | ✅ |
| 111 | [`HOW_PACKAGE_ACTIVATION_ISOLATION_WORKS.md`](HOW_PACKAGE_ACTIVATION_ISOLATION_WORKS.md) | Family-wide | ✅ |
| 112 | [`HOW_PROJECT_LAYER_COLLABORATION_WORKS.md`](HOW_PROJECT_LAYER_COLLABORATION_WORKS.md) | AI-ADLC / AI-UXD / AI-POLC → AI-DWG | ✅ |
| 113 | [`HOW_COMMUNICATION_FABRIC_WORKS.md`](HOW_COMMUNICATION_FABRIC_WORKS.md) | Family-wide / Cross-family | ✅ |

---

## Category 3: Installation & Delivery (How Users Get and Run Packages)

How packages are installed, configured, and activated on different platforms.

| # | Document Name | Scope | Status |
|---|--------------|-------|:------:|
| 20 | [`HOW_PACKAGE_INSTALLATION_WORKS.md`](HOW_PACKAGE_INSTALLATION_WORKS.md) | Family-wide | ✅ |
| 21 | [`HOW_MULTI_PLATFORM_SUPPORT_WORKS.md`](HOW_MULTI_PLATFORM_SUPPORT_WORKS.md) | Family-wide | ✅ |
| 22 | [`HOW_STEERING_FILE_LOADING_WORKS.md`](HOW_STEERING_FILE_LOADING_WORKS.md) | Family-wide | ✅ |
| 23 | `HOW_ONE_COMMAND_INSTALL_WORKS.md` | Family-wide | 💡 |
| 24 | `HOW_CROSS_AGENT_PORTABILITY_WORKS.md` | Family-wide | 💡 |

---

## Category 4: Governance & Compliance (How Rules Are Generated and Enforced)

How AI-GCE generates, validates, and enforces governance rules.

| # | Document Name | Scope | Status |
|---|--------------|-------|:------:|
| 25 | [`HOW_HOOK_GENERATION_WORKS.md`](HOW_HOOK_GENERATION_WORKS.md) | AI-GCE | ✅ |
| 26 | [`HOW_TIERED_GOVERNANCE_WORKS.md`](HOW_TIERED_GOVERNANCE_WORKS.md) | AI-GCE | ✅ |
| 27 | [`HOW_PROVENANCE_TRACKING_WORKS.md`](HOW_PROVENANCE_TRACKING_WORKS.md) | AI-GCE / Family | ✅ |
| 28 | [`HOW_COMPLIANCE_LOGGING_WORKS.md`](HOW_COMPLIANCE_LOGGING_WORKS.md) | AI-GCE | ✅ |
| 29 | `HOW_RULE_CONFLICT_DETECTION_WORKS.md` | AI-GCE | 📋 |
| 30 | `HOW_PLATFORM_PORTABLE_ADAPTERS_WORK.md` | AI-GCE | 💡 |
| 31 | `HOW_ROLE_BASED_SCOPING_WORKS.md` | AI-GCE / AI-DWG | 💡 |
| 32 | `HOW_COMPOUNDING_CORRECTION_LOOP_WORKS.md` | AI-GCE / AI-TGE | 💡 |
| 33 | `HOW_DEPENDENCY_CVE_AWARENESS_WORKS.md` | AI-GCE | 💡 |
| 34 | `HOW_GOVERNANCE_EFFECTIVENESS_BENCHMARK_WORKS.md` | AI-TGE / AI-GCE | 💡 |
| 118 | [`HOW_DRIFT_INTAKE_WORKS.md`](HOW_DRIFT_INTAKE_WORKS.md) | AI-GCE + AI-FLO + AI-ADLC/POLC/UXD + AI-DWG | ✅ |

---

## Category 5: Versioning & Change Management (How Change Is Managed)

How artifacts are versioned, how changes propagate, and how conflicts are resolved.

| # | Document Name | Scope | Status |
|---|--------------|-------|:------:|
| 35 | `HOW_VERSION_PATCH_MANAGEMENT_WORKS.md` | Family-wide | 📋 |
| 36 | `HOW_CHANGE_REQUEST_MANAGEMENT_WORKS.md` | AI-PILC | 💡 |
| 37 | `HOW_ARTIFACT_OWNERSHIP_WORKS.md` | Cross-cutting | 📋 |

---

## Category 6: UX & Design (How User Experience Is Designed)

How AI-UXD manages the design lifecycle.

| # | Document Name | Scope | Status |
|---|--------------|-------|:------:|
| 38 | [`HOW_UX_DESIGN_LIFECYCLE_WORKS.md`](HOW_UX_DESIGN_LIFECYCLE_WORKS.md) | AI-UXD | ✅ |
| 39 | `HOW_MERMAID_DIAGRAM_RENDERING_WORKS.md` | AI-ADLC / AI-PILC / AI-UXD | 💡 |
| 40 | `HOW_PROGRESSIVE_DISCLOSURE_WORKS.md` | Family-wide | 💡 |

---

## Category 7: Operational Practices (How to Use Packages in Real Projects)

How practitioners apply the AI-* packages to accomplish real-world tasks — the bridge between tool mechanics and professional practice. Written from the user's perspective: "I need to do X — how do I use this tool to get it done?"

| # | Document Name | Scope | Status |
|---|--------------|-------|:------:|
| 41 | [`HOW_TO_INITIATE_A_PROJECT.md`](HOW_TO_INITIATE_A_PROJECT.md) | AI-PILC | ✅ |
| 42 | [`HOW_TO_DESIGN_ARCHITECTURE.md`](HOW_TO_DESIGN_ARCHITECTURE.md) | AI-ADLC | ✅ |
| 43 | [`HOW_TO_PREPARE_A_DEVELOPMENT_WORKSPACE.md`](HOW_TO_PREPARE_A_DEVELOPMENT_WORKSPACE.md) | AI-DWG | ✅ |
| 44 | [`HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md`](HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md) | AI-GCE | ✅ |
| 45 | [`HOW_TO_RUN_THE_FULL_CHAIN.md`](HOW_TO_RUN_THE_FULL_CHAIN.md) | Family-wide | ✅ |
| 46 | [`HOW_TO_RETROFIT_GOVERNANCE_ON_EXISTING_CODE.md`](HOW_TO_RETROFIT_GOVERNANCE_ON_EXISTING_CODE.md) | AI-DWG + AI-GCE | ✅ |
| 47 | [`HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md`](HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md) | AI-ADLC + AI-DWG + AI-GCE | ✅ |
| 48 | [`HOW_TO_ONBOARD_A_NEW_TEAM_MEMBER.md`](HOW_TO_ONBOARD_A_NEW_TEAM_MEMBER.md) | AI-DWG + AI-GCE | ✅ |
| 49 | [`HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md`](HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md) | AI-GCE | ✅ |
| 50 | [`HOW_TO_EVALUATE_AN_IDEA_BEFORE_BUILDING.md`](HOW_TO_EVALUATE_AN_IDEA_BEFORE_BUILDING.md) | AI-ILC | ✅ |
| 51 | [`HOW_TO_MANAGE_PRODUCT_BACKLOG.md`](HOW_TO_MANAGE_PRODUCT_BACKLOG.md) | AI-POLC | ✅ |
| 52 | [`HOW_TO_DESIGN_USER_EXPERIENCE.md`](HOW_TO_DESIGN_USER_EXPERIENCE.md) | AI-UXD | ✅ |
| 53 | [`HOW_TO_MANAGE_A_PORTFOLIO_OF_PROJECTS.md`](HOW_TO_MANAGE_A_PORTFOLIO_OF_PROJECTS.md) | AI-PPM | ✅ |
| 54 | [`HOW_TO_CHOOSE_ARCHITECTURE_EXTENSIONS.md`](HOW_TO_CHOOSE_ARCHITECTURE_EXTENSIONS.md) | AI-ADLC | ✅ |
| 55 | [`HOW_TO_RUN_A_COMPLIANCE_AUDIT.md`](HOW_TO_RUN_A_COMPLIANCE_AUDIT.md) | AI-GCE | ✅ |
| 56 | [`HOW_TO_USE_TEST_MODE.md`](HOW_TO_USE_TEST_MODE.md) | Family-wide | ✅ |
| 115 | [`HOW_TO_SKIP_OR_REORDER_PACKAGES.md`](HOW_TO_SKIP_OR_REORDER_PACKAGES.md) | Family-wide | ✅ |
| 116 | [`HOW_TO_USE_THE_DASHBOARD.md`](HOW_TO_USE_THE_DASHBOARD.md) | Family-wide (AIFLC-PDLC-Dashboard) | ✅ |
| 119 | [`HOW_TO_RUN_THE_DATA_FABRIC.md`](HOW_TO_RUN_THE_DATA_FABRIC.md) | AI-DFE | ✅ |

---

## Category 8: Impact & Rationale (Why Practices Matter)

Why specific practices matter, what breaks when they're skipped, and how the AI-* Family prevents those failures. Stakeholder-facing justification docs — making the case for governance, architecture, and process discipline.

| # | Document Name | Practice Area | Status |
|---|--------------|---------------|:------:|
| 56 | [`WHY_API_CONTRACT_FIRST_MATTERS.md`](WHY_API_CONTRACT_FIRST_MATTERS.md) | API Design | ✅ |
| 57 | [`WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md`](WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md) | Architecture | ✅ |
| 58 | [`WHY_PROJECT_INITIATION_MATTERS.md`](WHY_PROJECT_INITIATION_MATTERS.md) | PMO / Governance | ✅ |
| 59 | [`WHY_GOVERNANCE_AUTOMATION_MATTERS.md`](WHY_GOVERNANCE_AUTOMATION_MATTERS.md) | Compliance | ✅ |
| 60 | [`WHY_SEPARATION_OF_DUTIES_MATTERS.md`](WHY_SEPARATION_OF_DUTIES_MATTERS.md) | Security / Roles | ✅ |
| 61 | [`WHY_SPEC_BEFORE_CODE_MATTERS.md`](WHY_SPEC_BEFORE_CODE_MATTERS.md) | Session Discipline | ✅ |
| 62 | [`WHY_PROGRESSIVE_GOVERNANCE_MATTERS.md`](WHY_PROGRESSIVE_GOVERNANCE_MATTERS.md) | Compliance Adoption | ✅ |
| 63 | [`WHY_MODULE_BOUNDARIES_MATTER.md`](WHY_MODULE_BOUNDARIES_MATTER.md) | Architecture / DDD | ✅ |
| 64 | [`WHY_STATE_TRACKING_MATTERS.md`](WHY_STATE_TRACKING_MATTERS.md) | Workflow Continuity | ✅ |
| 65 | [`WHY_BROWNFIELD_AWARENESS_MATTERS.md`](WHY_BROWNFIELD_AWARENESS_MATTERS.md) | Existing Systems | ✅ |
| 66 | [`WHY_DEPTH_CALIBRATION_MATTERS.md`](WHY_DEPTH_CALIBRATION_MATTERS.md) | Adaptive Process | ✅ |
| 67 | [`WHY_NAMING_CONVENTIONS_MATTER.md`](WHY_NAMING_CONVENTIONS_MATTER.md) | Code Quality | ✅ |
| 68 | [`WHY_SECURITY_GATES_MATTER.md`](WHY_SECURITY_GATES_MATTER.md) | Security | ✅ |
| 69 | [`WHY_TESTING_STRATEGY_MATTERS.md`](WHY_TESTING_STRATEGY_MATTERS.md) | Quality Assurance | ✅ |
| 70 | [`WHY_CHANGE_MANAGEMENT_MATTERS.md`](WHY_CHANGE_MANAGEMENT_MATTERS.md) | Change Control | ✅ |
| 114 | [`WHY_LIFECYCLE_SEQUENCE_MATTERS.md`](WHY_LIFECYCLE_SEQUENCE_MATTERS.md) | Process / Chain Sequencing | ✅ |

---

## Category 9: Design Patterns (Reusable Patterns Across Packages)

Recurring design patterns used across multiple AI-* Family packages — the structural building blocks that give the family its consistency.

| # | Document Name | Scope | Status |
|---|--------------|-------|:------:|
| 71 | [`PATTERN_TWO_SOURCE_MODEL.md`](PATTERN_TWO_SOURCE_MODEL.md) | AI-GCE / AI-TGE / AI-ILC | ✅ |
| 72 | [`PATTERN_CONDITIONAL_GENERATION.md`](PATTERN_CONDITIONAL_GENERATION.md) | AI-DWG / AI-GCE / AI-ADLC | ✅ |
| 73 | [`PATTERN_MARKER_FILE_DETECTION.md`](PATTERN_MARKER_FILE_DETECTION.md) | Family-wide | ✅ |
| 74 | [`PATTERN_GRACEFUL_STANDALONE.md`](PATTERN_GRACEFUL_STANDALONE.md) | Family-wide | ✅ |
| 75 | [`PATTERN_CUSTOM_PRESERVATION.md`](PATTERN_CUSTOM_PRESERVATION.md) | AI-DWG / AI-GCE | ✅ |
| 76 | [`PATTERN_PROGRESSIVE_ACTIVATION.md`](PATTERN_PROGRESSIVE_ACTIVATION.md) | Family-wide | ✅ |
| 77 | [`PATTERN_DOWNSTREAM_SIGNALING.md`](PATTERN_DOWNSTREAM_SIGNALING.md) | Family-wide (chain) | ✅ |
| 78 | [`PATTERN_ADAPTIVE_INTAKE.md`](PATTERN_ADAPTIVE_INTAKE.md) | All lifecycle packages | ✅ |
| 79 | [`PATTERN_GATE_BEFORE_TRANSITION.md`](PATTERN_GATE_BEFORE_TRANSITION.md) | All lifecycle packages | ✅ |
| 80 | [`PATTERN_NON_DESTRUCTIVE_RECONCILIATION.md`](PATTERN_NON_DESTRUCTIVE_RECONCILIATION.md) | AI-DWG / AI-GCE / AI-TGE | ✅ |

---

## Category 10: Troubleshooting & Recovery (What If Something Goes Wrong)

Scenario-based recovery guides for when things break — fast answers for practitioners in trouble.

| # | Document Name | Scenario | Status |
|---|--------------|----------|:------:|
| 81 | [`WHAT_IF_STATE_FILE_IS_LOST.md`](WHAT_IF_STATE_FILE_IS_LOST.md) | State file deleted, corrupted, or missing | ✅ |
| 82 | [`WHAT_IF_TEAM_REJECTS_GOVERNANCE.md`](WHAT_IF_TEAM_REJECTS_GOVERNANCE.md) | Team disables hooks, resists governance | ✅ |
| 83 | [`WHAT_IF_CHAIN_HANDOFF_FAILS.md`](WHAT_IF_CHAIN_HANDOFF_FAILS.md) | Successor can't find predecessor output | ✅ |
| 84 | [`WHAT_IF_WRONG_DEPTH_WAS_CHOSEN.md`](WHAT_IF_WRONG_DEPTH_WAS_CHOSEN.md) | Depth level doesn't match project complexity | ✅ |
| 85 | [`WHAT_IF_ARCHITECTURE_CHANGES_BREAK_GOVERNANCE.md`](WHAT_IF_ARCHITECTURE_CHANGES_BREAK_GOVERNANCE.md) | Re-derivation produces conflicts or broken rules | ✅ |

---

## Category 11: Decision Guides (When to Choose What)

Decision-timing guides for practitioners at a fork in the road — derived from patterns, answering "which option fits MY situation?"

| # | Document Name | Decision | Status |
|---|--------------|----------|:------:|
| 86 | [`WHEN_TO_USE_STANDALONE_VS_CHAIN.md`](WHEN_TO_USE_STANDALONE_VS_CHAIN.md) | Full chain or single package? | ✅ |
| 87 | [`WHEN_TO_USE_MINIMAL_VS_COMPREHENSIVE.md`](WHEN_TO_USE_MINIMAL_VS_COMPREHENSIVE.md) | Which depth level fits my project? | ✅ |
| 88 | [`WHEN_TO_USE_BROWNFIELD_VS_GREENFIELD.md`](WHEN_TO_USE_BROWNFIELD_VS_GREENFIELD.md) | Existing code or fresh start? | ✅ |
| 89 | [`WHEN_TO_TRIGGER_REDERIVATION.md`](WHEN_TO_TRIGGER_REDERIVATION.md) | Something changed — do I re-derive? | ✅ |
| 90 | [`WHEN_TO_CUSTOMIZE_VS_USE_STEERING.md`](WHEN_TO_CUSTOMIZE_VS_USE_STEERING.md) | Edit the file or edit the source? | ✅ |
| 91 | [`WHEN_TO_ACTIVATE_NEXT_GOVERNANCE_TIER.md`](WHEN_TO_ACTIVATE_NEXT_GOVERNANCE_TIER.md) | Ready to graduate tiers? | ✅ |
| 120 | [`WHEN_TO_CONFORM_AMEND_OR_WAIVE_DRIFT.md`](WHEN_TO_CONFORM_AMEND_OR_WAIVE_DRIFT.md) | Drift detected — which disposition? | ✅ |

---

## Category 12: Artifact Anatomy (Deep-Dive References)

Field-by-field breakdowns of key artifacts — for builders and contributors who need to create, debug, or understand these files at the structural level.

| # | Document Name | Artifact | Status |
|---|--------------|----------|:------:|
| 92 | [`ANATOMY_OF_A_STATE_FILE.md`](ANATOMY_OF_A_STATE_FILE.md) | `*-state.md` files | ✅ |
| 93 | [`ANATOMY_OF_A_HOOK.md`](ANATOMY_OF_A_HOOK.md) | `.kiro/hooks/*.json` files | ✅ |
| 94 | [`ANATOMY_OF_A_STEERING_FILE.md`](ANATOMY_OF_A_STEERING_FILE.md) | `.kiro/steering/*.md` files | ✅ |
| 95 | [`ANATOMY_OF_AN_ADR.md`](ANATOMY_OF_AN_ADR.md) | Architecture Decision Records | ✅ |

---

## Category 13: Lifecycle (How Artifacts Evolve Over Time)

Temporal guides showing how key artifacts move through states over a project's lifetime — from creation through evolution to retirement.

| # | Document Name | Subject | Status |
|---|--------------|---------|:------:|
| 96 | [`LIFECYCLE_OF_A_GOVERNANCE_RULE.md`](LIFECYCLE_OF_A_GOVERNANCE_RULE.md) | Rules: born → active → re-derived → deprecated | ✅ |
| 97 | [`LIFECYCLE_OF_A_STEERING_FILE.md`](LIFECYCLE_OF_A_STEERING_FILE.md) | Steering: generated → customized → reconciled → obsolete | ✅ |
| 98 | [`LIFECYCLE_OF_AN_ARCHITECTURE_DECISION.md`](LIFECYCLE_OF_AN_ARCHITECTURE_DECISION.md) | ADRs: proposed → accepted → propagated → superseded | ✅ |
| 99 | [`LIFECYCLE_OF_A_PROJECT_THROUGH_THE_CHAIN.md`](LIFECYCLE_OF_A_PROJECT_THROUGH_THE_CHAIN.md) | Project: idea → initiation → design → workspace → governed delivery | ✅ |

---

## Category 14: Interactions (How Components Work Together)

Maps pairwise interactions between system components — for practitioners who need to understand how changing one thing affects another.

| # | Document Name | Interaction | Status |
|---|--------------|-------------|:------:|
| 100 | [`INTERACTION_BETWEEN_STEERING_AND_HOOKS.md`](INTERACTION_BETWEEN_STEERING_AND_HOOKS.md) | Steering ↔ Hooks (dual enforcement) | ✅ |
| 101 | [`INTERACTION_BETWEEN_DEPTH_AND_GOVERNANCE.md`](INTERACTION_BETWEEN_DEPTH_AND_GOVERNANCE.md) | Depth levels ↔ Tier availability | ✅ |
| 102 | [`INTERACTION_BETWEEN_EXTENSIONS_AND_GOVERNANCE.md`](INTERACTION_BETWEEN_EXTENSIONS_AND_GOVERNANCE.md) | ADLC extensions ↔ GCE rules/hooks | ✅ |
| 103 | [`INTERACTION_BETWEEN_BROWNFIELD_AND_TIERS.md`](INTERACTION_BETWEEN_BROWNFIELD_AND_TIERS.md) | Brownfield baseline ↔ Tier progression | ✅ |

---

## Category 15: Reference Maps (Quick-Lookup Tables)

Consolidated lookup tables for specific reference data — instant answers without narrative.

| # | Document Name | What It Consolidates | Status |
|---|--------------|---------------------|:------:|
| 104 | [`REFERENCE_MAP_SIGNALS.md`](REFERENCE_MAP_SIGNALS.md) | All downstream signals: from → to → event → action | ✅ |
| 105 | [`REFERENCE_MAP_TRIGGERS.md`](REFERENCE_MAP_TRIGGERS.md) | All conditional generation triggers: file → condition → source | ✅ |
| 106 | [`REFERENCE_MAP_BASELINE_RULES.md`](REFERENCE_MAP_BASELINE_RULES.md) | All 10 universal baseline rules | ✅ |
| 107 | [`REFERENCE_MAP_MARKERS.md`](REFERENCE_MAP_MARKERS.md) | All marker files: package → filename → detected by | ✅ |
| 108 | [`GLOSSARY.md`](GLOSSARY.md) | Subject-matter terminology across all packages | ✅ |
| 109 | [`PILC_OUTPUT_STRUCTURE.md`](PILC_OUTPUT_STRUCTURE.md) | AI-PILC runtime output folder structure & portfolio feeding | ✅ |
| 113 | [`REFERENCE_MAP_DWG_INPUT_TO_OUTPUT.md`](REFERENCE_MAP_DWG_INPUT_TO_OUTPUT.md) | AI-DWG: each ADLC/POLC/UXD input → destination workspace file | ✅ |

---

## Summary

| Category | Documents | ✅ Created | 📋 Planned | 💡 Future |
|----------|:---------:|:----------:|:----------:|:---------:|
| 1. Package Mechanics | 13 | 13 | 0 | 0 |
| 2. Chain & Orchestration | 10 | 9 | 1 | 0 |
| 3. Installation & Delivery | 5 | 3 | 0 | 2 |
| 4. Governance & Compliance | 11 | 5 | 1 | 5 |
| 5. Versioning & Change | 3 | 0 | 2 | 1 |
| 6. UX & Design | 3 | 1 | 0 | 2 |
| 7. Operational Practices | 19 | 19 | 0 | 0 |
| 8. Impact & Rationale (WHY) | 16 | 16 | 0 | 0 |
| 9. Design Patterns | 10 | 10 | 0 | 0 |
| 10. Troubleshooting & Recovery | 5 | 5 | 0 | 0 |
| 11. Decision Guides | 7 | 7 | 0 | 0 |
| 12. Artifact Anatomy | 4 | 4 | 0 | 0 |
| 13. Lifecycle | 4 | 4 | 0 | 0 |
| 14. Interactions | 4 | 4 | 0 | 0 |
| 15. Reference Maps | 7 | 7 | 0 | 0 |
| **TOTAL** | **121** | **107** | **4** | **10** |

---

## Prioritization Guide

### Write First — Operational Practices (highest value for new users)

1. `HOW_TO_RUN_THE_FULL_CHAIN.md` — End-to-end operational guide
2. `HOW_TO_INITIATE_A_PROJECT.md` — First package most users encounter
3. `HOW_TO_DESIGN_ARCHITECTURE.md` — Second most common entry point
4. `HOW_TO_PREPARE_A_DEVELOPMENT_WORKSPACE.md` — What happens after architecture
5. `HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` — How to bring enforcement to any project

### Write First — WHY Documents (stakeholder justification, highest persuasion value)

1. `WHY_SPEC_BEFORE_CODE_MATTERS.md` — Counters "just start coding" culture
2. `WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md` — Justifies the upfront design investment
3. `WHY_API_CONTRACT_FIRST_MATTERS.md` — Prevents integration failures
4. `WHY_GOVERNANCE_AUTOMATION_MATTERS.md` — Justifies the AI-GCE investment
5. `WHY_PROJECT_INITIATION_MATTERS.md` — Counters "we don't need a charter" resistance

### Write Second — Operational (real-world scenarios)

6. `HOW_TO_RETROFIT_GOVERNANCE_ON_EXISTING_CODE.md` — Brownfield is the common case
7. `HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` — Reconciliation in practice
8. `HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md` — Tier progression in practice
9. `HOW_TO_CHOOSE_ARCHITECTURE_EXTENSIONS.md` — When DDD/Microservices/etc. apply
10. `HOW_TO_RUN_A_COMPLIANCE_AUDIT.md` — Periodic governance health check

### Recently Completed (2026-06-15) — newest-package knowledge coverage

All planned knowledge docs for the four newest packages are now written (every built package has both mechanics and operational coverage):

- `HOW_FLOW_ORCHESTRATOR_WORKS.md` — AI-FLO ✅ created
- `HOW_PORTFOLIO_MANAGEMENT_WORKS.md` — AI-PPM ✅ created
- `HOW_UX_DESIGN_LIFECYCLE_WORKS.md` — AI-UXD ✅ created
- `HOW_TO_MANAGE_PRODUCT_BACKLOG.md` — AI-POLC ✅ created
- `HOW_TO_DESIGN_USER_EXPERIENCE.md` — AI-UXD ✅ created
- `HOW_TO_MANAGE_A_PORTFOLIO_OF_PROJECTS.md` — AI-PPM ✅ created

**Remaining planned (📋, 4):** `HOW_LIFECYCLE_CHANGE_PROPAGATION_WORKS.md` (#18), `HOW_RULE_CONFLICT_DETECTION_WORKS.md` (#29), `HOW_VERSION_PATCH_MANAGEMENT_WORKS.md` (#35), `HOW_ARTIFACT_OWNERSHIP_WORKS.md` (#37) — tied to capabilities not yet built or separate work streams.

### Write On Demand (reference docs for specific questions)

- Any document can be written when someone asks "how does X work?" or "why does X matter?"
- The catalogue ensures we know what's missing and where it belongs

---

*Catalogue maintained by: Maheri | Created: 2026-06-11*

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-07-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
