## Description:

Deterministic external-memory execution loop using rules/goal/plan/progress/notes/lessons with strict preflight, one-step execution, and measurable lesson quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kdylan1010-alt](https://clawhub.ai/user/kdylan1010-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run tasks through a local file-backed memory loop that records rules, goals, plans, progress, notes, and lessons before executing one clear step at a time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on persistent local memory files that may accumulate sensitive task details.

Mitigation: Use it only in workspaces where persistent state is desired, and review the memory files before and after sensitive tasks.

Risk: Stored notes, progress, or lessons can steer later task execution if they become stale or inaccurate.

Mitigation: Review rules.md, goal.md, plan.md, progress.md, notes.md, and lessons.md during preflight before relying on the next action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kdylan1010-alt/skills/memory-driven-execution-loop)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance for stepwise agent execution and memory-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local markdown memory files: rules.md, goal.md, plan.md, progress.md, notes.md, and lessons.md.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
