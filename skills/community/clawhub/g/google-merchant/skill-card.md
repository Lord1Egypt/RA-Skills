## Description:

Helps agents access and manage Google Merchant Center products, inventory, promotions, data sources, account settings, and reports through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and developers use this skill to inspect Google Shopping account data and, with explicit approval, make changes to products, inventory, promotions, data sources, and settings. It also describes optional user-approved automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account changes can alter or delete products, inventory, promotions, data sources, or settings.

Mitigation: Check the account and exact resource IDs, show the intended change, and obtain explicit user approval before each write.

Risk: Hosted functions, triggers, and webhook destinations can continue running or forwarding data after setup.

Mitigation: Review and separately approve each automation and destination; remove unused automations and connections after the task.

Risk: Credentials and returned business data may be exposed if handled carelessly.

Mitigation: Use scoped connections, avoid unnecessary raw API-key use, and disclose only the response fields needed for the task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/google-merchant)
- [Merchant API overview](https://developers.google.com/merchant/api/overview)
- [Merchant API reference](https://developers.google.com/merchant/api/reference/rest)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first guidance; require explicit approval for account changes and new automations.]

## Skill Version(s):

1.2.7 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
