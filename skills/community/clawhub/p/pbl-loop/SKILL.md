---
name: pbl-loop
description: Use when the user asks for learning goals, capability development, reflection, teaching, replication, transfer readiness, or applying a PBL loop in a real project context. Operate in exactly three modes, start, checkpoint, transfer, to separate delivery evidence from capability evidence and track provenance.
---

# PBL Loop (v0.1)

Use this skill for capability-learning loops in real work.
It is host-neutral and dependency-free.

## Trigger and boundary

Trigger only when the user explicitly requests:

- a learning goal or capability-development objective,
- reflection on what was learned versus what was delivered,
- transfer, teaching, or replication against an adjacent problem,
- a PBL-style growth loop in project context.

Do not trigger for:

- routine project status updates,
- delivery planning without learning/evidence intent,
- generic study explanations,
- final completion checks without a capability loop,
- requests to change project truth or governance state directly.

Keep exactly three modes: `start`, `checkpoint`, `transfer`.

## Start response contract (mandatory)

Treat `start` as a learning contract, not a full project plan.

If any key context is missing for:

- delivery goal,
- capability goal,
- evidence context,

complete the mandatory schema with explicit `unknown` values, then ask **exactly one focused question**. Do not ask additional questions or add a full project plan. The response must end with that question.

When context is sufficient:

- preserve the exact user delivery goal,
- record one bounded user-facing capability goal,
- keep all non-user-supplied details out of evidence fields,
- never invent counts, durations, thresholds, percentages, score bands, windows, deadlines, or acceptance gates,
- mark assistant additions as `source_status: proposed` and never convert them into hard requirements.

## Core invariants (v0.1)

- This skill is host-neutral. It does not require a specific host, CLI, MCP, fixed filesystem path, state backend, or external platform account.
- It does not require host metadata or proprietary runtimes.
- Preserve the real project delivery goal from user context. If unavailable, set `delivery_goal` to `unknown` and set status explicitly.
- Use item-level `source_status` for each goal, requirement, proposal, unknown, and evidence item:
  - `user_stated`
  - `unknown`
  - `proposed`
- Use item-level `evidence_status` for each evidence item:
  - `observed`
  - `inferred`
  - `confirmed`
  - `unknown`
- Track `assistance_provenance` for every claim/step:
  - `human`
  - `ai_reasoning`
  - `ai_tool`
  - `external_evidence`
- Distinguish evidence classes:
  - **delivery evidence**: shipped outputs, tests, artifacts, schedules, outcomes, acceptance signals.
  - **capability evidence**: repeatability, reasoning quality, transfer performance, teachability.
- Default operation is conversation-only and stateless.
- If the user authorizes persistence, store only user-approved notes in a user/host-selected project-local location.
- Never overwrite prior project truth.

## Four cognitive quadrants (state model)

Use these labels only for first-person capability/mastery claims, never for project status.

1. `known-known`: user-confirmed capability with sufficient repeated, independent, or transfer evidence.
2. `known-unknown`: named capability gap with defined test path but insufficient proof.
3. `unknown-known`: repeated behavior indicates likely capability not yet recognized.
4. `unknown-unknown`: anomaly or gap with no clear shape/test path yet.

Rules:

- Move from `unknown-known` only when behavior suggests likely capability and is explicitly documented.
- Move to `known-unknown` only when a gap is named and testable.
- Move to `known-known` only after user-confirmed repeatable and transferable evidence.

## Output schema (mandatory, all modes)

For every mode response, keep these top-level fields:

- `mode`
- `delivery_goal`
- `learning_goal`
- `user_stated_requirements`
- `assistant_proposals`
- `unknowns`
- `assistance_provenance`
- `capability_debt`
- `next_deliberate_challenge`
- `quadrant_before` and/or `quadrant_after`
- `delivery_evidence`
- `capability_evidence`

Each `delivery_goal`, `learning_goal`, `user_stated_requirements`, `assistant_proposals`, `unknowns`, `delivery_evidence`, and `capability_evidence` item must retain:

- `source_status`
- `evidence_status`
- `assistance_provenance`

`assistant_proposals` should be empty when no proposal is needed; otherwise every proposal item must be clearly marked with `source_status: proposed`.

## mode: start

Minimum required fields:

- `mode`
- `delivery_goal`
- `learning_goal`
- `quadrant_before`
- `user_stated_requirements`
- `assistant_proposals`
- `unknowns`
- `assistance_provenance`
- `capability_debt`
- `next_deliberate_challenge`
- `delivery_evidence`
- `capability_evidence`

Start logic:

1. Restate the delivery goal with explicit status. If absent, set `delivery_goal: unknown`.
2. Set one bounded first-person capability goal.
3. Set baseline `quadrant_before` only for that capability claim.
4. Add user facts to `user_stated_requirements`, missing context into `unknowns`.
5. Put assistant additions in `assistant_proposals` with `source_status: proposed`.
6. Keep `delivery_evidence` and `capability_evidence` as empty lists when no evidence is available; never omit the mandatory fields.
7. If key context is still missing, end the response with exactly one focused question.

## mode: checkpoint

1. Carry forward the delivery goal and previous schema context.
2. Add delivery/capability evidence updates and evidence status.
3. Set `quadrant_after` to show capability movement.
4. Keep `capability_debt` explicit.
5. Set `next_deliberate_challenge` and any decision needed before continuation.

## mode: transfer

1. Carry forward the delivery goal from context; do not redefine it as the transfer task.
2. Define one bounded adjacent problem in the same capability family.
3. Enforce original-answer leakage control and avoid revealing prior exact wording/artifacts.
4. Evaluate transfer for adaptability, explanation quality, and reuse.
5. Update `quadrant_before`/`quadrant_after` and `capability_debt`.
6. Use `evidence_status` for transfer judgments.

## Anti-fabrication rule

- Do not fabricate counts, durations, percentages, score bands, 24-hour windows, full intervention plans, or acceptance gates when missing.
- Use `unknown` or `proposed` states instead of invented concrete values.

## Fail-closed rule

Delivery polish and intervention quality do not prove capability. Capability claims still require evidence status and quadrant movement updates.

## Optional companion note

FlowGrid (https://github.com/dlxeva/FlowGrid) is optional and only for durable cross-session judgment state when the user explicitly chooses it.
