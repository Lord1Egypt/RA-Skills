## Description:

Provides an AI agent with its own MailMolt email address for sending, receiving, searching, and managing email under human oversight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rakesh1002](https://clawhub.ai/user/rakesh1002)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give an AI agent a separate email identity for inbox monitoring, message search, agent-to-agent communication, and supervised outbound email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send outbound email through MailMolt at higher permission levels.

Mitigation: Use sandbox or supervised mode where possible, review outgoing messages manually, and avoid broad auto-reply workflows.

Risk: The skill requires a MailMolt API key and may also use webhook or linked-service secrets.

Mitigation: Store API keys and webhook secrets in a secret store or tightly permissioned environment variables, and rotate them if exposed.

Risk: Broad natural-language triggers may cause unintended email actions.

Mitigation: Require explicit user confirmation for sends, replies, referrals, webhooks, and linked-service actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rakesh1002/skills/mailmolt)
- [MailMolt documentation](https://mailmolt.com/docs)
- [MailMolt skill file](https://mailmolt.com/skill.md)
- [MailMolt heartbeat reference](https://mailmolt.com/heartbeat.md)
- [MailMolt API health endpoint](https://api.mailmolt.com/health)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown and plain text responses with JSON configuration examples and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or request email subjects, message bodies, recipient addresses, webhook settings, and MailMolt API configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata and mailmolt-hook.json; artifact config/package manifests list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
