## Description:

AI compute sales teams use this skill to collect customer GPU usage data, generate usage and efficiency reports, and identify optimization opportunities, anomaly alerts, cost trends, capacity needs, and churn-risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, customer success, and AI infrastructure teams use this skill to turn customer GPU telemetry into weekly or monthly utilization, cost, alert, optimization, and capacity-planning reports. It supports review preparation, renewal discussions, upsell analysis, and proactive intervention for at-risk customers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer GPU telemetry is stored in a local metrics database and may contain sensitive operational or customer data.

Mitigation: Restrict filesystem permissions for the local data directory, treat exported reports as sensitive, and review data handling before production use.

Risk: The invocation example uses an unpinned npx package command.

Mitigation: Use a pinned ClawHub CLI or package version for production workflows.

Risk: Reports and alerts can be generated from sample data when no matching real telemetry exists.

Mitigation: Remove the sample-data fallback or require an explicit demo mode before relying on generated reports for customer decisions.

## Reference(s):

- [Pans Gpu Monitor on ClawHub](https://clawhub.ai/dashiming/skills/pans-gpu-monitor)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Analysis]

**Output Format:** [Markdown reports and terminal text output with tabular metrics, alerts, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can import CSV or JSON telemetry and stores local metrics before generating weekly reports, monthly reports, or anomaly alerts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
