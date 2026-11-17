## Description:

Helps users register for PowPow (Bubble), verify their email, and sign in with a one-click link, with optional Alipay or PayPal subscription assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users can ask an agent to guide account registration, email verification, and sign-in. When a subscription is needed or requested, the agent can help set up checkout while the user completes payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration and sign-in involve account credentials and session tokens.

Mitigation: Use only when you intend to create or access a PowPow account, and keep verification codes and sign-in links private.

Risk: Optional subscription steps can open a browser checkout and initiate payment setup.

Mitigation: Confirm the plan and payment provider yourself before proceeding; complete payment only in the provider's checkout.

Risk: Temporary checkout and session-token files can remain on the local device.

Mitigation: Expect temporary local files and run the skill's cleanup step when finished to remove session-token state.

## Reference(s):

- [PowPow website](https://global.powpow.online)
- [PowPow registration](https://global.powpow.online/register)
- [Agent flow](references/agent-flow.md)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational guidance with sign-in or checkout links and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide registration troubleshooting and payment-status guidance.]

## Skill Version(s):

2.2.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
