## Description: <br>
Automates pull request review by collecting PR and CI data, running service health checks, scanning diffs for likely secrets, and optionally posting a Markdown summary to Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitHub pull requests, check CI and local service health, identify likely hardcoded secrets in diffs, and share a concise report with a trusted Discord channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord notifications may share PR titles, authors, changed-file names, CI results, and health-check output outside the repository environment. <br>
Mitigation: Use a Discord webhook only for trusted channels approved to receive that information. <br>
Risk: The GitHub CLI reads pull request metadata, diffs, and check status using the credentials available in the local environment. <br>
Mitigation: Run with least-privilege GitHub authentication in repositories where that access is intended. <br>
Risk: Health checks can execute an installed healthcheck helper or probe common local service endpoints. <br>
Mitigation: Use --skip-healthcheck when local probing or delegated health checks are not desired. <br>


## Reference(s): <br>
- [Discord Notification Formats](references/discord-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional Discord webhook payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the report to a file and truncates Discord content to fit webhook message limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
