# Approval — Plans and Humans

Validation only protects when the human actually engages with the plan. This file covers presenting plans, extracting real approval, handling skimmers and silence, and delivering bad news.

## Presenting a Plan

- Assume the human skims: the goal, the riskiest assumption, and the irreversible steps must survive a three-line read. The Plan Format's order (SKILL.md) already front-loads them — do not bury the irreversible line under step detail.
- Give the estimate as the range plus the high-end driver: "3-6h; high end fires if the export needs schema changes." A bare range invites the human to hear only the low number.

## The Approval Question

- "Ready to start?" invites a reflex yes. At L3+, ask one specific question whose answer proves the plan was read — point it at the irreversible step: "Step 4 drops the old index after verification — is Tuesday's backup current?"
- A substantive answer to that question is approval. An instant "yes" to "ok?" is a skim, and a skim before an irreversible step is a safety net made of paper.

## Skim-Approvers

- Repeated instant approvals on L3/L4 plans = validation has become theater. Propose the honest version: "I'll start these without asking and pause only before irreversible steps." Record the change (SKILL.md, Learning Loop); types in `always_validate` keep validation regardless.
- A user who consistently trims your plans is data: bias that user's per-type defaults one level down (`outcomes.md`, Feedback Questions).

## "Just Do It"

- Record it as a scope preference (SKILL.md, Configuration areas); drop one depth level for that task type.
- The floor never drops: an irreversible step still gets named before execution even when the plan doc is waived — one line, not a document: "Doing X now; note the delete in step 2 is not undoable."

## Silence

- No reply to an L3/L4 validation request is not approval. Execute reversible prep steps; never cross an irreversible boundary on silence.
- Re-ask once with the specific question (not a bare "ping"); still nothing → park the plan with state saved (`long-horizon.md`) and say what you are waiting on.

## Re-Approval

- Materially different — any of: a change to irreversible steps, a new high estimate beyond the approved range, a changed goal → re-approval at L3+ (canonical: SKILL.md, Executing Against The Plan).
- Cosmetic — reordering reversible steps, wording, step merges with identical checks → announce at the next checkpoint; no re-approval.

## Checkpoint Communication

Each checkpoint carries exactly three things: what is done (with check results), what is still changeable, and the one decision needed now. A checkpoint where nothing is decidable is a status update — cut it (`strategies.md`, Checkpoint).

## Bad News

Announce deviations at the deviation, not retroactively: what changed, the impact on estimate and goal, the options with your pick. What burns trust is rarely the slip itself — it is the human discovering it later than you knew it.
