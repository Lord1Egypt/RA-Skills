## Description:

Helps users register for PowPow (Burbuja), verify their email and sign in with one click, with optional guidance through a membership upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Prospective PowPow users can ask an agent to complete account registration, troubleshoot verification, and provide a one-click sign-in link. If they choose to upgrade, the agent can create and check a subscription order while the user completes payment themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration submits personal account details to PowPow.

Mitigation: Obtain the user's consent before submitting details to global.powpow.online.

Risk: A session token is held temporarily during sign-in or subscription steps.

Mitigation: Run the cleanup step when finished to remove temporary session state.

Risk: Optional subscription steps may involve payment.

Mitigation: Have the user complete any Alipay or PayPal payment in the official checkout; do not handle payment credentials.

## Reference(s):

- [PowPow skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-es)
- [PowPow website](https://global.powpow.online)
- [Registration flow](references/registration-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with links and inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a one-click sign-in link and an account summary; does not repeat the password.]

## Skill Version(s):

2.2.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
