## Description:

Operate the Payall crypto card CLI tool for managing crypto debit cards, checking balances and fees, applying for cards, topping up cards, withdrawing card funds, and sending USDT across BSC, Ethereum, and TRON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c0ldsmi1e](https://clawhub.ai/user/c0ldsmi1e)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate the Payall CLI for crypto card management, card recommendations, wallet balance checks, card top-ups, withdrawals, and USDT transfers. It is most relevant when a user wants terminal guidance for Payall card or wallet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports financial automation involving wallet signing, card details, and transaction commands.

Mitigation: Use it only with trusted Payall CLI installations and publisher trust, verify destination addresses and amounts manually, and avoid pasting private keys into chat or command arguments.

Risk: Some CLI flags can skip confirmation prompts for transfers, withdrawals, top-ups, or card applications.

Mitigation: Avoid confirmation-skipping flags such as --yes for transfers or withdrawals unless the user has explicitly reviewed the destination, chain, amount, and fees.

Risk: Card detail commands can reveal full card number, CVV, expiry, and billing details.

Mitigation: Reveal full card details only when strictly necessary for the user-requested task and avoid sharing or retaining sensitive card information beyond that workflow.

## Reference(s):

- [PayAll CLI ClawHub skill page](https://clawhub.ai/c0ldsmi1e/skills/payall-cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and structured CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command flags, wallet or card workflow steps, fee comparison guidance, and safety reminders for sensitive financial actions.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
