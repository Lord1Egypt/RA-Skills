## Description:

Helps users register for PowPow, verify their email, and sign in; an optional flow guides subscription upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow newcomers use this skill to create an account and get a one-click sign-in link with minimal interruption. Users who want a membership upgrade can receive payment guidance; publishing travel stories and creating digital humans are outside this skill's scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated passwords and one-click sign-in links grant access to the user's account.

Mitigation: Keep them private and share only with the intended user.

Risk: An optional subscription may lead to a payment page.

Mitigation: Ask the user to review the payment page before completing payment.

Risk: Registration state may contain account and order information.

Mitigation: Run the skill's cleanup step when finished.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-register-bn)
- [PowPow website](https://global.powpow.online)
- [Registration flow](references/registration-flow.md)
- [Agent flow](references/agent-flow.md)
- [Payment and activation](references/payment-and-activation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational Markdown with sign-in links and optional payment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide a generated password and a one-click sign-in link; handle both privately.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
