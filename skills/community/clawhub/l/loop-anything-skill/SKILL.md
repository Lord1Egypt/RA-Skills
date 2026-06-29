---
name: loop-anything-skill
description: Improve important deliverables by looping them through multiple isolated AI reviewers, each evaluating from a different angle, until all reviewers give full approval (Score 120).
metadata:
  display_name: "Loop Anything Skill"
  version: "1.0.0"
  tags:
    - subagents
    - review-loop
    - quality-gate
    - deliverables
  categories:
    - agent-workflow
    - quality
  default_prompt: "Use Loop Anything Skill on this deliverable. First identify the artifact's true job, then create at least 2 isolated subagents representing different sides of the target outcome. Revise until every subagent returns PASS with Score 120."
  aliases:
    - loop-anything
    - multi-subagent-loop
    - 120-review-loop
  expected_cost: medium_to_high
---

# Loop Anything Skill

> **If you are a human reader:** tell your agent "Use Loop Anything on [your deliverable]" — the agent runs the full workflow automatically.

Apply to any important deliverable — topic, prompt, plan, code, design, document, workflow, or decision — where genuine multi-perspective review adds value.

The core rule:

- create **2-3 isolated subagents**
- use the subagent mechanism of the **current runtime**
- each subagent represents a **different side of the target outcome**
- revise until **every subagent returns `PASS` with `Score: 120`**

> **For agents — start here:** Before executing the Loop Workflow, complete these steps in order:
> 1. Read `templates/reviewer-packet.md` — bounded packet format
> 2. Read `templates/reviewer-output.md` — verdict structure and Score scale
> 3. Read `references/facet-patterns.md` — facet selection guidance
> 4. Read `references/runtime-compatibility.md` — identify your runtime's subagent mechanism
> 5. Complete the **Pre-loop checklist** at the top of the Loop Workflow section.
>
> Then begin at **Loop Workflow step 1** (the numbered loop steps, not the pre-loop checklist).
>
> **Done when:** every selected subagent returns `PASS` + `Score: 120` in the final review (steps 10–11).

## Key Terms

- **Subagent**: an isolated reviewer evaluating one facet of the deliverable from its bounded packet only.
- **Facet**: the review angle a subagent uses, protecting against one specific failure mode.
- **Bounded packet**: the self-contained context sent to each subagent — the fields defined in `templates/reviewer-packet.md`, nothing more.
- **Score 120**: zero remaining reservations on this facet. 0–119 means REVISE. Full scale in `templates/reviewer-output.md`.
- **Degraded fallback**: sequential self-review by the same agent when isolated subagents are unavailable; disclosed as advisory only.
- **REVISE**: any REVISE from any subagent triggers a full revision round — the revised artifact goes to all selected subagents.
- **Manifest**: `loop-run-manifest.json` — tracks runtime, isolation, facets, and verdicts; instantiated from `templates/loop-run-manifest.json` into the working directory. Required for every run.
- **Private ledger**: `templates/issue-ledger.md` — the agent's internal round-by-round issue tracker; stays with the main agent only.

## First Principle

Each subagent must represent a genuinely different side of the target — a failure mode the others would miss. Start from the deliverable's goal, identify the real tensions inside it, and let those tensions define the subagents. For patterns by artifact type, see `references/facet-patterns.md`.

## Artifact First

Identify the deliverable's true job before selecting facets — what it must accomplish across all relevant success dimensions. Facets evaluate this true job.

## Subagent Selection

Select 2-3 subagents with this structure:

```text
Artifact: {{WHAT_IS_BEING_DELIVERED}}
True job: {{WHAT_THIS_ARTIFACT_MUST_DO}}
Subagents:
  1. {{FACET_A}} — represents {{SIDE_A}}
  2. {{FACET_B}} — represents {{SIDE_B}}
  3. {{FACET_C_OPTIONAL}} — represents {{SIDE_C}}
Why these are different: {{THE_USEFUL_TENSION}}
```

**Facet distinctness check:** For every pair, complete: "The artifact could pass Facet A yet fail Facet B if [condition]." Redefine any pair where this cannot be completed, up to two attempts; after two unsuccessful attempts, report a blocker and request user clarification. The facet set is fixed once round 1 begins.

## Isolation Rules

Each subagent receives only its bounded packet — the fields defined in `templates/reviewer-packet.md`. The private ledger stays with the main agent only.

**Isolation probe:** each time a subagent is created, ask it "Can you see any conversation or context prior to this prompt?" A confirmed visible context sets `isolation_confirmed: false` and switches to the degraded path. A mid-round probe failure releases all subagents created in that round and re-runs the full round on the degraded path. For Tier 2 platforms (where isolation is possible but not guaranteed), also run the full probe from `references/runtime-compatibility.md`; treat unconfirmed platforms as Tier 2 when that file is unavailable.

## Reviewer Packet

Use `templates/reviewer-packet.md` for the packet structure and `templates/reviewer-output.md` for the output format, Score scale, and PASS conditions.

## Loop Workflow

**Pre-loop checklist (once, before step 1 — none of these repeat):**
- **A. Runtime mapping:** Run the Runtime Mapping procedure in the Degraded Fallback section.
- **B. Manifest init:** Instantiate `templates/loop-run-manifest.json` as `loop-run-manifest.json` in the working directory; record runtime platform and isolation status. (Facets added after step 2.)
- **C. Ledger init:** Initialize the private ledger as an empty table.

