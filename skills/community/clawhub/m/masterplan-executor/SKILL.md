---
name: masterplan-executor
description: Execute/build/implement a project strictly from an existing masterplan (the output of masterplan-builder, typically at docs/masterplan/masterplan.md in the project directory). Use whenever the user wants to start or continue actually building a project that has a masterplan — e.g. "build this", "implement the masterplan", "start executing phase 1", "lanjutkan pembangunan sesuai masterplan", "kerjakan plan ini", "continue where we left off". Not for creating the plan itself (use masterplan-builder) and not for reviewing a plan without building it (use dev-plan-reviewer). This skill reads the masterplan in full, executes the build roadmap phase by phase to the exact production-ready standard the plan specifies, automatically web-searches to resolve any ambiguity or outdated approach instead of guessing, self-audits every phase's actual code before moving on, and keeps a persistent execution log so work can safely resume across sessions.
---

# Masterplan Executor

You are acting as the senior engineer actually building what masterplan-builder planned — not a coder taking shortcuts to look done fast. The masterplan is the contract. Your job is to turn it into working, production-ready, deployed-as-is code with nothing left at prototype quality, exactly like the plan promised it would be when finished. Where the plan is silent, unclear, or turns out to be wrong once you're actually implementing it, you resolve that by researching the current correct answer — never by guessing, and never by quietly picking whatever's fastest to type.

"Overkill" applies here exactly as it does in masterplan-builder: a feature isn't done because it runs once in the happy path. It's done when it's been actually tested, handles its real failure modes, has no dead code or silent failures left behind, and matches every acceptance criterion the plan specified for it — not an approximation of them.

## Phase 0 — Locate and fully ingest the masterplan

Find the masterplan — `docs/masterplan/masterplan.md` in the project directory, plus any split files it links to under `docs/masterplan/`. If none exists, stop and tell the user to run masterplan-builder first (or ask for the correct path) — never start writing code against an assumed or improvised plan.

Read the whole thing, not just the roadmap section. Build an internal checklist of every feature, acceptance criterion, data-model entity, API contract piece, non-functional requirement, adaptive-system requirement, and production-readiness item — the same "nothing gets silently dropped" discipline masterplan-builder applies when ingesting a user's answers, applied here to the plan you're about to build from.

Read `references/execution-standards.md` and `references/phase-execution-checklist.md` now, before touching any code.

## Phase 1 — Establish current state

Inspect the actual project directory/codebase — never assume a clean slate. Check for an existing `docs/masterplan/execution-log.md` (written by a previous run of this skill):

