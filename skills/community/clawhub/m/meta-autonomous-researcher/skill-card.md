## Description:

meta-autonomous-researcher is a distilled research-assistant skill that describes self-verification, reflection, and learner logging around autonomous research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to structure autonomous research tasks with added verification, reflection, and simple learner-recording behavior. Reviewers should confirm the claimed orchestration and self-evolution capabilities before relying on them for unattended workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates autonomous research, verification, orchestration, and self-evolution capabilities compared with the small learner logging script that is shipped.

Mitigation: Treat those claims as requiring review and supporting agent components before granting broad autonomy or relying on unattended verification.

Risk: Stored learning notes may be mistaken for trusted instructions or reliable memory.

Mitigation: Treat learner records as untrusted logs, review them before reuse, and avoid letting them override higher-priority instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-autonomous-researcher)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON learner records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local learner record when its script is run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
