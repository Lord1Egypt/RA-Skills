## Description: <br>
Trade and monitor Hyperliquid perpetual futures, including balances, positions with P&L, market analysis, order placement, order cancellation, and market trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anajuliabit](https://clawhub.ai/user/anajuliabit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to monitor Hyperliquid perpetual futures portfolios, analyze market momentum, inspect positions and balances, and prepare or execute trading commands with explicit wallet configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live trading power when HYPERLIQUID_PRIVATE_KEY is configured. <br>
Mitigation: Use testnet or a dedicated limited trading wallet, keep main wallet keys out of the agent environment, and manually verify every order before execution. <br>
Risk: The cancel-all command can cancel open orders across a market scope. <br>
Mitigation: Require explicit user confirmation for cancel-all actions and review the affected coin or account before running the command. <br>
Risk: The position checker writes portfolio state to a hard-coded local path. <br>
Mitigation: Remove or change the hard-coded trading-state path if local portfolio data should not be written there. <br>
Risk: Automated market signals may be incorrect or misleading for high-risk crypto perpetual futures trading. <br>
Mitigation: Treat analysis as informational, verify prices and position size independently, and do not rely on signals as financial advice. <br>


## Reference(s): <br>
- [Hyperliquid API Reference](references/api.md) <br>
- [Official Hyperliquid Documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/) <br>
- [ClawHub Skill Page](https://clawhub.ai/anajuliabit/hyperliquid-trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trading commands can call live Hyperliquid endpoints when credentials are configured; read-only commands can use a public wallet address.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
