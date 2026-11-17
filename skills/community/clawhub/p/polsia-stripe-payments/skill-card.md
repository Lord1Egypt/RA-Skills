## Description:

Accept payments on a Polsia-built site via Stripe Connect payment links, then verify them server-side without Stripe SDKs, webhooks, or STRIPE_SECRET_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentlevier](https://clawhub.ai/user/agentlevier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Polsia sites use this skill to add Stripe Connect payment links, poll for payment completion, and verify completed payments server-side through Polsia's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment fulfillment could run more than once if completion checks are retried or repeated.

Mitigation: Make fulfillment idempotent by checkout session ID, as specified in the security guidance and artifact behavior.

Risk: A Polsia API key could be exposed if payment verification is implemented client-side.

Mitigation: Keep POLSIA_API_KEY server-side and perform verification from trusted server code only.

Risk: Companies cannot accept payments until Stripe onboarding is complete, and the platform fee affects proceeds.

Mitigation: Confirm the company account has completed Stripe onboarding and disclose the 20% platform fee before enabling the flow.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, code, configuration, shell commands]

**Output Format:** [Markdown guidance with inline endpoint, environment variable, and polling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for payment-link creation, success-page polling, and server-side payment verification.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
