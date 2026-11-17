## Description:

Complete cold email campaign suite for Mailgo that helps an agent verify recipients, claim a mailbox, generate and optimize content, create campaigns, manage lifecycle actions, and report campaign results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leadsnavideveloper](https://clawhub.ai/user/leadsnavideveloper)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and run Mailgo cold-email campaigns, including recipient verification, sender mailbox setup, email content optimization, campaign creation, lifecycle controls, and reporting. Users should have a Mailgo account credential and confirm they have a lawful basis to contact recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Mailgo account credential that may allow mailbox, campaign, reporting, and reply-body access.

Mitigation: Use a dedicated, revocable Mailgo token from protected secret storage; do not paste the token into chat, and avoid command-line token flags that may expose secrets.

Risk: The skill can upload recipient lists and activate cold-email campaigns.

Mitigation: Confirm legal basis, consent, and platform terms before uploading leads or sending; use dry-run mode or an explicit final confirmation before campaign activation.

Risk: The skill can delete campaigns and read reply bodies.

Mitigation: Require explicit user confirmation before irreversible campaign deletion and before accessing reply content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leadsnavideveloper/skills/mailgo-coldmail-marketing)
- [Mailgo Product](https://app.mailgo.ai)
- [LeadsNavi Publisher Website](https://www.leadsnavi.com)
- [Mailgo OpenAPI Specification](artifact/gpt/openapi.json)
- [Spam Trigger Word Replacements](artifact/resources/spam-triggers.md)
- [Industry Email Templates](artifact/resources/industry-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated email content, JSON script outputs, and configuration instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Mailgo APIs through bundled scripts or OpenAPI actions using a Mailgo API key.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
