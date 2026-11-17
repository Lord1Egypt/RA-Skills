## Description:

Bidirectional bridge between Pilot Protocol and Slack channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agent builders use this skill to connect Pilot agents with Slack workspaces for outbound notifications and inbound Slack event streams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public Pilot daemon example can expose the bridge beyond the intended deployment boundary.

Mitigation: Use a controlled Slack workspace and private Pilot deployment; avoid the public daemon example unless strong authentication and network allowlisting are in place.

Risk: Slack text can trigger operational lookups such as daemon status or peer lists without documented access controls.

Mitigation: Restrict or remove Slack commands that return daemon status or peer lists unless workspace authorization and command access controls are documented.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-slack-bridge)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume pilotctl is installed, a Pilot daemon is running, and Slack webhook and relay services are configured.]

## Skill Version(s):

1.0.0 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
