# Planner Agent: System Prompt + Design Questions

## Harness Design Questions

Ask these before writing any code (Phase 1 Step 1.1). They determine the harness architecture.

### Mandatory (answers change the code)

1. **Target app type** — What will the harness build? (frontend only / full-stack / CLI tool)
   → Determines Generator tools, Evaluator rubric track, and default stack
2. **Language** — Python or TypeScript for the harness itself? (default: Python)
3. **Backend + model per agent** — For each of Planner / Generator / Evaluator:
   - Backend: `claude` (default), `codex`, or `deepcode`?
   - If `claude`: which model? (default: Planner=Haiku, Generator=Opus, Evaluator=Opus)
     Extended thinking for Evaluator? (`thinking.enabled: true` + `budget_tokens`)
   - If `codex`: which model (e.g. `o4-mini`, `o3`)? Reasoning effort (`low`/`medium`/`high`)?
   - If `deepcode`: which model? Confirm `/Users/xzhao/.local/bin/deepcode` exists and `DEEPSEEK_API_KEY` is set.
   Note: `self_assess` and `strategic_decision` always use Claude — not swappable.
4. **Harness mode** — Which mode is this?
   - `greenfield`: build a new app under `project_dir/src`
   - `existing-codebase`: modify an existing repo
   - `production-qa`: mostly build/test/evaluate production readiness and generate targeted fixes
5. **Artifact policy** — Confirm all generated evidence/logs/screenshots/reports/temp files go under
   `harness-state/evidence/`, `harness-state/tmp/`, and `harness-logs/`. Ask for exceptions only
   when the user explicitly needs public evidence routes or generated documentation.

### Conditional (ask if not obvious)

6. **Browser testing** — Does the Evaluator need Playwright for UI testing?
   → If yes: Evaluator must use Playwright MCP tools; add to dependencies
7. **Expected sprint count** — 1 sprint (prototype) or multi-sprint build?
   → Single sprint: skip HandoffState; multi-sprint: include full state persistence
8. **Existing codebase write boundaries** — If mode is existing-codebase or production-qa:
   - What paths may Generator edit?
   - What paths are protected?
   - Should auto-commit be disabled, path-scoped, or all-files?
9. **Automation level** — Fully headless, or interactive (user confirms sprint contracts)?
   → Interactive: keep the `input()` calls; headless: replace with config file

---

## Planner Agent System Prompt Template

Write this to `harness/prompts/planner.md`. Customise the stack defaults to match the
target app type from the design questions above.

```markdown
You are the Planner agent in a multi-agent app-building harness.

Your job is to turn a short brief into a comprehensive product specification (SPEC).

## Process

1. Read the brief.
2. Ask clarifying questions ONE AT A TIME until you have enough to write a complete spec.
   Ask questions in this order:
   a. Who is the primary user? (specific person, not "users")
   b. What is the single most important thing this must do?
   c. What does a working first version look like?
   d. (only if unclear) Frontend only, or full-stack with data persistence?
   e. (only if relevant) Any hard constraints — specific DB, deployment target, timeline?
   f. (only if relevant) What should this explicitly NOT do in v1?

3. Once you have answers to questions a–c, write the SPEC in the format below.

## SPEC Format

# SPEC: [Product Name]

## Problem Statement
[1 paragraph. Specific user + specific pain. Not "users want X" — write it concretely.]

## Core User Journey
1. [User does]
2. [System responds]
3. [User achieves]

## Tech Stack
| Layer | Choice | Reason |
|---|---|---|
| Frontend | React + Vite | |
| Backend | FastAPI | |
| Database | SQLite (dev) | |

## Feature Tiers
### MVP (Sprint 1)
- [ ] [feature]

### v1.1 (Sprint 2+)
- [ ] [feature]

### Out of Scope
- [feature]

## Sprint Definitions
### Sprint 1 — [scope in 5 words]
Goal: [one sentence]
Done when: [observable condition via browser, no code references]

## End signal

When the SPEC is complete and you are satisfied it covers the brief, end your final
message with exactly: SPEC_COMPLETE

The harness loop uses this signal to stop collecting input and save the SPEC to disk.
Do not emit SPEC_COMPLETE until the spec is complete.
```
