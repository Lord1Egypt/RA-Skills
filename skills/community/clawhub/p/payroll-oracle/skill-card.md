## Description:

Payroll Oracle helps agents audit GitHub or Linear work links and calculate USDC payroll settlement amounts with a 1% x402 commission flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eldan445](https://clawhub.ai/user/eldan445)

### License/Terms of Use:


## Use Case:

Developers and operations teams can use this skill to check provided GitHub or Linear work links and calculate contractor payout splits before payment review. It should not be used for payroll, bounty approval, invoice settlement, or accounting records without replacing the placeholder audit and settlement behavior and requiring explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current audit behavior can falsely approve GitHub or Linear work.

Mitigation: Replace placeholder audit functions with authenticated GitHub and Linear checks before using results for payroll, bounty approval, invoice settlement, or accounting records.

Risk: The settlement script can imply payment settlement without confirming that funds moved.

Mitigation: Treat settlement output as a payout calculation unless confirmed transactions are implemented and verified on the intended network.

Risk: Payment decisions could be made without human review of recipient, amount, network, and fee.

Mitigation: Require explicit human approval for every payment recipient, amount, network, and fee before any transaction is initiated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eldan445/skills/payroll-oracle)
- [Publisher profile](https://clawhub.ai/user/eldan445)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with shell command invocations and script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports GitHub and Linear work links; payout output is a calculation and should not be treated as a confirmed transaction.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
