## Description:

Monitors end-to-end business process data, configures anomaly thresholds, sends alerts, and summarizes incidents for workflows such as fulfillment, inventory sync, payments, and data pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams, developers, and data engineers use this skill to define monitoring objects, configure thresholds and data sources, route Feishu alerts, and generate incident summaries for business workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The monitoring daemon may keep running in the background.

Mitigation: Run it under a low-privilege account, monitor its process lifecycle, and stop or supervise it with an approved process manager.

Risk: Alert content may be sent to Feishu or configured webhooks.

Mitigation: Avoid sensitive data in alert messages and restrict webhook or bot credentials to the intended recipients.

Risk: Temporary PID, log, and cooldown files under /tmp may be unsafe for production use.

Mitigation: Review or replace the temporary file handling before production deployment.

Risk: Monitoring data sources can require operational credentials.

Mitigation: Use dedicated read-only monitoring credentials and keep secrets in environment variables or an approved secrets manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/process-data-monitor-claw)
- [Alert rules](references/alert-rules.md)
- [Data sources](references/data-sources.md)
- [Metrics library](references/metrics-library.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration snippets and Bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include monitoring configuration, alert rules, and operational commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
