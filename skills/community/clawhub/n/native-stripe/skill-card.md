## Description:

Native Stripe lets agents query and manage Stripe charges, customers, invoices, subscriptions, payment intents, refunds, products, prices, and balance transactions directly through the Stripe API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeninja23](https://clawhub.ai/user/codeninja23)

### License/Terms of Use:


## Use Case:

Developers and account operators use Native Stripe to inspect Stripe account data and perform account actions such as refunds or customer updates from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live Stripe secret key can give an agent access to sensitive account data and financial operations.

Mitigation: Use a restricted Stripe key, start with a test-mode key, and avoid exposing a full live secret key to the agent.

Risk: Refund creation and customer updates are real account-changing operations.

Mitigation: Require explicit confirmation, dry-run behavior, or resource allowlists before using mutation commands in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codeninja23/skills/native-stripe)
- [ClawHub Publisher Profile](https://clawhub.ai/user/codeninja23)
- [Stripe API Key Dashboard](https://dashboard.stripe.com/apikeys)
- [Stripe API Base URL](https://api.stripe.com/v1)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text tables or JSON returned from Stripe API commands, with Markdown setup and usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STRIPE_SECRET_KEY and python3; supports filtering, pagination limits, and optional raw JSON output.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
