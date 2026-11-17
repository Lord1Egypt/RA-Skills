## Description:

Extracts recurring error and warning patterns from user-provided logs and turns them into structured alert-rule drafts for monitoring systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to convert pasted server, application, or system logs into draft alert rules for tools such as Prometheus, Grafana, or PagerDuty. It is best suited for recurring error or warning patterns that need consistent monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated alert rules may be incomplete, noisy, or mismatched to the target monitoring system.

Mitigation: Treat rules as drafts and review match patterns, thresholds, severity, and routing before deployment.

Risk: Logs can contain secrets, credentials, customer data, or other sensitive operational details.

Mitigation: Redact sensitive values before pasting logs unless agent-side processing of that data is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/log-to-alert)
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills)
- [Reference index](references/index.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with YAML or JSON alert-rule examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft alert rules and validation guidance; rules should be reviewed before use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
