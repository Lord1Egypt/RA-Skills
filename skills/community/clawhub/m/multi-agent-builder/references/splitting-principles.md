# Agent Splitting Principles (Role Discovery Stage)

Use these principles before finalizing role count.

## A. Split when (positive signals)

1) **Context accumulates independently**
- Each role builds long-lived context that should not pollute others.
- Example: domain research memory vs writing style memory.

2) **Different memory / expertise cores**
- Roles require distinct knowledge systems, not just different tools.
- Example: security threat modeling vs growth channel strategy.

3) **Workflow is operationally independent**
- A role can run as a self-contained pipeline with clear inputs/outputs.
- Example: data collection pipeline vs implementation pipeline.

4) **Different risk boundaries or permissions**
- One role needs elevated capabilities while others should stay restricted.
- Split to enforce least privilege.

5) **Parallelism has real throughput value**
- Splitting reduces cycle time because tasks can run concurrently.

## B. Do NOT split when (negative signals)

1) **Only tools differ, context is the same**
- Keep one role and switch tools as needed.

2) **Only output format differs**
- Same core cognition, different channel/template => use one role + templates.

3) **Tasks require constant tight back-and-forth**
- If two roles must synchronize continuously, merge them to reduce coordination tax.

4) **Stage-only separation of one cognitive thread**
- Requirement analysis and architecture design are often two stages of one owner unless scale/risk requires split.

5) **Split increases overhead more than quality**
- If handoff cost > quality gain, do not split.

## C. Practical thresholds

- Default team size target: **3-6 specialist roles + 1 team-leader**.
- If >8 specialist roles, require explicit justification per added role.
- Every added role must satisfy all three:
  1. unique primary artifact
  2. unique decision authority
  3. measurable cycle-time or quality gain

## D. Merge triggers (during operation)

Merge two roles when any persists across runs:
- repeated duplicate outputs
- frequent contradictory decisions
- >30% handoff messages are clarification-only
- SLA misses mainly caused by coordination, not execution

## E. Split triggers (during operation)

Split one role when any persists across runs:
- context window pressure causes quality drops
- mixed objectives cause unstable output
- permission conflicts (one role needs risky tools occasionally)
- repeated bottleneck at one overloaded role

## F. Output requirement at discovery stage

For each proposed role, include:
- why_split_or_not (one line)
- unique_artifact
- authority_boundary
- dependency_count
- expected_parallel_gain

If any field is weak/empty, downgrade role to optional or merge.
