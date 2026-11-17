## Description:

Payment Gateway Toolkit supports multi-channel payment handling for Stripe and Alipay, including order creation, refunds, payment status queries, webhook verification, and order history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate or prototype Stripe and Alipay payment flows, including creating orders, issuing refunds, querying status, and validating Alipay notifications. It should be used in sandbox or carefully controlled payment-development environments until production payment safeguards are reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create payment intents and refund requests against Stripe or Alipay accounts.

Mitigation: Use sandbox or carefully controlled payment-development accounts, scope API access to intended accounts, and require explicit approval before any refund flow can run.

Risk: Payment amounts are handled as floating-point values, which can cause monetary rounding errors.

Mitigation: Validate all monetary values with Decimal or integer minor units before enabling production payment or refund operations.

Risk: Payment credentials and sensitive payment data may be exposed through examples, logs, command history, or returned order data.

Mitigation: Use test credentials during development, keep secrets out of prompts and logs, redact sensitive values from outputs, and review returned payment data before storing or sharing it.

Risk: Dependencies are declared with lower bounds only, so installed package versions may vary across environments.

Mitigation: Pin and review dependency versions before deployment, especially for payment SDKs and network-facing packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/payment-gateway-toolkit)
- [Project homepage](https://github.com/kaiyuelv/payment-gateway-toolkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment API credential placeholders and sandbox configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
