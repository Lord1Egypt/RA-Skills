<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: workspace-integrity-agent
description: >
  Validates generated workspace completeness — steering file presence and correctness,
  folder structure alignment with C4 L3 components, config consistency, and provenance integrity
  after AI-DWG generation or reconciliation.
generatedBy: AI-DWG
generatedVersion: "{version}"
source: ai-dwg-rules/core-generator.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read"]
trigger: WIA__
tier: 1
type: audit
---

# Workspace Integrity Agent

## Purpose

Validates that the development workspace produced by AI-DWG is structurally complete, internally consistent, and ready for AI-GCE governance enforcement and AI-DLC v1 development. Checks steering file presence against what the Architecture Package justifies, folder structure alignment with C4 L3 component decomposition, configuration file consistency, provenance front-matter integrity, and downstream readiness for AI-GCE signal consumption.

## When to Invoke

Call this agent **after AI-DWG completes generation or reconciliation** — before AI-GCE derives compliance hooks or the development team begins coding.

- **Trigger:** Type `WIA__` in the chat prompt
- **Cadence:** Once per full generation (Mode 1); once per reconciliation (Mode 2); once after brownfield overlay (Mode 3)
- **Process point:** After AI-DWG STEP 5 (Output Summary) or when the user says "is the workspace ready?"

**Concrete examples:**
- "I just generated the workspace from my AP" → call `WIA__` to validate completeness
- "Is my workspace ready for AI-GCE?" → call `WIA__` to check downstream readiness
- "I reconciled after architecture changes" → call `WIA__` to verify delta was applied correctly
- "The team is about to start coding" → call `WIA__` first to ensure day-1 readiness
- "I ran brownfield overlay on an existing repo" → call `WIA__` to confirm steering was correctly merged

## Consequences of Skipping

**Immediate impact:**
- Missing steering files → AI-GCE cannot derive complete compliance hooks; enforcement has gaps
- Folder structure misaligned with AP → developers create modules in wrong locations, violating architecture
- Config inconsistencies → build tools, linters, or test runners don't match architecture decisions
- Broken provenance → steering rules cannot be traced back to architecture decisions; trust erodes
- Incomplete downstream signal → AI-GCE receives a partial workspace state, derives incomplete governance

**Accumulated debt (skipped across multiple projects):**
- Workspaces diverge from architecture over time — "generated once, never validated" anti-pattern
- AI-GCE generates hooks against incomplete steering → false sense of governance coverage
- Development teams lose trust in generated workspaces ("the folders don't match the architecture")
- Reconciliation becomes unreliable — no baseline comparison for what's correct vs. what's drifted
- Cross-package contract violations go undetected — AI-DWG's "I Produce" guarantee becomes hollow

## Recovery

If you skipped `WIA__` and the workspace is already in use:

1. Run `WIA__` now — it checks the CURRENT state of the workspace against the source AP
2. For each gap found:
   - **Missing steering file:** Determine if the AP justifies it (conditional vs. always-present); if justified, regenerate the specific file using the relevant mapping rule from `ai-dwg-rule-details/mapping/`
   - **Folder structure gap:** Compare C4 L3 component names against `src/` or equivalent; add missing module directories; log additions in Change Log
   - **Config mismatch:** Cross-reference technology decisions in `adlc-state.md` against generated configs (`.editorconfig`, `docker-compose.yml`, etc.); fix inconsistencies
   - **Provenance missing/broken:** Add or correct the `---` front-matter block; ensure `source:` traces to the correct AP artifact
   - **Downstream signal incomplete:** Re-send the AI-DWG→AI-GCE signal with the corrected workspace state
3. If AI-GCE has already derived hooks:
   - Flag which steering files were missing/corrected
   - Request AI-GCE re-derivation for affected compliance rules
4. If development has already started:
   - Compare existing code module locations against the validated structure
   - Flag any code placed in non-architectural locations for team awareness

## Checks Performed

### Steering File Completeness (S1–S5)

1. **S1 — Always-present file verification:** Verify all 14 mandatory steering files exist in `rules/`: `workspace-rules.md`, `architecture-principles.md`, `tech-stack.md`, `coding-standards.md`, `security-rules.md`, `api-standards.md`, `module-structure.md`, `testing-strategy.md`, `database-rules.md`, `naming-conventions.md`, `git-workflow.md`, `error-handling.md`, `observability-logging.md`, `observability-sensitive.md`.
2. **S2 — Conditional file justification:** For each conditional steering file present (`multi-tenancy.md`, `resilience-standards.md`, `frontend-standards.md`, `event-sourcing.md`, `feature-flags.md`, `api-versioning.md`, `observability-tracing.md`, `domain-context.md`), verify the AP contains the architectural justification (extension active, pattern detected, or trigger condition met).
3. **S3 — No unjustified conditionals:** Verify no conditional steering file exists WITHOUT AP justification. A conditional file without architectural backing = bloat.
4. **S4 — Operational document presence:** Verify `DEFINITION_OF_DONE.md`, `CODEOWNERS`, `info/PROJECT_INSTRUCTIONS.md`, and `README.md` exist at workspace root.
5. **S5 — Planning template presence:** Verify `templates/` contains planning templates appropriate to team size (sprint-planning, session-planning, standup at minimum for team size > 1).

