## Description:

Use the single ItPay entry point when a human asks an agent to buy through ItPay; buyer workflows cover service discovery, purchase, checkout, delivery, recovery, and refunds, while seller workflows are not yet implemented.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itpay](https://clawhub.ai/user/itpay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw agent operate ItPay buyer flows for catalog discovery, checkout handoff, delivery recovery, and refunds while keeping payment approval with the human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through purchases and checkout presentation that may create external service costs.

Mitigation: Before checkout, verify the service, price, currency, required contact fields, and destination chat, then wait for explicit human approval.

Risk: Device private keys, bearer tokens, display tokens, or checkout handoff details could expose payment or delivery access if shared outside the intended flow.

Mitigation: Keep credentials and display tokens out of ordinary responses, use only the intended ItPay handoff, and do not share device private keys.

Risk: Identity or session recovery mistakes could bypass quota, ownership, grant, or refund state.

Mitigation: Use one stable OpenClaw agent type and the server-returned recovery commands; do not rotate identity, create duplicate checkouts, or invent IDs.

Risk: Seller behavior is not implemented in this release.

Mitigation: Use the skill for buyer workflows only and do not invent seller commands, onboarding, listings, or successful seller states.

## Reference(s):

- [ClawHub ItPay skill page](https://clawhub.ai/itpay/skills/itpay)
- [ItPay OpenClaw skill homepage](https://github.com/itpay-ai/itpay-skill-openclaw)
- [ItPay CLI Buyer Quickstart](artifact/vendor/itpay-cli/docs/agent/buyer/quickstart.json)
- [Human Checkout Handoff And Payment Verification](artifact/vendor/itpay-cli/docs/agent/buyer/payment-flow.json)
- [Device Identity And Session Recovery](artifact/vendor/itpay-cli/docs/agent/buyer/identity-and-sessions.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise human-facing status or decision prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON CLI envelopes as evidence for agent responses; requires Node.js 18+ and the bundled ItPay CLI.]

## Skill Version(s):

2.0.25 (source: server release evidence, bundle.lock.json, and package-lock.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
