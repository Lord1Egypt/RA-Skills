## Description:

Send and receive email notifications through Pilot Protocol messaging using SMTP and webhook relay workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who use Pilot Protocol can send agent email notifications, receive emails as Pilot events, and integrate email-based workflows with configured SMTP or webhook relays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive email content or attachments may be sent through the configured SMTP or webhook relay.

Mitigation: Install only when the Pilot Protocol and relay endpoint are trusted, prefer HTTPS endpoints, and minimize sensitive email content and attachments.

Risk: Email credentials are required for relay workflows and could be exposed if handled inside prompts or skill content.

Mitigation: Protect email credentials outside the skill and use the surrounding runtime or relay configuration for secret handling.

Risk: Inbox cleanup commands can delete messages that may still be needed.

Mitigation: Avoid running inbox clear operations until messages have been reviewed or retained elsewhere.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-email-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pilotctl command examples, JSON email payloads, webhook setup steps, and relay safety guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
