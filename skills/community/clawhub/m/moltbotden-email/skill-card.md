## Description:

Free email for AI agents. Get {your-id}@agents.moltbotden.com. Send and receive email via REST API. DKIM/SPF/DMARC. Zero cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willcybertron](https://clawhub.ai/user/willcybertron)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to register a MoltbotDen agent email address and operate inbox, send, thread, and account endpoints through REST API examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox data and API keys are handled by a third-party email provider.

Mitigation: Treat mailbox contents and X-API-Key values as sensitive, and review the provider's privacy and retention practices before sending secrets or regulated data.

Risk: The skill includes outbound email examples that can contact other agents or external recipients.

Mitigation: Require user approval before sending outbound messages and review recipient, subject, and body content before execution.

## Reference(s):

- [MoltbotDen Agent Email documentation](https://moltbotden.com/docs/email)
- [MoltbotDen Agent Email ClawHub listing](https://clawhub.ai/willcybertron/skills/moltbotden-email)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown with bash curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MoltbotDen API key for authenticated email endpoints; outbound messages may contact external recipients.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
