# Platonic Coding Workflow Overview

## Objective

Execute the full three-phase Platonic Coding workflow with clear phase visibility and correct handoffs between RFC specification, implementation, and review. Platonic Brainstorming integration is optional at Phases 1 and 2.

## Phase Visibility Rule

**Always show the current Phase** at the start of each step and in any status summary, e.g.:

- `[Phase 1] RFC Specification`
- `[Phase 2] Implementation`
- `[Phase 3] Spec Compliance Review`
- `[FINISHED]`

## Phase Flow

```
Phase 1: RFC Specification
    → Optional: platonic-brainstorming (conceptual design exploration)
    → Create design draft (docs/drafts/)
    → Generate RFC from draft
    → SPECS mode: specs-refine (validate + update supporting files)
Phase 2: Implementation
    → Optional: platonic-brainstorming (design refinement)
    → IMPL mode: impl-full (spec analysis → guide → plan → code + tests)
Phase 3: Spec Compliance Review
    → REVIEW mode: review code against RFC + impl guides
    → Compliance report
FINISHED
```

## Default Paths

- Design drafts: `docs/drafts/`
- RFC specs: `docs/specs/`
- Implementation guides: `docs/impl/`

User may override any path via `.platonic.yml`.

## Platonic Brainstorming Integration Pattern

All phases that integrate brainstorming follow this standard pattern:

### Detection and Invocation

1. **Detect**: Use Skill tool with `skill: "platonic-brainstorming"` to check availability
2. **Invoke**: If available and user wants structured exploration:
   - Skill guides collaborative dialogue
   - Explores requirements, constraints, approaches, trade-offs
   - Produces design artifacts (draft or refined insights)
3. **Benefits**: Structured exploration, approach comparison, incremental validation

### Phase-Specific Usage

- **Phase 1**: Use before RFC formalization for conceptual design exploration
- **Phase 2**: Use before implementation for design refinement and architecture validation
- **Phase 3**: Not applicable (review phase is purely analytical)

## When to Ask the User

- **Phase 1**: RFC number/index for the new or updated RFC, if not specified. Whether to use `platonic-brainstorming` for conceptual design.
- **Phase 2**: RFC number/index for which to implement, if not specified. Whether to use `platonic-brainstorming` for design refinement. The IMPL mode operation handles its own confirmation gates for impl guide and coding plan.
- **Phase 3**: Which code paths and RFC(s) to review, if not specified.

## Skill/Mode Invocations

| Phase | Optional Integration | Skill / Action |
|-------|---------------------|----------------|
| 1 | `platonic-brainstorming` | **SPECS mode** — draft → RFC → refine (validate + update supporting files) |
| 2 | `platonic-brainstorming` | **IMPL mode** — impl-full: spec analysis → impl guide → coding plan → code with tests |
| 3 | — | **REVIEW mode** — review code against RFC specs and impl guides |

Read the phase-specific reference file before executing each phase:

- `references/WORKFLOW/workflow-phase-1.md` — RFC Specification
- `references/WORKFLOW/workflow-phase-2.md` — Implementation
- `references/WORKFLOW/workflow-phase-3.md` — Spec Compliance Review