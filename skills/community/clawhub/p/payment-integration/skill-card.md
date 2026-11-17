## Description:

Senior payment integration engineer that helps developers integrate 8 major payment providers (Stripe, PayPal, Alipay, WeChat Pay, Apple Pay, Google Pay, Razorpay, Square) with working code examples, security best practices, and webhook patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxty](https://clawhub.ai/user/xiaoxty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and implement payment integrations across major providers, with guidance for code examples, webhook handling, testing, and security practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested webhook logging can expose headers, payloads, or payment-related secrets if copied directly into production.

Mitigation: Redact sensitive headers and payload fields, avoid raw webhook logging in production, and keep only the minimum audit data needed for debugging.

Risk: Payment and webhook examples may become outdated or may not fully match a provider's current verification requirements.

Mitigation: Verify each provider flow against current official documentation before handling real payments, especially webhook signature validation and body parsing requirements.

Risk: Generated payment integration code may mishandle money amounts, idempotency, or asynchronous payment state.

Mitigation: Review code before use, test in provider sandboxes, validate amounts server-side, and add idempotency and duplicate-event handling before deployment.

## Reference(s):

- [Payment Provider Detailed Reference](providers.md)
- [ClawHub Skill Page](https://clawhub.ai/xiaoxty/skills/payment-integration)
- [Publisher Profile](https://clawhub.ai/user/xiaoxty)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and actionable integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and can focus on a selected payment provider.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
