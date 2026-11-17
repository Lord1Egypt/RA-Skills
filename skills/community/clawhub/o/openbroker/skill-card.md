## Description:

Hyperliquid trading plugin for market and limit orders, position management, funding-rate review, background monitoring, and event-driven automation with alerts for PnL changes and liquidation risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ya7ya](https://clawhub.ai/user/ya7ya)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate Hyperliquid trading workflows, inspect account and market data, place orders, and create monitored trading automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent real-money trading authority through a wallet private key and live Hyperliquid order commands.

Mitigation: Install only with a dedicated, limited wallet, prefer testnet or dry runs first, cap funding and leverage, and avoid broad mainnet permissions.

Risk: Persistent trading automations can continue acting on market events after setup.

Mitigation: Review generated automation code before live runs, require explicit risk limits, monitor positions and liquidation risk, and use stop/cleanup handlers.

Risk: Dashboard forwarding can send audit notes, metrics, and trade actions to a configured endpoint.

Mitigation: Set OB_DASHBOARD_URL only to a trusted endpoint or leave it unset.

Risk: The installed npm package controls trading behavior.

Mitigation: Verify the exact openbroker-plugin package and version before installation.

## Reference(s):

- [Open-broker ClawHub Skill Page](https://clawhub.ai/ya7ya/skills/openbroker)
- [openbroker-plugin npm package](https://www.npmjs.com/package/openbroker-plugin)
- [Hyperliquid App](https://app.hyperliquid.xyz/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, TypeScript automation code, and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22+, network access to api.hyperliquid.xyz, the openbroker CLI, and HYPERLIQUID_PRIVATE_KEY for trading operations.]

## Skill Version(s):

1.2.0 (source: SKILL.md metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
