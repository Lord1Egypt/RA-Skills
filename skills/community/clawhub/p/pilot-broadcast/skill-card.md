## Description:

Publish messages to all trusted peers on a topic over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to publish announcements, status updates, notifications, and alerts to trusted peers over Pilot Protocol topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broadcast recipient scope is unclear, which could send operational updates to unintended trusted peers.

Mitigation: Verify the Pilot Protocol publish scope before use and avoid sensitive message content unless the recipient set is explicit.

Risk: Messages may expose credentials, private keys, personal data, or sensitive operational details if broadcast broadly.

Mitigation: Do not include secrets or sensitive data in broadcast payloads; use a private messaging workflow when targeting a specific peer.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot Protocol daemon, and active trust relationships.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
