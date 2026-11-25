## Description:

Connect OpenClaw to PB-Runner to review running, recovery, and goal data from Garmin or Apple Watch and draft training sessions for approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pb-runner](https://clawhub.ai/user/pb-runner)

### License/Terms of Use:

MIT-0

## Use Case:

Runners using OpenClaw with PB-Runner use this skill to review training and recovery data, track goals, and draft sessions for their schedule. Proposed changes are saved only after the runner explicitly approves them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth connects the agent to run and recovery information in the signed-in PB-Runner account.

Mitigation: Review the requested account access and sign in with the runner’s own PB-Runner account; use the data only to answer and coach that runner.

Risk: Coaching or recovery readings could be mistaken for medical advice.

Mitigation: For pain, injury, dizziness, chest pain, or unusual heart symptoms, direct the runner to a clinician instead of coaching through them.

## Reference(s):

- [PB-Runner OpenClaw setup guide](https://pb-runner.com/guide/openclaw)
- [PB-Runner getting started guide](https://pb-runner.com/guide)
- [PB-Runner FAQ](https://pb-runner.com/support)
- [PB-Runner privacy policy](https://pb-runner.com/privacy)
- [PB-Runner Garmin Connect IQ app](https://apps.garmin.com/apps/36345af4-1210-4b9f-9ffd-2c82ba0ed875)

## Skill Output:

**Output Type(s):** [Coaching guidance, Training plan drafts, Text, Shell commands, Configuration instructions]

**Output Format:** [Plain language and Markdown, with shell commands for setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance uses the runner's connected training data and units; proposed changes require explicit approval before saving.]

## Skill Version(s):

1.0.4 (source: artifact/SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
