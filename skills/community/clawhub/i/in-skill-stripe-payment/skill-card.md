## Description: <br>
Guides an agent through gating premium skill behavior behind a Stripe one-time checkout, checking local receipts, showing a payment link, and verifying completed Checkout Sessions by email. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[divyn](https://clawhub.ai/user/divyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill as a reference for adding a Stripe payment gate before premium behavior runs. It is suitable for demonstrating the payment flow and for adapting the placeholder premium section into a real paid skill after hardening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stripe secret keys are required for payment verification. <br>
Mitigation: Install only where STRIPE_SECRET_KEY can be protected, and never ask end users to provide the secret key. <br>
Risk: The demo receipt cache is local agent state and is not a production entitlement system. <br>
Mitigation: For real paid skills, replace the local receipt cache with server-side or signed entitlement storage bound to a stable user identity. <br>
Risk: Payment amount checks can unlock access at the wrong price if not configured. <br>
Mitigation: Confirm MIN_AMOUNT_CENTS matches the Stripe Payment Link price before launch. <br>


## Reference(s): <br>
- [Stripe Payment Links documentation](https://stripe.com/docs/payment-links) <br>
- [ClawHub skill release page](https://clawhub.ai/divyn/in-skill-stripe-payment) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Stripe environment configuration and may write local receipt state.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
