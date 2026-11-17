## Description:

Deploy an autonomous warehouse orchestration system with four agents for robot fleet coordination, inventory tracking, pick optimization, and dock scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and warehouse automation teams use this skill to configure a four-agent autonomous warehouse setup that coordinates robot dispatch, inventory state, pick waves, and dock events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents high-impact setup and messaging authority across warehouse roles.

Mitigation: Review the setup before installation and use it only in a controlled, least-privileged warehouse environment.

Risk: The setup depends on installed skills, pilotctl, clawhub, and a running daemon.

Mitigation: Pin and verify each installed dependency before enabling the setup.

Risk: Peer trust and data-sharing behavior may expose operational messages if identities are not checked.

Mitigation: Validate deployment prefixes as hostname-safe values and manually confirm peer identities before handshakes.

Risk: The pick-optimizer role references payment escrow behavior.

Mitigation: Avoid enabling the payment-escrow role unless the financial workflow is explicitly required and separately reviewed.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-autonomous-warehouse-setup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup guidance, hostnames, manifests, data-flow descriptions, and peer handshake commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
