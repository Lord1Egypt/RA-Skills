## Description:

Bootstraps new OpenClaw users with guided setup and configurable feature introductions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dukesky](https://clawhub.ai/user/dukesky)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to complete first-run setup, create starter workspace files, and receive scheduled introductions to core OpenClaw capabilities at their chosen pace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists personal setup data in workspace files.

Mitigation: Provide only necessary onboarding details, avoid sensitive contact information, and review USER.md and ONBOARDING_PROGRESS.md after setup.

Risk: The skill schedules recurring onboarding messages through a cron job.

Mitigation: Confirm the schedule and delivery channel, and know how to pause or delete the onboarding cron job before installation.

Risk: The artifact includes unsafe guidance about giving credentials to the agent.

Mitigation: Do not provide passwords, recovery codes, private keys, or long-lived tokens to the agent.

## Reference(s):

- [OpenClaw User Onboarding on ClawHub](https://clawhub.ai/dukesky/skills/openclaw-user-onboarding)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON-like cron job configuration, and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update USER.md, SOUL.md, HEARTBEAT.md, ONBOARDING_PROGRESS.md, and a recurring onboarding cron job.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
