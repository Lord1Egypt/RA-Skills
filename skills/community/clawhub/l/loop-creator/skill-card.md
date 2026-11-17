## Description:

Builds supervised self-running agent loops that use a trigger, state file, objective pass/fail gate, stop condition, and guarded rollout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansraj316](https://clawhub.ai/user/hansraj316)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn recurring chores such as CI triage, PR checking, digests, dependency bumps, and documentation refreshes into supervised recurring agent workflows with objective gates and state tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact tells agents to ignore some mandatory skill-routing hooks, which may bypass intended control hierarchy.

Mitigation: Remove or replace that wording with hierarchy-preserving guidance before installation; require review of any instruction that conflicts with higher-priority system or platform rules.

Risk: Self-running loops can repeat commands, consume budget, or apply changes without enough supervision if configured too broadly.

Mitigation: Use narrowly scoped commands, objective stop conditions, manual proof runs, explicit max-iteration limits, and human approval for scheduled routines, hooks, commits, pushes, merges, or publish actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hansraj316/skills/loop-creator)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose loop procedure files, state-file structure, objective gate commands, command allowlists, rollout level, and proof-run reporting.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