### Workspace Structure Alignment (W1–W4)

6. **W1 — Module-to-component mapping:** Cross-reference source folder structure against C4 L3 component names in `module-structure.md`. Every architectural component should map to a workspace module.
7. **W2 — No orphan modules:** Verify no source directory exists that isn't traceable to a C4 L3 component or a recognized infrastructure concern (config, scripts, docs).
8. **W3 — Depth-level consistency:** Verify generated content depth matches the AP complexity indicators (Minimal/Standard/Comprehensive) as documented in the generation summary.
9. **W4 — Extension-specific structure:** If AI-ADLC extensions were active, verify the corresponding workspace structures exist (e.g., DDD → aggregate-aligned modules; Microservices → service boundaries).

### Configuration Consistency (C1–C4)

10. **C1 — Technology label alignment:** Verify technology labels in `tech-stack.md` match what appears in generated configs (`.editorconfig` language, `docker-compose.yml` services, package manager references).
11. **C2 — Git workflow alignment:** Verify `git-workflow.md` branching model is reflected in any generated CI/CD pipeline configs or PR templates.
12. **C3 — Testing strategy alignment:** Verify `testing-strategy.md` test types are reflected in generated test folder structure and any test runner configurations.
13. **C4 — Security rules enforcement:** Verify security constraints from `security-rules.md` are reflected in generated configs (e.g., HTTPS-only in docker-compose, auth middleware in service configs).

### Provenance Integrity (P1–P3)

14. **P1 — Front-matter presence:** Every generated steering file MUST have the provenance front-matter block (`generatedBy: AI-DWG`, `generatedVersion`, `source`, `generatedOn`, `ownership`).
15. **P2 — Source traceability:** Every `source:` field must resolve to an actual AP artifact path that exists and informed the steering file's content.
16. **P3 — Ownership correctness:** `ownership: generated` for files produced entirely by AI-DWG; `ownership: hybrid` for reconciled files with team customizations; `ownership: user` never set by AI-DWG.

### Downstream Readiness (D1–D3)

17. **D1 — AI-GCE signal completeness:** Verify the workspace contains everything AI-GCE needs to derive compliance hooks: steering files present + `rules/workspace-rules.md` as the entry point marker.
18. **D2 — State file consistency:** If `adlc-state.md` is accessible, verify the workspace reflects its declared extensions, containers, and technology decisions.
19. **D3 — Marker file integrity:** Verify `rules/workspace-rules.md` exists and contains the architecture identity section (system name, tech stack summary, constraint summary) that AI-GCE uses as its detection marker.

## Output

- **If all checks pass:** Summary report:
  ```
  ✅ Workspace Integrity Check — PASS
  🏗️ {system_name} | Depth: {level} | Mode: {1|2|3}
  📁 Steering: {n}/14 mandatory + {m} conditional | Modules: {n} mapped
  ⚙️ Configs: consistent | Provenance: complete | Downstream: ready
  🎯 Ready for AI-GCE governance derivation + development kickoff.
  ```

- **If violations found:**
  - Per-check report: check ID, status (PASS/WARN/FAIL), finding, remediation suggestion
  - Summary score: `{passed}/{total} checks passed`
  - Compliance log entry appended to `.governance/compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, agent: `workspace-integrity-agent`, result: `pass|fail|warn`
  - Prioritized remediation list (FAIL items first, then WARN)

**Output location:** `.governance/compliance-log/events/` (if `.governance/` exists; otherwise inline report only)

## Related

- **Generator source:** `ai-dwg-rules/core-generator.md` (defines generation modes and output guarantees)
- **Validation rules:** `ai-dwg-rule-details/common/validation-rules.md` (cross-check specifications)
- **AP reading guide:** `ai-dwg-rule-details/common/ap-reading-guide.md` (how to parse AP for validation)
- **Contract:** Agent Governance Contract §4, §5
- **Predecessor dependency:** AI-ADLC's `adlc-state.md` informs what the workspace SHOULD contain
- **Successor dependency:** AI-GCE reads `rules/` — integrity of that folder directly impacts governance quality
- **Complementary agents:** `compliance-audit-agent` (AI-GCE) checks code compliance; WIA checks workspace-level structural integrity
