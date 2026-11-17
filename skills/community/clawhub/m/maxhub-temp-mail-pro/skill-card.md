## Description:

Creates temporary email addresses and retrieves inbox messages and email details through the MaxHub API for authorized testing, verification, and privacy use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA teams use the skill to create temporary inboxes, retrieve messages, and read message details for authorized testing and legitimate verification. It also supports privacy-conscious one-time receiving; it must not be used to evade identity checks or for spam or fraud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports an unpinned installer.

Mitigation: Review the installation source and verify the intended release before installing.

Risk: The security scan reports automatic legal-confirmation records.

Mitigation: Check that any consent step reflects a real user decision before relying on it.

Risk: The security scan reports incomplete reference resolution, so its evidence is incomplete.

Mitigation: Confirm endpoint details against the published references and service documentation before use.

Risk: Mailbox tokens, passwords, and API credentials can expose access to mailboxes or the API account.

Mitigation: Keep credentials out of prompts and logs, and let the user retain mailbox credentials.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-temp-mail)
- [Temp Mail Pro release](https://clawhub.ai/xiewxx/skills/maxhub-temp-mail-pro)
- [MaxHub API service](https://www.aconfig.cn)
- [Endpoint and field guidance](artifact/references/mail.md)
- [Endpoint whitelist](artifact/references/endpoints_whitelist.yaml)

## Skill Output:

**Output Type(s):** [Text, Structured data, Email content]

**Output Format:** [Email addresses, inbox summaries, and message details in text or structured response form]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include email addresses, message contents, links, and mailbox credentials; avoid retaining or exposing sensitive values.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
