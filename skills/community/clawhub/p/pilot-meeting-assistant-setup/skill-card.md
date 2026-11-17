## Description:

Deploy a meeting assistant system with three agents for scheduling, note capture, and action item tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure three coordinated meeting-assistant agents: a scheduler, a note-taker, and an action tracker. The skill helps set hostnames, install role-specific dependencies, write setup manifests, and establish peer handshakes for meeting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs multiple unpinned dependent skills.

Mitigation: Pin and verify each dependent skill before installing it in a real workspace.

Risk: Meeting notes, attendee details, action items, archives, and reminders may be processed by agents and external destinations.

Mitigation: Confirm organizational approval for the meeting data and notification destinations before configuring the workflow.

Risk: Incorrect peer identity or hostname choices can route meeting data to the wrong agent.

Mitigation: Use a simple hostname-safe prefix and confirm each peer identity before completing handshakes.

## Reference(s):

- [Pilot Protocol Network](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup steps, manifest templates, hostnames, handshake commands, and example publish/subscribe commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
