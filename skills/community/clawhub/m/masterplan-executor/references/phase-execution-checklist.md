# Phase Execution Checklist

The mechanical steps for executing a single build-roadmap phase, in order. Don't skip a step because the phase feels simple — simple-looking phases are exactly where a skipped self-audit lets a gap through.

```
[ ] 1. Ingest scope
    - Re-read every masterplan section this phase touches (features + acceptance
      criteria, tech stack entries, data model pieces, API contract, adaptive-system
      requirements, relevant production-readiness items)
    - List, explicitly, what "done" means for this phase per the masterplan's own
      Build Roadmap section

[ ] 2. Identify ambiguity before writing code
    - Anything unclear, underspecified, internally contradictory, or possibly outdated
      in what the plan says for this phase?
    - If yes: web_search (and web_fetch official docs where relevant) BEFORE writing
      the code that depends on the unclear part — never write it once and fix it later
      based on a guess

[ ] 3. Implement
    - Write the code to the standard in references/execution-standards.md
    - If this phase supersedes something from an earlier phase, delete the superseded
      code/config/flags as part of this step, not as a follow-up

[ ] 4. Self-test for real
    - Run the test suite (or the relevant subset)
    - Actually execute/run the feature, not just read the code back
    - Actually trigger the failure/edge-case paths this phase's error handling covers

[ ] 5. Self-audit against references/execution-standards.md
    - Go through the Universal checklist plus the relevant category-specific and
      adaptability sections
    - List anything that's a Blocker or Major finding
    - Fix every one before proceeding — do not defer

[ ] 6. Update docs/masterplan/execution-log.md
    - Phase status → done
    - What was actually built
    - Any research performed this phase (question / source / resolution)
    - Any deviation from the plan and why
    - Self-audit result (clean, or what was found and fixed)

[ ] 7. Commit at this phase boundary with a message that maps to the roadmap phase

[ ] 8. Only now move to the next phase
```

## If a phase can't be completed in one session

Stop at a clean sub-boundary if possible (e.g. after step 4/5 of a sub-feature, not mid-function). Record the exact stopping point in the execution log — not just "in progress," but specifically what's done and what's the next concrete step — so the next session (this skill or a human) can resume without re-deriving state from the code alone.

## If the masterplan itself is the blocker

If step 2's research reveals the plan is actually wrong (not just underspecified) — e.g. it names a deprecated approach, or two sections contradict each other in a way research can't reconcile — don't pick a side silently. Implement the researched-correct approach, log it clearly as a deviation with the reason, and if it changes user-facing behavior or a major architecture decision, surface it to the user before continuing past that point.
