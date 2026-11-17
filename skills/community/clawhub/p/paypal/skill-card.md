## Description:

Integrate PayPal payments with proper webhook verification, OAuth handling, and security validation for checkout flows and subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement PayPal REST API checkout, subscription, payout, webhook, OAuth token, dispute, and refund workflows with payment-specific validation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment examples could produce unsafe financial workflows if copied directly into production.

Mitigation: Review and strengthen generated code with authenticated server-side authorization, transaction ownership checks, exact amount and currency validation, merchant validation, idempotency controls, refund limits, and audit logging.

## Reference(s):

- [PayPal Code Patterns](patterns.md)
- [PayPal Webhook Events](webhooks.md)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with JavaScript, HTML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no required binaries are declared.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
