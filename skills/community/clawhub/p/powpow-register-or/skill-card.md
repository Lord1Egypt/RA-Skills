## Description:

Guides users through PowPow (Bubble) account registration, email verification and one-click login, with optional assistance starting a subscription order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users use this skill to create an account through an agent-led conversation, confirm an emailed code and receive a login link. If they choose to upgrade, the agent can start an Alipay or PayPal order and check its status; the user completes payment themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared local state file can mix login tokens and payment sessions between different users.

Mitigation: Avoid concurrent use by different users under the same OS account until state is isolated per user and session.

Risk: Registration and optional payment-order creation involve sensitive account information and potential charges.

Mitigation: Use only with the user's informed consent; have the user complete payment directly with the checkout provider.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-or)
- [PowPow website](https://global.powpow.online)
- [Agent workflow](references/agent-flow.md)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Links, Shell commands]

**Output Format:** [Conversational text and Markdown with links and commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide account login and optional checkout links; treat login links as sensitive.]

## Skill Version(s):

2.2.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
