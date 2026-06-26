## Description: <br>
A command-line skill built on the LongPort OpenAPI Python SDK for quotes, account positions, order management, and market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankxiong](https://clawhub.ai/user/frankxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent query LongBridge brokerage market data, account balances, positions, orders, and, when explicitly enabled, submit or cancel limit orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to sensitive LongBridge brokerage account data. <br>
Mitigation: Install only for intended brokerage workflows, use paper-trading or least-privilege credentials where possible, and avoid shared or synced directories for credential files. <br>
Risk: If trading is enabled, buy, sell, and cancel commands can affect a live brokerage account. <br>
Mitigation: Keep LONGBRIDGE_TRADE_ENABLED unset or false by default and enable it only for deliberate trading sessions. <br>
Risk: The documented --yes/-y option bypasses trade confirmation prompts for programmatic use. <br>
Mitigation: Avoid --yes/-y for live trades and require human review before submitting or cancelling orders. <br>


## Reference(s): <br>
- [LongPort OpenAPI](https://open.longportapp.com/) <br>
- [ClawHub skill page](https://clawhub.ai/frankxiong/longbridge-kit) <br>
- [Publisher profile](https://clawhub.ai/user/frankxiong) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON-capable CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LongBridge API credentials and supports optional named profiles for account selection.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
