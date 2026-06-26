## Description: <br>
OpenClawCash crypto wallet API for AI agents (also called openclawcash). Use when an agent needs to send native or token transfers, check balances, list wallets, or interact with EVM and Solana wallets programmatically via OpenClawCash. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macd2](https://clawhub.ai/user/macd2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to operate OpenClawCash-managed wallets, inspect balances and transactions, and execute EVM or Solana transfers, swaps, checkout escrow flows, and Polymarket actions. It requires an OpenClawCash API key and network access to https://openclawcash.com. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent move funds, trade, and manage payment infrastructure. <br>
Mitigation: Use per-action confirmation, low-value or tightly scoped wallets, and limited API-key permissions. <br>
Risk: Wallet imports and private-key handling can expose sensitive credentials. <br>
Mitigation: Avoid importing private keys unless managed custody is intended, and prefer input methods that do not place secrets in shell history or process arguments. <br>
Risk: Checkout webhooks and external MCP package use may expand the trusted surface. <br>
Mitigation: Review webhook destinations carefully and separately review or pin the external MCP package before using the npx path. <br>


## Reference(s): <br>
- [OpenClawCash API Endpoint Details](references/api-endpoints.md) <br>
- [OpenClawCash service](https://openclawcash.com) <br>
- [ClawHub release page](https://clawhub.ai/macd2/open-claw-cash) <br>
- [Publisher profile](https://clawhub.ai/user/macd2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTWALLETAPI_KEY, curl, network access to OpenClawCash, and confirmation for write actions.] <br>

## Skill Version(s): <br>
1.21.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
