## Description:

Automates post-submit pull request checks by running deterministic code review, service health validation, combined JSON reporting, and optional Discord webhook delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill in CI, post-submit hooks, or on demand to review PR diffs, combine service health status, and notify a team Discord channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable health-check command can run in the target repository or CI environment.

Mitigation: Allow only trusted maintainers to set HEALTHCHECK_CMD and the healthcheck skill path, and run the skill in a controlled repository or CI environment.

Risk: Review and health data can be sent to a Discord webhook or saved as report artifacts.

Mitigation: Protect DISCORD_WEBHOOK_URL as a secret and review generated reports for sensitive repository or service details before sharing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/pr-autocheck)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [analysis, json, markdown, shell commands, configuration]

**Output Format:** [JSON reports, Discord embed payloads, saved files, and concise command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports under reports/ and may post a summarized notification when DISCORD_WEBHOOK_URL is configured.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
