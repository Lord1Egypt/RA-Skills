## Description:

Guidelines for reliable OpenClaw cron jobs: model pinning, absolute paths, timeouts, delivery config, and error recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure more reliable OpenClaw cron jobs with explicit model choices, absolute command paths, suitable timeouts, delivery settings, failure recovery checks, concurrency limits, and failure alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes fixed Telegram delivery and failure-alert recipients that may not belong to the installing user.

Mitigation: Review and replace Telegram recipients before installation or use, and only allow cron creation or updates after confirming delivery and failure-alert destinations.

Risk: Existing cron configurations may already contain the fixed Telegram recipient from the skill examples.

Mitigation: Check existing cron configurations for telegram:37134287 and replace it with an approved recipient before running scheduled notifications.

## Reference(s):

- [Cron Hardening ClawHub listing](https://clawhub.ai/hohobohan/skills/hobohan-cron-hardening)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides cron configuration patterns and operational checks for agent-authored schedules.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
