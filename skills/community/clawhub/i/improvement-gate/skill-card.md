## Description:

Validates executed improvement candidates through a six-layer quality gate and returns keep, reject, revert, or pending review decisions with audit receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill after an improvement executor produces ranking and execution artifacts to decide whether a candidate should be kept, reverted or rejected, or sent for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's scripts can restore or write files using paths from input artifacts, even though the documentation frames the gate primarily as verification.

Mitigation: Run it only in a tightly scoped workspace with trusted ranking and execution artifacts, and confirm rollback path containment before installation or use.

Risk: Human review state is managed through local review IDs and state files.

Mitigation: Use a controlled state root and validate review IDs before completing approvals or rejections.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/improvement-gate)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with bash commands and JSON receipt descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces gate decisions and audit receipts, and may create pending human review records.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
