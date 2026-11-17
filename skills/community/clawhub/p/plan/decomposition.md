# Decomposition — From Goal to Steps

Steps are claims about the future; the done-check is what makes each claim falsifiable. This file covers altitude, checks, slicing, dependencies, and the steps nobody writes.

## Altitude

- 3-7 steps per plan (canonical: SKILL.md, Plan Format). More than 7 = wrong altitude: group into milestones, plan the first milestone in step detail.
- Fewer than 3 while plan-needed signals fired = steps are hiding inside one line — "migrate the database" is four steps wearing a coat.
- Milestone = an independently valuable, demoable state: if the plan died here, what is shipped still stands. Step = one work session, completable without new human input; if a step contains a decision the human must make, split at the decision.

## Done-Checks

Every step names the observable that proves completion (canonical rule: SKILL.md, Core Rules). The catalog:

| Check type | Example |
|---|---|
| Artifact exists | migration file at the named path |
| Diff | patch/PR posted for review |
| Passing test | the named test, seen red before the fix, now green |
| Command output | health endpoint returns 200; dry-run prints the expected row count |
| Log line | "consumer connected" appears within 30s of start |
| Decision doc | "X vs Y, with the pick and the reason" |
| Human ack | explicit approval message on a named question |

- A check must be executable by the agent or observable by the human without interpretation. "Looks good" is not a check; "renders identically at the three breakpoints in the ticket" is.
- Activity-verb blacklist — these are hopes, not steps: investigate, explore, look into, handle, improve, review (bare). Convert: "investigate X" → decision doc; "review Y" → list of defects or an explicit pass; no conversion possible → spike (`strategies.md`).

## Slicing: Vertical by Default

- Vertical slice: the thinnest end-to-end path first — one endpoint, one record, one page rendered. Integration risk dies in step 1-2 instead of surfacing at the end, where it is most expensive.
- Horizontal layers (all of the schema, then all of the logic, then all of the UI) hide integration until the final merge. Legitimate only when the interface is contractual (published API spec, agreed schema) — the same precondition as Parallel (`strategies.md`).

## Dependencies

- For each step, name what it needs and what it unblocks. A step that nothing depends on and no goal consumes is scope creep — cut it.
- Within dependency constraints, order by information: the step most likely to invalidate the plan goes first (SKILL.md, Core Rules). Natural order and safe order differ; the migration that writes its rollback script first is exploiting that difference.

## The Steps Nobody Writes

Plans fail disproportionately on steps that were never written. Scan this list at plan time; each applicable item becomes a named step with its own check, not a footnote:

- Rollback script — written and tested before the irreversible step (`risk.md`)
- Backup, plus **verifying the restore** — an unverified backup is a checkbox, not a safety net
- Migration of existing data/state, not just the new schema
- Verification after the change — the deploy is not the last step; the check that the deploy worked is
- Communication: who needs to know before, during, after
- Cleanup: temp state, feature flags, parked branches
- Monitoring window: who watches what, for how long, after the change lands

## Sizing Steps by Risk

Granularity scales with risk, not uniformity. A 5-minute irreversible step deserves its own line with its own check; a 2-hour reversible refactor can be one line. Fine-grained around irreversible and novel steps, coarse on known reversible stretches — uniform granularity wastes detail where it is useless and starves it where it saves you.