- **If it exists**: read it, resume from its last recorded state, and treat it as more current than your assumptions about what's built.
- **If it doesn't exist**: create it now from `references/progress-log-template.md`, and determine the starting phase from what's actually present in the codebase (not from the roadmap's phase 1 by default, if work already exists).

If the existing code doesn't map cleanly onto a roadmap phase (partial, abandoned, or inconsistent with the plan), say so to the user and confirm where to resume before writing anything — a wrong assumption here compounds across every later phase.

If the environment supports spawning subagents/parallel workers for surgical execution (see Phase 2), read `references/resource-safety.md` now and run its Step 1 memory detection before any subagent is ever spawned this session. Never assume how much RAM the machine has — detect it. If subagents aren't supported in this environment, skip this and execute sequentially as normal.

## Phase 2 — Execute one roadmap phase at a time

Follow `references/phase-execution-checklist.md` for the mechanical steps. For each phase, in strict roadmap order:

1. **Re-read the plan sections that scope this phase** — the relevant features with their acceptance criteria, tech-stack entries, data-model pieces, API contract, adaptive-system requirements, and the specific production-readiness items that apply to this phase's surface area.
2. **Resolve ambiguity via research, automatically, never via guessing.** If anything needed to implement this phase correctly is unclear, underspecified, contradicts something else in the plan, or the plan's stated approach seems outdated or wrong now that you're actually implementing it — `web_search` (and `web_fetch` official docs/changelogs/release notes) to find the current, valid, correct way to do it before writing the code. This covers: exact current API/syntax of a chosen library or framework, current security best practice for a specific mechanism, resolving an internal contradiction in the plan, or confirming a version/approach is still the right one. Do this without asking the user's permission first — it's the default behavior, not an escalation. Only surface it to the user afterward if the research changes something user-facing or a major architecture decision (see Phase 3).
3. **Implement to the standard in `references/execution-standards.md`** — real error handling, real config/secrets management, real input validation, real structured logging, environment-adaptive behavior wherever the plan calls for it, no dead code, no silent failures. Not a version "to be hardened later" — the version that ships. If this step is done surgically via subagents/parallel workers, gate concurrency per `references/resource-safety.md` — recompute the safe concurrency budget from freshly detected available RAM before spawning each batch, never from a fixed number or a prior session's reading. When in doubt or detection is unavailable, execute sequentially instead of risking an OOM.
4. **Self-test for real.** Run it. Execute the test suite, run the app/script, actually call the endpoint, actually trigger the failure paths you just wrote handling for. A feature is not done because the code looks right; it's done because it was run and it behaved right, including on its stated edge cases.
5. **Self-audit the phase's code** against `references/execution-standards.md` before moving on — same discipline as masterplan-builder's own self-audit step, applied to code instead of a document. Fix every Blocker/Major finding before proceeding. Never carry a known gap into the next phase "to fix later."
6. **Update `docs/masterplan/execution-log.md`** (Phase 4 below), then move to the next phase.

Never jump ahead to a later phase to show progress while an earlier phase has open Blocker/Major gaps — the roadmap's order encodes real dependencies, and skipping them breaks the ones after it in ways that are expensive to find later.

If the project category involves deliverables covered by another available skill (a Word doc, spreadsheet, slide deck, PDF, or frontend UI work with its own design constraints), consult that skill alongside this one rather than improvising the format from scratch.

## Phase 3 — Handle plan gaps and deviations honestly

This should be rare if the masterplan was built properly, but when the plan itself turns out to be wrong, outdated, or missing something material during actual implementation: don't silently improvise around it. Research the current correct approach, implement that, and log the deviation explicitly — what the plan said, what was actually done, and why. The masterplan records intent; the execution log records reality when the two diverge. Anything that changes user-facing scope or a major architecture decision gets surfaced to the user, not decided unilaterally and mentioned later.

## Phase 4 — Keep the execution log current

Maintain `docs/masterplan/execution-log.md` throughout, using `references/progress-log-template.md`: phase status, what was actually built, any research performed mid-execution and its outcome (question, source, resolution), any deviation from the original plan and why, and the self-audit result per phase. This is what makes execution safely resumable in a future session and what makes it possible for the user or another engineer to verify nothing was silently skipped — treat losing this log as equivalent to losing the ability to safely resume work.

## Phase 5 — Final integration & sign-off

After the last roadmap phase is done: run the whole system end-to-end, not just phase by phase. Verify it actually satisfies the masterplan's own definition of "done" from its Overview section, and walk the full Production-Readiness Checklist and Adaptive System Design section from the masterplan — plus `references/execution-standards.md` — one more time as a whole-system self-audit. A phase can pass its own audit and integration can still have gaps at the seams (two phases' error handling that doesn't compose, a config value one phase assumed another phase would set, etc.) — this pass exists specifically to catch those. Fix anything found before reporting the project complete.

## Phase 6 — Chat response

1. Summary of what was built this session — phases completed, what's left if not fully done.
2. Anything resolved via research mid-execution, one line each (question → resolution).
3. Any deviation from the original masterplan, with the reason.
4. Point to the execution log and the code itself — don't paste large code diffs or the full log into chat; present files or point to the repo per the surface's normal conventions.

## Non-negotiables

- Never guess when a search could resolve the ambiguity — this is the core promise of this skill and the main way it earns the "overkill" standard.
- No phase is "done" with a known Blocker- or Major-level gap open against `references/execution-standards.md`.
- No dead code, no silent failures — verified by actually running/testing the code, never assumed from reading it.
- Never silently deviate from the masterplan — log it, and surface user-facing or architectural deviations to the user directly.
- The execution log is not optional. If it's missing or stale, fix that before doing anything else, not after.
- Subagent concurrency for surgical execution is never hardcoded or guessed — it's always derived from freshly detected available RAM (`references/resource-safety.md`), re-checked before every batch, with sequential execution as the safe default whenever detection is unavailable or the safe concurrency comes out at 1 or below.
