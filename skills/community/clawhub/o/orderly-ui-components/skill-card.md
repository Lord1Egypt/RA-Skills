## Description: <br>
Build trading interfaces using pre-built React components - OrderEntry, Positions, TradingPage, WalletConnect, Sheets, Tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to build trading interfaces with Orderly Network React components, including order entry, positions, order books, wallet connection, charts, tables, sheets, and modals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may be adapted into live trading flows involving wallets, orders, positions, withdrawals, or leverage without sufficient user confirmation or sandbox testing. <br>
Mitigation: Test with sandbox accounts first and require explicit confirmations for orders, closes, withdrawals, and leverage changes before connecting to live trading workflows. <br>
Risk: Trading UI code can expose users to account, network, fee, slippage, liquidation, or permission mistakes if important transaction details are hidden or broad authority is granted. <br>
Mitigation: Display network, account, amount, fees, slippage, and liquidation impact before submission, and avoid broad wallet or trading-key authority for unreviewed code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tarnadas/orderly-ui-components) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript, CSS, and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation examples and integration guidance for React trading UI components.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
