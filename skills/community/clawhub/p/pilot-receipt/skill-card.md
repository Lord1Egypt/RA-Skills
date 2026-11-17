## Description:

Delivery and read receipts for messages over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators using Pilot Protocol use this skill to send messages with receipt metadata, check inbox receipts, subscribe to receipt channels, and publish read confirmations for audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clearing the inbox can remove received messages needed for later audit or troubleshooting.

Mitigation: Review and preserve relevant messages before using pilotctl --json inbox --clear.

Risk: Agents may issue pilotctl commands that send messages or publish receipts on the Pilot Protocol network.

Mitigation: Review generated commands, hostnames, message data, and receipt payloads before execution.

## Reference(s):

- [Pilot Protocol Network](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require pilotctl on PATH and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