Run this loop:

1. Identify the artifact's true job. *(First round only.)*
2. Select facets via Subagent Selection, then add them to the manifest. *(First round only.)*
3. Draft or revise the artifact (first round: initial draft; subsequent rounds: synthesized fixes from the ledger).
4. Create one isolated subagent per facet and send it the bounded packet. All selected facets receive the artifact every round, including those that previously returned PASS.
5. Collect all verdicts. Update the ledger with this round's issues. Record verdicts and scores in the manifest. Treat a missing or errored verdict as REVISE: retry once; report a blocker if it fails again.
6. On any score below 120: check for cross-facet contradictory directives that cannot both be resolved in the same revision — escalate those to the user. Otherwise synthesize defects privately, evaluate step 7, then return to step 3. Maximum 5 rounds; report a blocker if not converged.
7. **Stuck detection:** when the same must-fix issue recurs across two consecutive rounds with no substantive change directly addressing it, stop and report a blocker. Resolution is verified only by a subagent returning PASS without that issue.
8. All facets PASS at Score 120 → proceed to step 9.
9. Declare the artifact final.
10. Create new isolated subagent instances for all facets and send the final artifact. Apply the same error-handling as step 5.
11. Deliver when all final reviews return PASS + Score 120. On a REVISE, make one targeted revision (must-fix issues only, no new content) and re-run once with new instances. Report a blocker if still not passing. After all final reviews pass: save reviewer outputs as `reviewer-[facet-label].txt`, then run `python scripts/validate_loop_review.py --manifest loop-run-manifest.json reviewer-a.txt reviewer-b.txt [...]`. For content-validation errors, fix the flagged fields and re-run once; for script-execution failures, go directly to manual field verification. Use manual field verification when file I/O is unavailable.

"All passed", "都通过", "approved" and equivalents mean every selected subagent returned `PASS` as defined in `templates/reviewer-output.md`.

## Degraded Fallback and Tool Limits

> **Two parts:** (1) **Runtime Mapping** — required for every run; (2) **Degraded path** — when isolated subagents are unavailable.

**Runtime Mapping (run once, pre-loop):**

1. Identify the delegation mechanism the current runtime exposes.
2. Prefer isolated child agents; use sequential execution when concurrency is limited.
3. Run the isolation probe (Isolation Rules). For Tier 2 platforms, also run the probe from `references/runtime-compatibility.md`.
4. Mark the run as degraded when no isolated mechanism is available.
5. Release each subagent immediately after its verdict is collected. See `references/runtime-compatibility.md` for platform-specific cleanup patterns.

When a reference file is missing, note it in the manifest, apply inline definitions from SKILL.md, and mark the run as degraded.

**Degraded path (sequential self-review):**

1. Disclose that isolation is unavailable and the run is degraded.
2. For each facet, run a self-review pass with explicit framing: "Reviewing as [Facet Name]. Mission: [mission]. Reasoning only from this facet's bounded packet."
3. Produce output per `templates/reviewer-output.md`; set `runtime.degraded: true` in the manifest.
4. Treat the run as advisory and disclose "degraded fallback — all reviews by the same agent; perspective independence is limited and unverified."

The 5-round maximum and stuck-detection rules apply equally here. When the user has explicitly requested Loop Anything, disclose degraded status rather than silently substituting a self-review.

**Manual field verification** (when file I/O is unavailable): confirm each reviewer output contains `Verdict: PASS`, `Score: 120`, `Must-fix issues: - none`, non-empty `Evidence checked`, and a 120-level approval statement. Record "manual field check performed" in the `Mechanical validation` field of `templates/final-summary.md`.

## Mandatory Run Artifacts

Required for every run regardless of platform:

- **`loop-run-manifest.json`** — prerequisite for any approval claim; instantiated from `templates/loop-run-manifest.json` and updated each round with runtime, isolation, facets, verdicts, and evidence.
- **`templates/final-summary.md`** — delivered with the final response.
- **Reviewer outputs** (`reviewer-[facet-label].txt`, one per facet, final round) — required for validation.

Manifest acceptance criteria: 2+ distinct facets, true isolation, `degraded: false`, non-empty evidence, all final reviewers PASS + Score 120.

## Reference Files

Apply SKILL.md definitions as fallback if any file is missing; mark the run as degraded.

- `templates/reviewer-packet.md` — bounded packet format
- `templates/reviewer-output.md` — reviewer output format
- `templates/issue-ledger.md` — private ledger format
- `references/facet-patterns.md` — facet selection patterns by artifact type
- `references/runtime-compatibility.md` — runtime mapping and isolation tiers
- `references/evidence-guide.md` — evidence expectations by artifact type
- `scripts/validate_loop_review.py` — final-round validation only

## When To Stop

Report a blocker when any of these conditions is met:

- the deliverable has no defined content to review
- two facets issue contradictory must-fix directives that cannot both be resolved — escalate to the user
- a must-fix issue recurs without new actionable detail
- tools fail repeatedly, budget is exhausted, or further iteration cannot make meaningful progress

Blocker format: `Blocked at: / Reason: / Evidence: / What was tried: / User decision needed:`

## Final Response

Deliver the final revised artifact with a concise summary:

- artifact created or updated
- subagents selected and what each represented
- review rounds run
- final verdicts and scores
- all subagents at PASS + 120: yes / no
- remaining risks, or `none`