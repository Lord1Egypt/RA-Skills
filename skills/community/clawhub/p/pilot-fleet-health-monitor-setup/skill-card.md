## Description:

Deploy a three-agent fleet health monitoring setup for web and database services, with a central alert hub that filters alerts and forwards notifications to Slack or PagerDuty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure web-monitor, db-monitor, and alert-hub agents for fleet health monitoring, peer handshakes, alert aggregation, and Slack or PagerDuty notification routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Required skills may be installed from mutable package names.

Mitigation: Use a trusted registry and pin exact versions or digests for each required skill before production installation.

Risk: Auto-approved trust handshakes can connect the wrong peer if identities are not checked.

Mitigation: Verify peer hostnames and identities before initiating or accepting handshakes.

Risk: Operational alert data may be forwarded to Slack or PagerDuty without clear field scoping.

Mitigation: Confirm webhook destinations and limit alert payload fields before enabling external notifications.

Risk: Deployment prefixes are used in hostnames and peer names.

Mitigation: Validate the prefix as a simple hostname-safe value before using setup commands.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-fleet-health-monitor-setup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands and JSON manifest examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Role-specific setup instructions for web-monitor, db-monitor, and alert-hub agents.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
