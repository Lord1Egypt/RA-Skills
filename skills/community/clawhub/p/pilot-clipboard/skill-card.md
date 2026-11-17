## Description:

Shared clipboard for quick text and data snippets between agents over Pilot Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to exchange short text snippets, command output, and small data payloads across the Pilot network without transferring files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clipboard text or command output may contain secrets, regulated data, private project details, or other sensitive content.

Mitigation: Review content before sending and avoid sharing sensitive data unless the transfer is explicitly authorized.

Risk: Snippets are sent over the Pilot network to user-selected destinations.

Mitigation: Install and use the skill only with trusted Pilot destinations, and verify the destination before sending.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-clipboard)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pilotctl and jq; sends user-provided snippets or command output over Pilot Protocol.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
