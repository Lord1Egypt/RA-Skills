## Description: <br>
Query prediction markets, place trades, and manage positions with the Polymarket CLI for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Polymarket markets, inspect prices and order books, track positions, and, with explicit confirmation, place or manage trades through the Polymarket CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for financial preferences or trading-related notes to persist across sessions. <br>
Mitigation: Save preferences only after explicit user permission, and do not store private keys or sensitive wallet configuration. <br>
Risk: Trading, approvals, API-key deletion, notification deletion, and automation commands can affect account state or funds. <br>
Mitigation: Require explicit confirmation before each high-impact action and show market details, prices, and order parameters before execution. <br>
Risk: Wallet files and private keys could be exposed if the agent reads local configuration or runs wallet-management commands. <br>
Mitigation: Do not read ~/.config/polymarket/config.json or files containing private keys; wallet create, import, show, and reset commands must be run directly by the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/polymarket-cli) <br>
- [Skill homepage](https://clawic.com/skills/polymarket-cli) <br>
- [Polymarket CLI repository](https://github.com/Polymarket/polymarket-cli) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polygon RPC](https://polygon-rpc.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON-producing CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may access external Polymarket and Polygon services; trading and wallet-related actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
