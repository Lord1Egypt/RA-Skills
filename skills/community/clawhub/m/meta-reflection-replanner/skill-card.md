## Description:

A meta-skill distilled from reflection-replanner that adds self-verification, self-reflection, super-agent orchestration, and persistent learning for iterative replanning tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced agent users use this skill to analyze failed plans, classify likely causes, revise the plan, and add verification and reflection steps for repeated improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to keep persistent local learning state, including usage history, error patterns, and user preferences.

Mitigation: Inspect or delete learned_patterns.json periodically and treat it as untrusted local data.

Risk: The skill describes automatic updates to its own SKILL.md after repeated errors or usage thresholds.

Mitigation: Remove or disable automatic instruction-rewrite behavior unless a user explicitly reviews and approves the change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-reflection-replanner)
- [ClawHub publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured replanning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May record local usage history, error patterns, and user preferences when the learner script is used.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
