## Description:

MoneyClaw lets an agent inspect a prepaid wallet, create bounded payment tasks, and continue user-confirmed payment steps through a MoneyClaw account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elvismusli](https://clawhub.ai/user/elvismusli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use MoneyClaw to check prepaid wallet readiness, create auditable buyer-side payment tasks, and continue explicitly authorized checkout steps. Merchant-side acquiring guidance is included only for users who explicitly want to collect payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent financial payment authority, including creating payment tasks, retrieving payment execution details after approval, and reconciling charges.

Mitigation: Install it only for accounts where the user understands MoneyClaw auto-approval settings, prepaid balance limits, and the exact payment authority delegated to the agent.

Risk: Payment execution details can expose sensitive card and billing data for an active checkout.

Mitigation: Retrieve execution details only when the payment task is card_ready and the user explicitly asks to continue that exact payment step.

Risk: Merchant acquiring guidance goes beyond the primary buyer-side payment purpose and can affect invoice, widget, and webhook setup.

Mitigation: Use acquiring guidance only when the user explicitly wants to collect payments, and verify signed webhooks server-side before fulfilling orders.

Risk: Prepaid balance, auto-approval, and hidden-card bootstrap behavior can make available funding differ from the immediate purchase amount.

Mitigation: Check wallet readiness, account auto-approval state, provider-minimum funding behavior, and payment intent history before spending or retrying.

## Reference(s):

- [MoneyClaw OpenClaw homepage](https://moneyclaw.ai/openclaw)
- [MoneyClaw Skill Page](https://clawhub.ai/elvismusli/skills/moneyclaw)
- [Authorized Payment Safety Reference](references/payment-safety.md)
- [Acquiring Reference](references/acquiring.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and payment state interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MONEYCLAW_API_KEY and explicit user authorization before payment execution steps.]

## Skill Version(s):

5.5.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
