## Description: <br>
Guides an agent in using the `polymarket` CLI to browse markets, inspect CLOB data, review wallet or account state, and place or cancel orders with wallet-safety guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ItsNash0](https://clawhub.ai/user/ItsNash0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to research Polymarket markets, inspect price and wallet data, and prepare CLI commands for trading workflows. It is especially useful when the agent must distinguish read-only market research from sensitive trading, approval, bridge, API-key, notification, or wallet-management actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide sensitive Polymarket actions such as order placement, cancellation, approvals, bridge operations, API-key changes, and notification changes. <br>
Mitigation: Use it mostly for read-only research unless the user intentionally wants to trade, and verify the exact market or token, side, price, size, and account before approving any sensitive action. <br>
Risk: Wallet setup, import, show, reset, and address commands may expose or modify private-key configuration. <br>
Mitigation: Keep wallet-management commands user-only, never paste a private key into chat, and have the user run setup or wallet commands directly in their own terminal. <br>


## Reference(s): <br>
- [Polymarket CLI command map](references/command-map.md) <br>
- [Polymarket CLI GitHub repository](https://github.com/Polymarket/polymarket-cli) <br>
- [ClawHub skill page](https://clawhub.ai/ItsNash0/nash0-polymarket-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers `-o json` for automation; sensitive trading and wallet-adjacent commands require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
