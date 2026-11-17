## Description:

Connects a runner's PB-Runner data to an AI coach for recovery-aware training advice and draft sessions that are saved only with the runner's approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pb-runner](https://clawhub.ai/user/pb-runner)

### License/Terms of Use:

MIT-0

## Use Case:

Runners use this skill with OpenClaw to review their runs, recovery, goals, and schedule, receive coaching and draft training sessions, and approve any proposed changes before they are saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the coach exposes personal running, recovery, profile, goal, and schedule data to the agent.

Mitigation: Connect only with the runner's consent, use the data only for their coaching, and disconnect with `openclaw mcp logout pbrunner` when access is no longer wanted.

Risk: An unreviewed training-plan change could be saved to the runner's schedule.

Mitigation: Show each proposed change and save it only after the runner explicitly approves it in the conversation.

Risk: Coaching advice could be mistaken for medical guidance when a runner reports concerning symptoms.

Mitigation: Refer pain, injury, dizziness, chest pain, or unusual heart symptoms to a clinician instead of coaching through them.

## Reference(s):

- [PB-Runner OpenClaw setup guide](https://pb-runner.com/guide/openclaw)
- [PB-Runner getting started guide](https://pb-runner.com/guide)
- [PB-Runner privacy policy](https://pb-runner.com/privacy)
- [PB-Runner skill on ClawHub](https://clawhub.ai/pb-runner/skills/pb-runner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown with setup commands and training-plan drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Training-plan changes require explicit user approval before saving.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
