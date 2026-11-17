## Description:

Demonstrates how an agent can gate placeholder premium skill behavior behind a one-time Stripe checkout, verify payment by email through Stripe, and cache a local receipt.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[divyn](https://clawhub.ai/user/divyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this demo to prototype a paid-skill flow that checks for an existing receipt, shows a Stripe Payment Link when needed, verifies checkout by email, and only then allows premium placeholder behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment entitlement can be forged, reused, or granted from unrelated Stripe sessions.

Mitigation: Use this as a demo only; before production, validate entitlement server-side or with signed, user-bound, product-bound receipts and exact Stripe product or session checks.

Risk: The local receipt cache can persist access beyond the intended user, machine, product, or revocation state.

Mitigation: Protect local storage, bind receipts to a stable user and product, and add expiry and revocation handling.

Risk: Runtime payment verification depends on host secrets and outbound Stripe API access.

Mitigation: Provide Stripe secrets only through the deployment environment, avoid exposing them to end users, and handle temporary Stripe or network failures without unlocking premium behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/divyn/skills/in-skill-stripe-payment)
- [Stripe Payment Links documentation](https://stripe.com/docs/payment-links)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires host-provided Stripe environment variables and may read or write a local receipt cache.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
