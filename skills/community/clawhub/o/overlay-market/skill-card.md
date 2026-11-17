## Description:

Trade leveraged perpetual futures on Overlay Protocol (BSC), scan markets, analyze prices with technical indicators, check wallet balance, encode build and unwind transactions, and monitor positions with PnL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthurka-o](https://clawhub.ai/user/arthurka-o)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Overlay Protocol markets on BSC, prepare leveraged perpetual futures trades, review wallet balances and positions, and create transactions for signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mainnet trading and bundled transaction signing can put wallet funds at risk if transactions are not reviewed before signing.

Mitigation: Review every transaction before signing, prefer an external signer or restricted smart account, and use a dedicated low-value wallet.

Risk: Approving unlimited USDT spending can expose more funds than intended.

Mitigation: Use a custom approval amount unless unlimited approval is deliberate and appropriate for the wallet.

Risk: Piping unknown transaction JSON into the bundled sender could sign an unintended transaction.

Mitigation: Only send transaction JSON produced by reviewed skill commands and inspect the target, data, value, and chain ID before broadcasting.

## Reference(s):

- [Overlay App](https://app.overlay.market)
- [Overlay Documentation](https://docs.overlay.market)
- [ClawHub skill page](https://clawhub.ai/arthurka-o/skills/overlay-market)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON transaction objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Build and unwind scripts can emit unsigned BSC transaction JSON; send.js can return broadcast transaction status JSON.]

## Skill Version(s):

0.1.6 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
