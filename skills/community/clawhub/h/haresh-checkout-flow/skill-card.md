## Description:

Process e-commerce checkout via n8n webhook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haresh-sai06](https://clawhub.ai/user/haresh-sai06)

### License/Terms of Use:


## Use Case:

External commerce users and checkout agents use this skill to validate carts, handle authentication or guest checkout, collect shipping information, process payment options, and present order confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive checkout data may be sent to local n8n webhooks.

Mitigation: Document what checkout data is sent, authenticate webhook requests, validate inputs, and avoid sending full payment details.

Risk: Payment processing may occur before final user confirmation.

Mitigation: Require the user to review and confirm the final order before calling any payment-processing or order-creation webhook.

Risk: Payment information could be mishandled if raw payment details are collected or logged.

Mitigation: Use only tokenized payment method identifiers and never store or log full payment details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haresh-sai06/skills/haresh-checkout-flow)
- [ClawHub publisher profile](https://clawhub.ai/user/haresh-sai06)

## Skill Output:

**Output Type(s):** [guidance, API Calls, markdown]

**Output Format:** [Markdown checkout guidance with webhook call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces checkout flow steps, validation outcomes, payment retry guidance, and order confirmation summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
