## Description: <br>
PayRam MCP Integration helps agents connect to PayRam's MCP server to create crypto payment links, generate payout and webhook code, scaffold payment apps, and follow headless setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BuddhaSource](https://clawhub.ai/user/BuddhaSource) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and agent builders use this skill to integrate PayRam crypto payment flows, payment links, payouts, referrals, webhooks, and headless setup steps into applications or autonomous agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed setup scripts can modify payment infrastructure or expose wallet-bearing hosts. <br>
Mitigation: Pin and inspect scripts before use, avoid curl-to-bash on production or wallet-bearing machines, and begin with testnet or empty wallets. <br>
Risk: Automated payouts, wallet deployments, contract deployments, or production payment actions can move funds or change infrastructure. <br>
Mitigation: Require explicit human approval for every payout, wallet deployment, contract deployment, or production payment action. <br>
Risk: Local PayRam token or wallet secret files may expose payment infrastructure if handled loosely. <br>
Mitigation: Protect .payraminfo secrets with strong local permissions or a secret manager and keep token or mnemonic files out of version control. <br>


## Reference(s): <br>
- [PayRam MCP Integration Skill Page](https://clawhub.ai/BuddhaSource/payram-mcp-integration) <br>
- [PayRam MCP Documentation](https://docs.payram.com/mcp-integration) <br>
- [PayRam Homepage](https://payram.com) <br>
- [PayRam Helper MCP Server Repository](https://github.com/PayRam/payram-helper-mcp-server) <br>
- [PayRam Headless Agent Guide](https://github.com/PayRam/payram-scripts/blob/main/docs/PAYRAM_HEADLESS_AGENT.md) <br>
- [PayRam Architecture & Security Model](references/architecture.md) <br>
- [PayRam Headless Setup](references/headless-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration steps, and app scaffolding instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose payment, payout, webhook, wallet, contract, or deployment actions that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
