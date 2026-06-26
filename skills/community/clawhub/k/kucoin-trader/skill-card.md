## Description: <br>
Professional KuCoin (KC) trading system - multi-account support, spot/margin/futures trading, asset transfers. Use to check balances, transfer assets, open/close positions, and manage your KuCoin portfolio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dex-scan](https://clawhub.ai/user/dex-scan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage KuCoin accounts from an agent, including checking balances and market data, querying orders, transferring assets, and placing spot, margin, or futures trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live KuCoin exchange-trading authority, including transfers, borrowing, repayment, leverage changes, cancellations, and trades. <br>
Mitigation: Install only when live account control is intended; use restricted API keys, disable withdrawals unless required, apply IP restrictions where possible, and require manual confirmation outside the skill before account-changing actions. <br>
Risk: Using full trading credentials for read-only workflows exposes unnecessary account-control capability. <br>
Mitigation: Prefer read-only KuCoin keys for balance, order, and market queries, and separate higher-privilege keys from routine agent use. <br>


## Reference(s): <br>
- [KuCoin API Documentation](https://docs.kucoin.com/) <br>
- [ClawHub skill page](https://clawhub.ai/dex-scan/kucoin-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and KuCoin API credentials configured via environment variables or ~/.openclaw/credentials/kucoin.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact package.json and skill.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
