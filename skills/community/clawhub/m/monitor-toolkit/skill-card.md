## Description:

Creates configurable monitoring checks for systems, logs, operations alerts, deployments, and other user-defined targets, with scheduling and alerting handled by the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations engineers, and automation teams use this skill to define monitoring targets, checks, thresholds, schedules, and alerts for infrastructure, logs, deployments, and operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request command execution or API-style access without enough concrete limits.

Mitigation: Allow only clearly specified read-only diagnostic commands unless an operator explicitly approves a change.

Risk: Monitoring credentials or API keys could be over-scoped or exposed during operational use.

Mitigation: Use narrowly scoped credentials, keep secrets in environment variables or approved secret stores, and avoid logging keys or tokens.

Risk: Unattended scheduling, broad file writes, deployment actions, or production automation could affect live systems.

Mitigation: Run in least-privileged environments and require review before enabling write, deployment, or scheduled actions against production data or services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/monitor-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON status examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include monitoring targets, thresholds, schedules, alerts, diagnostic results, and remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
