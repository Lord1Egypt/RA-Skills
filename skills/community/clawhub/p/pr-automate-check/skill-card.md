## Description:

Automated PR submission pipeline for code review, service health validation, and Discord notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run automated pre-merge checks for GitHub pull requests. It fetches PR diff and status data, runs service health validation when available, and can post a concise status notification to Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs authenticated GitHub CLI commands against pull request data.

Mitigation: Use it only in trusted repositories with scoped GitHub credentials and review results before acting on them.

Risk: The skill can send PR and health information to an arbitrary Discord webhook.

Mitigation: Pass only approved webhook URLs and avoid sourcing webhook values from untrusted automation.

Risk: The skill can execute a local healthcheck helper when present.

Mitigation: Verify the installed healthcheck skill before enabling automatic cron or PR-event execution.

## Reference(s):

- [PR Automate Check on ClawHub](https://clawhub.ai/terrycarter1985/skills/pr-automate-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pull request metadata, health status, diff path, and optional Discord notification status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
