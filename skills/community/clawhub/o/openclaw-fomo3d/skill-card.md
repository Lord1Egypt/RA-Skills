## Description: <br>
Openclaw Fomo3d provides a CLI for interacting with Fomo3D, slot-machine, token-trading, and prediction-market flows on BNB Chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ErenVance](https://clawhub.ai/user/ErenVance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a BNB Chain wallet, query Fomo3D game state, trade FOMO tokens, run slot-machine actions, and create or participate in prediction markets. Agents should use it when the user asks for Fomo3D gameplay, token trading, prediction-market operations, or wallet status workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a private key for signing BNB Chain transactions. <br>
Mitigation: Use a dedicated low-balance wallet, prefer environment variables over saved config files, and avoid using wallets that hold valuable assets. <br>
Risk: Buy, sell, bet, deposit, propose, and dispute commands can submit irreversible live transactions that may lose funds. <br>
Mitigation: Start on testnet, inspect command parameters before execution, use small amounts, and confirm the selected network before submitting transactions. <br>
Risk: The buy and sell flows document zero minimum output, which means there is no slippage protection. <br>
Mitigation: Avoid large trades through this skill unless slippage controls are added or the transaction is independently reviewed. <br>
Risk: Slot prize-pool deposits are documented as permanently locked. <br>
Mitigation: Warn users before running slot deposit commands and require explicit confirmation of the amount and permanence. <br>
Risk: Automatic token approvals may leave allowances after use. <br>
Mitigation: Review and revoke token allowances after completing game, trading, or prediction-market actions. <br>


## Reference(s): <br>
- [Fomo3D Homepage](https://fomo3d.app) <br>
- [Openclaw Fomo3d on ClawHub](https://clawhub.ai/ErenVance/openclaw-fomo3d) <br>
- [BNB Chain Testnet Faucet](https://www.bnbchain.org/en/testnet-faucet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands should normally include --json for machine-readable output.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
