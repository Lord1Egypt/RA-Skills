---
name: platonic-coding
description: Intelligent orchestrator for Platonic Coding workflow. Auto-detects project state and routes to the right next step—initialize a project, run the recovery flow for existing code, formalize drafts into RFCs, refine specs, implement from guides with tests, or review code compliance. Single entry point for the complete specification-driven development lifecycle.
license: MIT
metadata:
  version: "2.3.0"
  author: "Xiaming Chen"
  category: "workflow"
  replaces:
    - platonic-init
    - platonic-specs
    - platonic-impl
    - platonic-code-review
    - platonic-workflow
  integrates:
    - platonic-brainstorming (optional)
---

# Platonic Coding

Intelligent orchestrator for the complete **specification-driven development lifecycle**. Auto-detects project state and executes the appropriate workflow phases—initialization, specification management, implementation, or review. Integrates with `platonic-brainstorming` as an optional accelerator in Phases 1 and 2 for structured design exploration and refinement.

## When to Use This Skill

Use this skill when you need to:

- **Bootstrap** a new project with Platonic Coding infrastructure
- **Adopt** Platonic Coding for an existing codebase (recover specs from code)
- **Manage** RFC specifications (validate, refine, generate indices)
- **Implement** features from RFC specs with guides and tests
- **Review** code for spec compliance
- **Run** the full workflow from design → RFC → code → review

**Keywords**: platonic coding, specs, RFC, implementation, review, workflow, spec-driven, initialization

## Intelligent Auto-Detection

Auto-detects project state when invoked without specific instructions. See `references/REFERENCE.md` for the full decision tree.

**Quick Reference**:
- No `.platonic.yml` → INIT mode (scaffold new or recover existing)
- RFCs but no guides → Phase 2 (implementation)
- Guides + code → Phase 3 (review) or resume Phase 2

**Override** with canonical operations: `init-scaffold`, `init-scan`, `specs-refine`, `impl-full`, `review`, `workflow --phase <N>`.

## Core Workflow Phases

| Phase | Focus | Output | Brainstorming |
|-------|-------|--------|---------------|
| **1** | RFC Specification | Draft → RFC → `specs-refine` | ✅ Optional |
| **2** | Implementation | Guide → Code + Tests | ✅ Optional |
| **3** | Review | Compliance report | ❌ |

Phases run sequentially (full workflow) or independently (explicit invocation). See `references/WORKFLOW/workflow-overview.md` for details.

## Operation Modes

### INIT Mode
Bootstrap Platonic Coding infrastructure. Operations: `init-scaffold`, `init-scan`, `init-plan-modular-specs`, `init-recover-*`.

**Examples**: `init-scaffold for project "Acme"`, `init-scan then recover specs`.

### SPECS Mode
Manage RFC specifications. Operations: `specs-refine` (comprehensive), `specs-generate-*`, `specs-validate-*`, `specs-check-*`.

**Examples**: `specs-refine`, `specs-generate-index`.

### IMPL Mode
Translate RFCs to guides and code. Operations: `impl-full` (default), `impl-create-guide`, `impl-code`, `impl-validate-guide`, `impl-update-guide`.

**Confirmation Gates**: Pauses after impl guide and coding plan. Override with "no confirmations".

**Examples**: `impl-full for RFC-042`, `impl-code from IG-001`.

### REVIEW Mode
Validate code against specs. Generates report-only by default (no code changes). 6-step process: understand specs → checklist → map → review → discrepancies → report.

**Examples**: `review src/auth/ against RFC-001`, `review for gap analysis`.

### WORKFLOW Mode
Orchestrate full 3-phase flow. See `references/WORKFLOW/workflow-overview.md`.

**Examples**: `workflow --phase 1`, `workflow with platonic-brainstorming`.

---

For detailed guides, see `references/REFERENCE.md`.

## Default Paths & Templates

| Artifact | Path | Naming |
|----------|------|--------|
| Drafts | `docs/drafts/` | `YYYY-MM-DD-<topic>-design.md` |
| RFCs | `docs/specs/` | `RFC-NNN-<name>.md` |
| Guides | `docs/impl/` | `IG-NNN-<name>.md` |

Templates in `assets/` use `{{PLACEHOLDER}}` syntax.

## Best Practices

1. Trust auto-detection; override with explicit operations when needed
2. Review generated artifacts (all Draft status)
3. Run `specs-refine` regularly
4. Use confirmation gates—don't skip unless confident
5. Review mode is report-only by default

## Dependencies

- Read/write to project directories
- Access to `.platonic.yml`
- Understanding of target language/framework
