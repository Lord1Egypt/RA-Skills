## Description:

Manage Paystack customers, transactions, payment pages, transfers, and payment operations via the Paystack API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw agent to Paystack through ClawLink, inspect payment data, verify transactions, manage customers, create payment pages, and perform guarded payment operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and trusting an unpinned third-party ClawLink plugin that stores Paystack credentials.

Mitigation: Verify the ClawLink plugin provenance before installation, use a dedicated least-privilege Paystack credential where possible, and revoke the Paystack key if the skill is no longer used.

Risk: Payment, transfer, create, update, or delete operations may affect production Paystack data or real money.

Mitigation: Preview and confirm every write or transfer, including target resource, recipient, currency, and amount, before execution.

Risk: Connected Paystack accounts may contain sensitive customer or transaction data.

Mitigation: Review the skill before installing against production accounts and restrict the connected credential to the minimum access needed for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hith3sh/skills/paystack-payments)
- [Publisher profile](https://clawhub.ai/user/hith3sh)
- [Paystack API Documentation](https://paystack.com/docs/api/)
- [Paystack Transaction API](https://paystack.com/docs/api/transaction/)
- [Paystack Customer API](https://paystack.com/docs/api/customer/)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide tool calls that access Paystack account data or initiate payment operations through a connected ClawLink integration.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
