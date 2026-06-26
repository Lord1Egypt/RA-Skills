## Description: <br>
Who is this wallet and what have they been doing? Identity labels, balance, PnL summary, recent transactions, perp positions, and counterparties. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to profile Ethereum wallet activity with Nansen CLI commands, including identity labels, token balances, PnL, recent transactions, perpetual positions, and counterparties. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Nansen CLI commands that require a configured Nansen API key. <br>
Mitigation: Confirm the nansen-cli package is trusted, configure NANSEN_API_KEY only in the intended environment, and review unexpected nansen commands before execution. <br>


## Reference(s): <br>
- [Nansen Wallet Deep Dive on ClawHub](https://clawhub.ai/nansen-devops/nansen-wallet-deep-dive) <br>
- [nansen-cli package](https://www.npmjs.com/package/nansen-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen binary and NANSEN_API_KEY environment variable.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
