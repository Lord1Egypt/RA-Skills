## Description:

Send and receive SMS messages through a self-hosted SMS Gateway running on a USB GSM modem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattboston](https://clawhub.ai/user/mattboston)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to let an agent send SMS messages to allowlisted phone numbers and review incoming messages through a locally hosted GSM modem gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path includes running an unpinned remote installer with root privileges.

Mitigation: Review the installer before use and prefer a pinned release with a verified checksum or signature.

Risk: The SMS gateway API key can authorize message access or sending if exposed.

Mitigation: Store the key outside shared or synced workspaces where possible and restrict access to the local gateway environment.

Risk: Checking messages prints SMS contents and marks unread messages as read.

Mitigation: Use the receive command only when the user expects message contents to be displayed and read state to change.

Risk: A non-local gateway over plain HTTP can expose SMS traffic and API credentials.

Mitigation: Use HTTPS for any gateway that is not strictly local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattboston/skills/gsm-sms-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Send operations return status text and JSON from the gateway; receive operations print message metadata and bodies, then mark unread messages as read.]

## Skill Version(s):

0.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
