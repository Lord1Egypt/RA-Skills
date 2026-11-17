## Description:

Build autonomous purchasing agents with spending controls, vendor evaluation, escrow protection, and multi-protocol buying across UCP, ACP, and A2A marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this guide to design procurement agents that discover vendors, evaluate trust, apply spending controls, execute multi-protocol purchases, use escrow and dispute flows, and reconcile spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples can perform real payment actions with live GreenHelix, Stripe, or wallet credentials.

Mitigation: Use sandbox credentials or review-only mode until mandatory policy enforcement, spending limits, and explicit approval are in place.

Risk: Example flows do not consistently enforce the approval controls described by the guide.

Mitigation: Add approval gates before payment or token-bearing requests and block execution when policy checks fail.

Risk: Payment or token-bearing requests sent to unvalidated origins can expose credentials or authorize unintended transactions.

Mitigation: Use origin allowlists, strict URL validation, scoped credentials, idempotency keys, and human confirmation before live requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-procurement-playbook)
- [GreenHelix sandbox endpoint](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python code examples, checklists, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide; live workflows may require GREENHELIX_API_KEY, WALLET_ADDRESS, and STRIPE_API_KEY.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
