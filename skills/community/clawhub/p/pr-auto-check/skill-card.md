## Description:

Automated PR submission pipeline: run code review, verify service health, and post the full result to a Discord channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to collect pull request CI status, changed-file summaries, service health results, and code-review findings, then notify a Discord channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PR metadata, CI status, changed-file names, and service health summaries may leave the repository environment through a Discord webhook.

Mitigation: Use only where that information is approved for sharing, restrict the webhook to the intended Discord endpoint, and avoid exposing webhook secrets in shell history or logs.

Risk: The pipeline may run a local health-check script whose provenance is not verified by this skill.

Mitigation: Prefer a fixed, trusted health-check script path and review the installed healthcheck skill before enabling automated use.

## Reference(s):

- [PR Auto-Check output format](references/output-format.md)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/pr-auto-check)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Human-readable Markdown or JSON report with shell commands for collection and notification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a temporary JSON result file and send selected PR, CI, diff, and health details to a configured Discord webhook.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
