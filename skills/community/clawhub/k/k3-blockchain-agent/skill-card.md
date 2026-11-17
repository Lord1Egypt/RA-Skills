## Description:

Builds automated blockchain analysis workflows on K3 from natural language requests to deployed automations that fetch on-chain data, analyze it with AI, and deliver insights via email, Telegram, or Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexgrankinukr-hash](https://clawhub.ai/user/alexgrankinukr-hash)

### License/Terms of Use:


## Use Case:

Developers and blockchain operators use this skill to create K3 workflows for on-chain analytics, wallet and contract monitoring, DeFi reports, alerts, Telegram bots, and optional blockchain actions. It helps an agent clarify requirements, discover data sources, test workflow inputs, deploy K3 automations, and verify runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create persistent K3 automations that send workflow data to third-party destinations.

Mitigation: Require final user review before deployment, verify email, Telegram, Slack, webhook, API, and Google Sheets destinations, and confirm scheduled workflows can be paused or revoked.

Risk: The skill can guide workflows that execute swaps, token transfers, Coinbase or Uniswap actions, or smart contract writes.

Mitigation: Use testnet or limited-fund wallets for action workflows, require explicit approval for trade and contract-write conditions, and set practical limits before enabling live funds.

Risk: Incorrect endpoints, chain-specific addresses, missing credentials, or rate limits can produce empty or misleading workflow data.

Mitigation: Create and run a minimal data-fetch test workflow, inspect returned data with workflow run details, and fix the source before deploying the full automation.

Risk: API keys, bot tokens, and MCP integration credentials may be exposed or misused if embedded directly in workflow instructions.

Mitigation: Use connected K3 or MCP integrations for credentials, avoid placing secrets in prompts or reports, and verify credential scopes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexgrankinukr-hash/skills/k3-blockchain-agent)
- [Data Sources Discovery Guide](references/data-sources.md)
- [K3 Node Types Reference](references/node-types.md)
- [Workflow Patterns](references/workflow-patterns.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with K3 workflow configuration details and tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide persistent K3 workflow deployment after user review; no local executable code is included in the artifact.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
