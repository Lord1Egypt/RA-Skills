## Description:

Guides developers through building an agent-commerce observability stack with OpenTelemetry tracing, GreenHelix metrics and events, anomaly detection, dashboards, alerting, SLA monitoring, and cost attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this guide to add tracing, metrics, alerting, dashboards, SLA checks, and cost attribution to multi-agent commerce systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telemetry examples may send customer, transaction, escrow, credential, or internal topology identifiers to external observability, webhook, or Slack destinations if copied directly into production.

Mitigation: Redact or hash sensitive identifiers, use allowlisted HTTPS destinations, and document retention and access controls for GreenHelix, Slack, and observability backends.

Risk: Illustrative webhook and alerting examples may be adapted with the wrong destinations or insufficient operational review.

Mitigation: Replace sample URLs with approved endpoints, review alert routing and escalation policies, and test behavior in the sandbox before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-observability-stack)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix agent schema](https://greenhelix.net/schemas/agent/1.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guide with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples require environment-specific telemetry, webhook, Slack, and observability backend configuration before production use.]

## Skill Version(s):

1.3.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
