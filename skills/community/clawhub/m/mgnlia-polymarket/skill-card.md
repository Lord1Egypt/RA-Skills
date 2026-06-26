## Description: <br>
Browse, trade, manage positions, and scan expiry arbitrage opportunities on Polymarket prediction markets via the polymarket CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guzus](https://clawhub.ai/user/guzus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search Polymarket markets, inspect odds and order books, manage positions, and prepare CLI-driven trading workflows. Funds-affecting actions require explicit user confirmation of the market, side, price, size, wallet, fees, and irreversible effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real funds through trading, approvals, deposits, split, merge, redeem, cancel, and other wallet-backed actions. <br>
Mitigation: Use read-only commands by default and require explicit confirmation of market, side, price, size, wallet, fees, and irreversible effects before any funds-affecting action. <br>
Risk: The installer fetches and runs remote installation code and may build from source without a pinned, verified release. <br>
Mitigation: Review or replace the installer with a pinned, verified release before installation. <br>
Risk: Private keys can be exposed if pasted into chat or command lines during wallet import or setup. <br>
Mitigation: Do not paste real private keys into chat or command lines; use secure wallet setup practices outside the agent conversation. <br>
Risk: The TypeScript expiry arbitrage scanner constructs a shell command from query text. <br>
Mitigation: Avoid the TypeScript scanner with untrusted query text until its shell command construction is fixed. <br>


## Reference(s): <br>
- [Polymarket CLI GitHub](https://github.com/Polymarket/polymarket-cli) <br>
- [Polymarket Docs](https://docs.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper commands can return JSON from the polymarket CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market research is available without a wallet; trading and on-chain operations require wallet setup and user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
