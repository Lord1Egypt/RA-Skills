## Description:

Professional KuCoin (KC) trading system - multi-account support, spot/margin/futures trading, asset transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dex-scan](https://clawhub.ai/user/dex-scan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect KuCoin balances and market data, transfer assets between account types, and manage spot, margin, and futures orders through Node-based commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move funds and place real spot, margin, and futures orders.

Mitigation: Use a minimum-permission KuCoin API key, disable withdrawals, apply exchange-side IP restrictions, and require explicit confirmation or dry-run approval before trades, transfers, cancellations, borrowing, and repayment.

Risk: Leveraged futures and margin actions can amplify losses, including high leverage when a futures trade omits an explicit leverage value.

Mitigation: Avoid futures or margin permissions unless required, enforce conservative leverage limits, require stop-loss review, and remove the executable 125x futures default before production use.

Risk: KuCoin credentials may be stored in a local JSON file or environment variables.

Mitigation: Keep credential files restricted to the local user, rotate keys after testing, and do not grant permissions beyond the specific account actions needed.

## Reference(s):

- [KuCoin API Documentation](https://docs.kucoin.com/)
- [ClawHub Skill Page](https://clawhub.ai/dex-scan/skills/kucoin-trader)
- [Publisher Profile](https://clawhub.ai/user/dex-scan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline Node command examples and JSON credential configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance and executes KuCoin API operations through local Node scripts when invoked by an agent.]

## Skill Version(s):

1.0.1 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
