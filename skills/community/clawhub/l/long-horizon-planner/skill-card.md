## Description:

Long Horizon Planner helps agents decompose high-level goals into dependency-based milestone DAGs, compute topological order and critical paths, recommend next executable milestones, and generate progress reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan long-running, multi-step work by creating milestone plans, tracking dependencies, identifying critical paths, and producing Markdown progress reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learner can preserve user preferences, error notes, and usage history in the skill directory.

Mitigation: Avoid recording sensitive project details in preferences or notes, and review persisted learning data before sharing or publishing the skill directory.

Risk: The skill encourages learned content to be written back into its own instructions, which can affect future agent behavior.

Mitigation: Do not allow automatic SKILL.md write-back without human review; inspect proposed instruction changes before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/long-horizon-planner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON plan files, and Markdown progress reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planner operations are local and deterministic; learner operations may persist preferences, error notes, and usage history in the skill directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
