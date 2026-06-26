## Description: <br>
Hyperliquid trading plugin with background position monitoring and custom automations. Execute market orders, limit orders, manage positions, view funding rates, run trading strategies, and write event-driven automation scripts with automatic alerts for PnL changes and liquidation risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ya7ya](https://clawhub.ai/user/ya7ya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent inspect Hyperliquid account state, discover markets, place trades, manage orders, and run monitored trading automations. It is intended for users who deliberately configure a wallet or API key for agent-assisted crypto trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live crypto trades and automate trading decisions. <br>
Mitigation: Install only for intentional agent-assisted trading, test with dry-run and testnet first, and use a dedicated low-balance or restricted API wallet. <br>
Risk: The skill requires sensitive wallet credentials. <br>
Mitigation: Store HYPERLIQUID_PRIVATE_KEY only in trusted agent environments and avoid using a wallet with withdrawal authority when a restricted API wallet is sufficient. <br>
Risk: Persistent automation or forwarding behavior can continue acting after setup. <br>
Mitigation: Inspect generated automation before running it live, monitor active automations, and configure only dashboard or webhook URLs controlled by the user. <br>


## Reference(s): <br>
- [ClawHub Open-broker Skill Page](https://clawhub.ai/ya7ya/openbroker) <br>
- [OpenBroker npm Package](https://www.npmjs.com/package/openbroker-plugin) <br>
- [Hyperliquid App](https://app.hyperliquid.xyz/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, JSON-capable CLI output, and JavaScript automation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 22+, network access to api.hyperliquid.xyz, the openbroker CLI, and HYPERLIQUID_PRIVATE_KEY for live trading.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
