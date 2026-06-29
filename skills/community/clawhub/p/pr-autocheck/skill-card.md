## Description: <br>
PR Autocheck runs post-submit pull request checks by reviewing code diffs, checking service health, saving a combined report, and syncing a limited summary to Discord when a webhook is configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill in PR and CI workflows to review code changes, validate service health, persist a JSON report, and notify a team Discord channel when delivery is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted CI inputs could change the health-check command or Discord webhook destination. <br>
Mitigation: Install only where CI environment variables are controlled by trusted maintainers, and review HEALTHCHECK_CMD and DISCORD_WEBHOOK_URL before enabling automated post-submit use. <br>
Risk: Discord delivery may be unavailable or fail after the local report is generated. <br>
Mitigation: Use the saved report and surfaced discord_exit status to distinguish pending or failed delivery from a successful notification. <br>


## Reference(s): <br>
- [PR Autocheck on ClawHub](https://clawhub.ai/terrycarter1985/pr-autocheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON report with shell command usage and optional Discord embed summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports locally under reports/ and surfaces Discord delivery status.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
