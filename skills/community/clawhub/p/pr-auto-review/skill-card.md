## Description:

Automated PR review pipeline that analyzes PR diffs and CI/CD status, checks for potential secrets and service health issues, and posts a structured Discord notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run PR checks, summarize code review and service health findings, and notify a team Discord channel before or after merge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository and service-health details may be posted to an external Discord webhook destination.

Mitigation: Install only where external PR and health-check notifications are acceptable, and use a dedicated Discord webhook from a trusted secret store.

Risk: Real webhook URLs may be exposed when passed directly on shared command lines.

Mitigation: Avoid placing production webhook URLs in shell history, logs, or shared automation definitions.

Risk: Health checks may probe sensitive or unintended local services.

Mitigation: Use --skip-healthcheck or constrain health-check execution for sensitive environments.

Risk: Scheduled automation can repeatedly send external notifications.

Mitigation: Enable cron-based automation only when repeated external notifications are intended.

## Reference(s):

- [Discord Notification Formats](references/discord-formats.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/pr-auto-review)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown report with optional Discord webhook JSON payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save the report to a file; Discord notification content is truncated to fit webhook message limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
