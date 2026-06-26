## Description: <br>
Generate a comprehensive portfolio report for a wallet's Uniswap positions across all chains, covering total value, PnL, fee earnings, impermanent loss, and composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and DeFi operators use this skill to summarize Uniswap liquidity positions for a wallet across supported chains, including portfolio value, PnL, fees, impermanent loss, range status, and composition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates portfolio analysis to a portfolio-analyst subagent. <br>
Mitigation: Install only when comfortable with that delegation and review generated reports before acting on recommendations. <br>
Risk: Wallet configuration guidance mentions private-key based setup. <br>
Mitigation: Prefer public wallet addresses for reporting and avoid pasting or storing real private keys in chat, skill files, logs, or plain environment configuration. <br>
Risk: Portfolio data may be delayed by RPC or subgraph synchronization. <br>
Mitigation: Treat reported values as point-in-time estimates and verify critical balances or transactions against trusted data sources before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/portfolio-report) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill specification](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain-text portfolio report with tabular and summary sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet-level totals, position details, PnL, fee earnings, impermanent-loss estimates, range status, and recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
