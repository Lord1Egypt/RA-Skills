## Description:

Helps users register for PowPow, verify their email, and sign in with one click, with optional guidance for Alipay or PayPal subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

People creating a PowPow account use the agent to complete email verification, registration, and sign-in within a conversation. It can also help troubleshoot registration and guide an optional subscription purchase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration shares an email address, chosen password, verification code, and optionally an avatar or phone number with PowPow.

Mitigation: Use the skill only if comfortable sharing these details with PowPow, and use a trusted single-user machine.

Risk: Account session tokens are retained locally during the flow.

Mitigation: Run cleanup after completing the flow to remove the local token state.

Risk: Optional subscription orders lead to payment pages.

Mitigation: Verify the payment page before paying and complete payment yourself.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-gu)
- [PowPow website](https://global.powpow.online)
- [Agent flow](references/agent-flow.md)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)
- [Screenshots](references/screenshots.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Links]

**Output Format:** [Conversational text with commands and sign-in or payment links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May share bundled product screenshots and report registration or subscription status.]

## Skill Version(s):

2.2.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
