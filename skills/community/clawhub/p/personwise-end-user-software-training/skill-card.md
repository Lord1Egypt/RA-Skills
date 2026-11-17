## Description:

Turns supplied training guides into an askable digital-human course for end-user software training.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Training teams and business users use this skill to turn supplied CRM, ERP, or other software training materials into a grounded interactive course for end users. The course is designed for learners who need practical software adoption training based on their organization's own materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update path can run service-provided commands.

Mitigation: Review each update command before approval and run only commands supplied through the trusted PersonWise workflow.

Risk: The installer uses weakened native publisher-signature checks on macOS and Windows.

Mitigation: Install only when PersonWise is trusted for the selected environment and review installation behavior before deployment.

Risk: The installed CLI persists in the user's profile and can act on selected training materials and account actions.

Mitigation: Use trusted source materials and accounts, and limit approvals to the requested course creation or update task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-end-user-software-training)
- [PersonWise publisher profile](https://clawhub.ai/user/personwiseai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with JSON inputs and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces course workflow guidance and may create or update PersonWise course artifacts through the PersonWise CLI after user approval and OAuth.]

## Skill Version(s):

2.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
