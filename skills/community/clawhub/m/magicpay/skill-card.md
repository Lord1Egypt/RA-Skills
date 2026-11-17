## Description:

Helps an agent handle MagicPay payments, funding, saved information, agent email, account readiness, choices, and payment recovery through a remote connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xor777](https://clawhub.ai/user/xor777)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent to make authorized purchases or transfers can use MagicPay for checkout, funding, saved details, receipts, and recovery of uncertain payment outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving a payment or transfer can authorize real spending.

Mitigation: Review the exact amount, recipient, and MagicPay approval before authorizing; do not treat a chat response or an opened checkout link as approval or settlement.

Risk: Saved personal and payment values can be exposed during authorized browser checkout.

Mitigation: Use values only for the authorized task and avoid repeating them in replies, files, logs, or exported evidence.

Risk: Payment state can remain uncertain after an interrupted checkout or cancellation.

Mitigation: Recover and reconcile the same operation before claiming completion or starting another payment.

## Reference(s):

- [MagicPay skill homepage (Clawdis metadata)](https://github.com/nuanu-ai/skills/tree/main/skills/magicpay)
- [MagicPay marketplace documentation (OpenClaw metadata)](https://github.com/nuanu-ai/skills/blob/main/docs/magicpay/openclaw/marketplace/README.md)
- [Payment operations](references/payment-operations.md)
- [Payment guardrails](references/guardrails.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Conversational text and Markdown with links or commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payment outcomes require confirmation from the exact payment operation.]

## Skill Version(s):

0.4.96 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
