## Description:

Pengbo Space helps agents query pengbo.space SMM services, find service IDs, place confirmed orders, check order status, request refills, and check account balance through the pengbo.space API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amadohallal](https://clawhub.ai/user/amadohallal)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to automate pengbo.space social-media growth workflows, including service discovery, order placement after explicit confirmation, order tracking, refill requests, and balance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or refill paid social-growth orders after confirmation.

Mitigation: Review the service ID, link, quantity, account balance, and confirmation flag before running order or refill commands.

Risk: Bundled update and release/security scripts can modify local files or the user's Python environment.

Mitigation: Run those scripts only from a trusted release source, verify update signatures, and pin dependencies before use.

Risk: API keys, output links, order data, and API responses may be sensitive.

Mitigation: Store API keys in environment variables or a secret manager, limit log sharing, and redact order and account details before redistribution.

Risk: The release evidence flags unsolicited recharge promotion content.

Mitigation: Treat promotional claims as unverified and confirm terms directly on pengbo.space before acting on them.

## Reference(s):

- [Pengbo Space Skill Page](https://clawhub.ai/amadohallal/skills/pengbo-space)
- [Pengbo Space API Documentation](https://pengbo.space/user/api/docs)
- [Pengbo Space API Reference](references/api-reference.md)
- [Security Release Checklist](references/security-release-checklist.md)
- [Update Signing](references/update-signing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require explicit confirmation; API responses and order data may include sensitive information.]

## Skill Version(s):

1.1.1-beta.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
