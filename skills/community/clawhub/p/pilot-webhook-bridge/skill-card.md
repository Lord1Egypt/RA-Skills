## Description:

Forward Pilot Protocol events to HTTP webhooks for Slack, Discord, PagerDuty, and custom integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to forward Pilot Protocol event streams to team communications, alerting, monitoring, and workflow webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pilot event data can leave the user's environment when forwarded to external webhook services.

Mitigation: Use approved private destinations and redact secrets, personal data, customer data, and internal-only details before forwarding.

Risk: A global webhook can forward more events than intended.

Mitigation: Prefer selective subscriptions scoped to the required source, topic, and timeout.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-webhook-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces webhook setup and selective forwarding patterns for Pilot events.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
