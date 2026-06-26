## Description: <br>
Trade on GRVT (Gravity Markets) derivatives exchange via the grvt-cli tool for market data, account review, order management, transfers, withdrawals, leverage changes, and trade history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madeinusmate](https://clawhub.ai/user/madeinusmate) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate the grvt-cli for GRVT derivatives market analysis, account monitoring, order placement, and fund management. It is suited to agents that need command guidance for authenticated crypto derivatives workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through crypto derivatives trades, transfers, withdrawals, leverage changes, and stored private-key workflows. <br>
Mitigation: Prefer testnet, avoid large balances or production private keys, and require explicit user approval for each live trade, transfer, withdrawal, leverage change, or secret-bearing config export. <br>
Risk: The underlying CLI stores API keys, private keys, and session cookies on disk. <br>
Mitigation: Use trusted machines only, keep keys out of shell history, rotate or clear credentials after use, and verify secrets are redacted before sharing config output. <br>
Risk: The artifact states that the CLI is a community project with no formal security audit or official GRVT support. <br>
Mitigation: Inform users of the disclaimer before use, review commands before execution, and use dry-run or confirmation prompts for write operations. <br>


## Reference(s): <br>
- [Config and Auth Commands](artifact/references/commands-config.md) <br>
- [Market Data Commands](artifact/references/commands-market.md) <br>
- [Trading Commands](artifact/references/commands-trade.md) <br>
- [Account Commands](artifact/references/commands-account.md) <br>
- [Fund Management Commands](artifact/references/commands-funds.md) <br>
- [Error Handling and Troubleshooting](artifact/references/errors.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/madeinusmate/grvt-markets-agent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON, NDJSON, table, or raw CLI output format guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
