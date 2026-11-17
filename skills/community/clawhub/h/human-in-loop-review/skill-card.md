## Description:

Routes risky, irreversible, privileged, financial, deployment, and privacy-sensitive agent actions to a human review queue with approval, rejection, summaries, and audit fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to pause risky autonomous-agent or automation actions for manual review before execution. It is intended for workflows that need approval queues, reviewer decisions, and audit records around actions with side effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment says the skill is presented as a human approval safety gate, but the artifacts show broken approval controls.

Mitigation: Do not rely on this skill as an enforcement layer for destructive, financial, deployment, privacy, or privileged actions unless the approval model is reviewed and backed by external controls.

Risk: The security assessment flags unrelated persistent self-learning behavior that stores preference and history data locally.

Mitigation: Disable or remove the learner unless local retention, path containment, and human review of any skill changes are explicitly controlled.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qq435912743/skills/human-in-loop-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review classifications, queue records, approval or rejection decisions, summaries, and local preference/history records when the learner is used.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
