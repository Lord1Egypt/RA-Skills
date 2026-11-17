## Description:

Helps an agent inspect, triage, summarize, export, and safely update GitHub security alerts for code scanning, Dependabot, malware, and secret scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nick2bad4u](https://clawhub.ai/user/nick2bad4u)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to review GitHub repository security posture, export alert data for triage, and apply carefully reviewed alert state updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface sensitive security alert details, including secret scanning context.

Mitigation: Use a minimally scoped GitHub token, keep secret values redacted by default, and avoid placing sensitive values in chat, logs, reports, issues, or commits.

Risk: The skill can propose or execute alert state changes, including bulk dismissals or resolutions.

Mitigation: Run dry-run commands first, review selected alerts and comments carefully, and apply mutations only with the corresponding GitHub permissions.

## Reference(s):

- [Server-resolved source repository](https://github.com/Nick2bad4u/Github-Security-CodeScanning-Alerts-Skill)
- [ClawHub skill page](https://clawhub.ai/nick2bad4u/skills/github-security-codescanning-alerts-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and optional JSON-producing commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose GitHub REST API operations and dry-run alert updates that should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
