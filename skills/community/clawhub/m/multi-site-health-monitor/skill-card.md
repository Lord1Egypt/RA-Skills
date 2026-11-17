## Description:

Monitors dozens of websites with configurable health checks, auto-restart alerts, intelligent alert routing, uptime tracking, performance monitoring, and automated incident response across multiple domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to design and configure health checks, alert routing, uptime reporting, and incident response workflows for multiple websites and services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages automated restarts, rollbacks, remote SSH commands, webhook actions, and cloud infrastructure actions.

Mitigation: Keep restart, rollback, AWS, SSH, and webhook actions disabled unless each target and command is explicitly approved, scoped, logged, and reversible.

Risk: Monitoring and alerting setup can require API keys and service credentials.

Mitigation: Use least-privilege API keys and avoid pasting real bearer tokens into prompts or shared configuration.

Risk: Long-running deployment guidance may affect production services if monitoring actions are misconfigured.

Mitigation: Review generated configurations before deployment and test endpoints, thresholds, alert routing, and rollback behavior in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/multi-site-health-monitor)
- [Artifact homepage](https://github.com/ncreighton/empire-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include monitoring configurations, alert payloads, incident response steps, and integration setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
