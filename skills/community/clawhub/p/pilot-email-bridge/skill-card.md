## Description: <br>
Send and receive emails via Pilot Protocol messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect Pilot agents with email workflows, including outbound notifications, inbound message handling, and file attachments through configured SMTP, IMAP, or webhook relays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email relay configuration can send messages, message bodies, recipients, and attachments to external SMTP or webhook services. <br>
Mitigation: Use trusted relays, review recipients, message bodies, attachment paths, and endpoints before sending, and prefer least-privileged email credentials. <br>
Risk: Clearing the inbox can remove queued messages before they have been reviewed. <br>
Mitigation: Review or export queued messages before running inbox clearing commands. <br>


## Reference(s): <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume the pilotctl binary, a running Pilot daemon, and configured email relay credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
