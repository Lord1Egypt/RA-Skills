## Description:

AI agent for automated prediction market trading on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arubiku](https://clawhub.ai/user/arubiku)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to analyze Polymarket markets, detect arbitrage opportunities, and prepare or execute automated trades with configured risk limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports automated real-money prediction-market trading.

Mitigation: Require explicit confirmation and hard value limits before any live trade.

Risk: The setup asks users to expose a wallet private key to an unspecified command-line tool.

Mitigation: Use only a dedicated low-value wallet, avoid exposing a main wallet private key, and verify the exact mia-polymarket executable and source before installing.

## Reference(s):

- [Mia Polymarket Trader on ClawHub](https://clawhub.ai/arubiku/skills/mia-polymarket-trader)
- [Polymarket](https://polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market analysis, trading commands, wallet/API configuration steps, and risk-control guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
