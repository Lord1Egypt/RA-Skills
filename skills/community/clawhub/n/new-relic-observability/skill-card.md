## Description:

Monitor applications, infrastructure, logs, synthetic checks, and cloud services in New Relic. Configure alerts, manage dashboards, query telemetry data with NRQL, set up synthetic monitors, manage workloads, configure notification channels, and track deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill in OpenClaw to monitor New Relic telemetry, query NRQL, inspect applications and infrastructure, and manage alerts, dashboards, synthetic monitors, workloads, users, API keys, and cloud integrations through ClawLink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad administrative New Relic access through a persistent third-party ClawLink plugin and hosted credential custody.

Mitigation: Install only if ClawLink is trusted with New Relic account access; prefer a dedicated least-privilege credential and start with read-only permissions where possible.

Risk: Write and destructive actions can modify or delete New Relic dashboards, policies, users, API keys, monitors, workloads, and related resources.

Mitigation: Require explicit review before user, API-key, account, alert, dashboard, monitor, cloud-integration, or deletion actions, and preview targets and effects before execution.

Risk: Some operations can remove custom state or have limited recovery, including dashboard updates, dashboard deletion, and golden metric or tag resets.

Mitigation: Fetch existing configuration first, preserve required identifiers such as dashboard page and widget GUIDs, and confirm backups or recovery expectations before making changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/new-relic-observability)
- [New Relic NerdGraph API Reference](https://docs.newrelic.com/docs/apis/nerdgraph/)
- [New Relic NRQL Reference](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/)
- [New Relic Alert Policies](https://docs.newrelic.com/docs/alerts-applied-intelligence/new-relic-alerts/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=new-relic-observability)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include New Relic NRQL, GraphQL-backed ClawLink tool calls, and confirmation prompts before write or destructive actions.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
