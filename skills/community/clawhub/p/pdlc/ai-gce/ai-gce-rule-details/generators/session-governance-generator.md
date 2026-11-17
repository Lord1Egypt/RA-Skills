<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Session Governance — Derivation Logic

## Purpose

Derives AI-DLC v1 session methodology rules (GOV-SESSION-*) from `session-governance.md`. This is a HYBRID category: built-in baseline ensures minimum AI-DLC v1 discipline; steering enriches with project-specific session rules.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in methodology discipline: session rules define HOW AI operates, not just WHAT it produces
- Treat baseline rules (spec-before-code, never-vibe-code) as non-negotiable methodology controls
- Evaluate correction escalation patterns: repeated violations signal a process gap, not just an instance failure
- Ensure every session rule is binary-checkable at the moment of enforcement (promptSubmit, preToolUse)
- Consider autonomy mode as a control parameter: autopilot vs. supervised changes the enforcement surface

### Anti-Patterns for This Activity
- Do NOT weaken "never vibe code" or "spec before code" — these are the AI-DLC v1 methodology's identity
- Do NOT create session rules that require human memory to enforce — hooks must verify automatically
- Do NOT allow session-discipline to be removed from the hook set (it may be noisy but it's core methodology)

### Quality Check
A good output from this activity sounds like:
- "GOV-SESSION-BASELINE-01: Spec/design MUST exist before implementation. Enforced by pre-code-spec-check.json (preToolUse write). Fires BEFORE any code file is written — prevention, not detection."
- "Correction escalation: if session-discipline detects same violation twice (loop pattern), hook output recommends Level 2 (Pattern Fix: update steering file)."

---

## Source Steering Files

| File | What to Extract |
|------|----------------|
| `session-governance.md` | Session rules table (SG-01 to SG-12), session structure, autonomy mode |

---

## Built-in Baseline (Always Generated — These ARE the AI-DLC v1 Methodology)

| Rule ID | Statement | Rationale |
|---------|-----------|-----------|
| GOV-SESSION-BASELINE-01 | Spec/design MUST exist before implementation code is written | AI-DLC v1 core: design precedes implementation |
| GOV-SESSION-BASELINE-02 | NEVER "vibe code" — all code follows steering rules, no freestyling | AI-DLC v1 discipline: AI follows rules |
| GOV-SESSION-BASELINE-03 | One task at a time — complete before starting next | AI-DLC v1 focus: prevents context mixing |
| GOV-SESSION-BASELINE-04 | If AI loops twice on same mistake, stop and try different approach | AI-DLC v1 efficiency: escalation over repetition |

---

## Steering-Enriched Rules

### From `session-governance.md` → Rules Table

Every SG-NN rule in the steering becomes a GOV-SESSION rule:

| Steering Rule | Generated Compliance Rule |
|---------------|--------------------------|
| SG-01: "NEVER write code without checking relevant steering files first" | GOV-SESSION-001: Steering files loaded before any code generation |
| SG-02: "One task per session — complete before starting next" | GOV-SESSION-002: No parallel task starts |
| SG-03: "Verify against DEFINITION_OF_DONE.md before declaring task complete" | GOV-SESSION-003: DoD verification at task completion |
| SG-07: "Read domain-context.md before naming any entity, variable, or endpoint" | GOV-SESSION-007: Domain context consulted before naming |
| SG-08: "Read api-standards.md before creating any API endpoint" | GOV-SESSION-008: API standards consulted before endpoint creation |

### From `session-governance.md` → Session Structure

The session structure (Start → Check → Plan → Implement → Test → Verify → Complete) generates process compliance rules:

| Structure Step | Generated Rule |
|---------------|---------------|
| "Start: Read task requirements + identify affected modules" | GOV-SESSION-010: Affected modules identified before coding |
| "Check: Load relevant steering files for those modules" | GOV-SESSION-011: Module-specific steering loaded |
| "Verify: Check against DEFINITION_OF_DONE.md" | GOV-SESSION-012: DoD check is the completion gate |

### From `session-governance.md` → Autonomy Mode

| Mode | Generated Behavior Rule |
|------|------------------------|
| Autopilot | GOV-SESSION-MODE: Complete task end-to-end; user reviews result |
| Supervised | GOV-SESSION-MODE: Yield after each file edit; user approves each change |

---

## Tier Assignment

| Rules | Tier | Rationale |
|-------|:----:|-----------|
| GOV-SESSION-BASELINE-01/02/03/04 | 1 | Core AI-DLC v1 methodology — active from Day 0 |
| GOV-SESSION-001 through 012 (from steering) | 2 | Full session discipline needs team context |

---

## Hook Mapping

| Hook | Event | Rules Enforced |
|------|-------|----------------|
| `session-discipline.json` | promptSubmit | GOV-SESSION-BASELINE-01/02/03/04, GOV-SESSION-002/007 |
| `pre-code-spec-check.json` | preToolUse (write) | GOV-SESSION-BASELINE-01, GOV-SESSION-001/003 |
| `post-task-governance.json` | postTaskExecution | GOV-SESSION-003/012 |

---

## Correction Escalation Model (From Built-in + Steering)

The session-discipline hook includes correction escalation detection:

```
Level 1 (Point Fix): Single wrong value → tell AI the specific fix
Level 2 (Pattern Fix): Same mistake in multiple places → update steering file
Level 3 (Design Fix): Logic structure wrong → fix in design docs
Level 4 (Restart): >30% wrong → abandon session, improve inputs
```

The hook detects loop patterns (same fix attempted twice) and recommends escalation.

---

## Phase Applicability

| Phase | Rules Active |
|-------|-------------|
| Setup | GOV-SESSION-BASELINE-01/02/03/04 (always) |
| Foundation+ | Full GOV-SESSION-* set (all steering-derived rules) |
