## Description: <br>
Query and manage Stripe data via the Stripe API, including charges, customers, invoices, subscriptions, payment intents, refunds, products, and prices, with filtering, pagination, and direct calls to api.stripe.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeninja23](https://clawhub.ai/user/codeninja23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query Stripe account data and perform supported Stripe account actions such as creating refunds or updating customer records through the Stripe API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use live Stripe credentials to perform payment-system actions, including refunds and customer updates. <br>
Mitigation: Use Stripe test keys or restricted keys where possible, and require explicit human approval before refund creation, customer updates, or any POST request to Stripe. <br>
Risk: Stripe secret keys could be exposed through logs, chat transcripts, or copied command output. <br>
Mitigation: Keep STRIPE_SECRET_KEY in the environment, do not paste live keys into chats, and redact credentials from logs or shared outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codeninja23/native-stripe) <br>
- [Stripe API Keys](https://dashboard.stripe.com/apikeys) <br>
- [Stripe API v1 Endpoint](https://api.stripe.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Formatted terminal tables for list results and JSON for single-object or raw responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and STRIPE_SECRET_KEY; supports a --json flag for raw JSON output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
