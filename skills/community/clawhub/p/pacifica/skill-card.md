## Description: <br>
Guides an agent in using Pacifica MCP and CLI tools for crypto perpetuals trading, market data, account monitoring, order management, and real-time streams on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockchain-oracle](https://clawhub.ai/user/blockchain-oracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to select Pacifica tools, format trading parameters, inspect markets and accounts, place or manage orders, and monitor live crypto market streams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide wallet-signed trading, leverage, margin, batch order, transfer, withdrawal, and cancel-all actions. <br>
Mitigation: Require explicit user confirmation for every financial action and verify the requested symbol, side, amount, leverage, margin mode, destination account, and withdrawal amount before execution. <br>
Risk: A generated wallet file and private key may control funds. <br>
Mitigation: Use a dedicated low-balance wallet where possible, protect the wallet file, and prefer testnet for evaluation or onboarding. <br>
Risk: Loose triggers may route broad crypto or market requests into trading-capable workflows. <br>
Mitigation: Use read-only market and account tools for informational requests, and escalate to signed tools only after the user clearly requests a specific state-changing action. <br>


## Reference(s): <br>
- [ClawHub Pacifica release](https://clawhub.ai/blockchain-oracle/pacifica) <br>
- [Blockchain Oracle publisher profile](https://clawhub.ai/user/blockchain-oracle) <br>
- [Pacifica website](https://pacifica.fi) <br>
- [Pacifica testnet app](https://test-app.pacifica.fi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text] <br>
**Output Format:** [Markdown guidance with inline tool names, parameters, and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide wallet-signed trading, leverage, margin, transfer, withdrawal, and WebSocket monitoring actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
