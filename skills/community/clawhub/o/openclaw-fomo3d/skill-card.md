## Description:

Provides a CLI for interacting with Fomo3D, Slot Machine, and Prediction Market contracts on BNB Chain, including status checks, wallet setup, token trades, game actions, and market settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erenvance](https://clawhub.ai/user/erenvance)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent prepare and run Fomo3D CLI commands for wallet checks, game participation, token trading, slot actions, and prediction-market creation, betting, dispute, and settlement workflows on BNB Chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign real-wallet blockchain transactions, which may irreversibly move funds.

Mitigation: Use a dedicated low-value wallet and test on BNB Chain testnet before any mainnet use.

Risk: Private keys may be exposed if stored in local configuration.

Mitigation: Prefer the FOMO3D_PRIVATE_KEY environment variable and avoid saving private keys in config.json.

Risk: Trading commands may use unlimited approvals or execute with no slippage protection.

Mitigation: Review approvals and trade parameters before execution, and avoid mainnet trading unless the user understands the transaction terms.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/erenvance/skills/openclaw-fomo3d)
- [Fomo3D homepage](https://fomo3d.app)
- [BNB Chain testnet faucet](https://www.bnbchain.org/en/testnet-faucet)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON command-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI actions may sign irreversible blockchain transactions when configured with a funded wallet.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
