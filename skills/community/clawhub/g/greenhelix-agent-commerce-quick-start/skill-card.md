## Description:

A quick-start guide to agent commerce that explains x402, GreenHelix API calls, and example flows for registration, payment, and escrow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external builders use this guide to understand agent-commerce concepts and adapt sample GreenHelix sandbox API calls for identity registration, service listing, payments, and escrow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide references payment and signing credentials that could authorize financial or identity-sensitive operations.

Mitigation: Use sandbox or test credentials by default, scope keys narrowly, and avoid providing production Stripe or signing keys unless a reviewed workflow requires them.

Risk: The private-key example prints secret key material.

Mitigation: Do not run that example as written; store private keys securely and remove logging or display of secret values.

Risk: Copying payment examples without review could trigger real payment, escrow, or settlement operations.

Mitigation: Confirm endpoints, amounts, and account mode before execution, and prefer the GreenHelix sandbox for initial testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-commerce-quick-start)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API registration](https://api.greenhelix.net/register)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)
- [GreenHelix sandbox API endpoint](https://sandbox.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is non-executable and does not install dependencies; examples reference GreenHelix, signing, and Stripe credentials supplied by the user.]

## Skill Version(s):

1.3.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
