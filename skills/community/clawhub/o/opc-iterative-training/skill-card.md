## Description:

Helps an agent improve local skills by comparing freestyle responses with skill-guided execution and turning reusable strengths into skill updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to run training cases, compare freestyle and skill-guided outputs, and update local skill files and training logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly read and modify local skill files, including through passive or scheduled training triggers.

Mitigation: Require explicit approval for each training run, specify the exact target skill path, and review all proposed changes before any write.

Risk: Skill updates based on training comparisons could introduce incorrect guidance or regress existing behavior.

Mitigation: Use version control or backups for rollback, review diffs, and backtest updated skills against prior cases before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-iterative-training)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance, training records, comparative analysis, and edited skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create training artifacts under ./Skill训练 and propose or apply updates to target skill files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
