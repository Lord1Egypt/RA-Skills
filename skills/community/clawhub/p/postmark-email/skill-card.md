## Description:

Inspect transactional email activity, manage templates, review message delivery events, configure webhooks, and administer Postmark email workflows via the Postmark API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, and email operations staff use this skill to inspect Postmark delivery activity, troubleshoot bounces and spam complaints, manage templates and message streams, and configure webhooks or server settings through confirmed Postmark tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration depends on ClawLink and connected Postmark credentials for server access.

Mitigation: Install only from a trusted ClawHub source, use a narrowly scoped and revocable Postmark token where possible, and revoke credentials when the integration is no longer needed.

Risk: Write-capable tools can create, update, archive, or delete Postmark resources such as templates, webhooks, suppressions, message streams, inbound rules, and server settings.

Mitigation: Review write previews, confirm the target resource and intended effect with the user, and execute write calls only after the preview matches the user's request.

Risk: Server configuration changes can affect all email sending on the connected Postmark server.

Mitigation: Prefer read and describe operations before writes, validate parameters against the live tool schema, and reserve server-level changes for explicit administrative requests.

## Reference(s):

- [Postmark API Documentation](https://postmarkapp.com/developer/api/overview)
- [Postmark Message Streams API](https://postmarkapp.com/developer/api/message-streams)
- [Postmark Templates API](https://postmarkapp.com/developer/api/templates)
- [Postmark Webhooks API](https://postmarkapp.com/developer/api/webhooks)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=postmark-email)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate Postmark tool calls through ClawLink after connection checks and user confirmation for writes.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
