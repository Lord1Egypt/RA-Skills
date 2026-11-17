## Description:

Query perpetual futures market data, account positions, open orders, fills, and prepare signed order, cancel, and deposit flows through LiberFi's CLI and API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombmod](https://clawhub.ai/user/bombmod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect LiberFi perpetuals market data and account-specific positions, orders, and fills. It also guides human-confirmed order, cancel, and SOL deposit workflows for Hyperliquid-backed perpetuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent global CLI installation can introduce supply-chain risk.

Mitigation: Install only a reviewed, pinned version of @liberfi.io/cli from a trusted source; do not allow automatic global installation without review.

Risk: Authenticated reads can expose account-linked perpetuals positions, orders, and fills.

Mitigation: Confirm the intended account context before authenticated queries and disclose only the requested account data.

Risk: Deposit and signed submit flows can trigger irreversible financial actions.

Mitigation: Require explicit user confirmation of wallet/account, amount, recipient, and action before deposit-place, order-submit, or cancel-submit.

## Reference(s):

- [Perp Deposit Flow](reference/deposit-flow.md)
- [LiberFi Homepage](https://liberfi.io)
- [ClawHub Skill Page](https://clawhub.ai/bombmod/skills/liberfi-perpetuals)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured CLI output and includes human-confirmation gates for financial actions.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
