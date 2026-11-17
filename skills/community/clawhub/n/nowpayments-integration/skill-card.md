## Description:

Integrates the NowPayments API so an agent can add multi-cryptocurrency checkout, IPN callback handling, payment verification, and order tracking to an AI-operated store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use this skill to have an agent add NowPayments checkout, IPN webhook handling, and payment status tracking to an AI-operated store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-flow changes may be under-scoped and could affect checkout, callback, or order-status behavior.

Mitigation: Apply changes in a test branch or staging environment and review each endpoint, callback, and payment-status change before deployment.

Risk: Payment API keys and IPN secrets may be exposed if environment files, logs, or chat transcripts are mishandled.

Mitigation: Store NOWPAYMENTS_API_KEY and NOWPAYMENTS_IPN_SECRET in protected environment configuration, keep secret files gitignored, and avoid logging or sharing secret values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/casperzinou/skills/nowpayments-integration)
- [NowPayments Docs](https://documenter.getpostman.com/view/7900902/S1a7UnNT)
- [Store Example](https://www.talonforge.xyz/store)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for checkout endpoints, IPN callbacks, environment variables, and payment-status handling.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
