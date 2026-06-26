## Description: <br>
Query Nile Markets -- on-chain FX markets powered by the Open Nile Protocol, starting with non-deliverable forwards (NDFs), through a read-only MCP integration for pool state, positions, oracle prices, and account data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taiyangc](https://clawhub.ai/user/taiyangc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DeFi users can use this skill to query Nile Markets testnet protocol data, including pool health, positions, oracle prices, account state, fee analytics, token balances, allowances, and trade simulations. It is intended for read-only analysis through a configured Nile Markets MCP endpoint, not wallet management or on-chain execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses and query details may be visible to the configured MCP server. <br>
Mitigation: Use an endpoint you trust and avoid sending sensitive addresses or query details unless that disclosure is acceptable. <br>
Risk: The skill reports Sepolia testnet data and the API is under active development, so results may not reflect production market conditions. <br>
Mitigation: Treat responses as testnet protocol data, verify network and freshness metadata when available, and avoid using outputs as real-money trading instructions. <br>
Risk: Users may ask the agent to manage wallets, sign transactions, transfer tokens, or submit on-chain writes that this skill cannot perform. <br>
Mitigation: Keep usage read-only and refuse requests for wallet control or transaction execution; use the Nile Markets web application or contract ABIs outside the skill for on-chain operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/taiyangc/nile-markets) <br>
- [Nile Markets Protocol Docs](https://docs.nilemarkets.com) <br>
- [Nile Markets MCP Server Docs](https://docs.nilemarkets.com/ai-agents/mcp-server) <br>
- [Nile Markets Smart Contract Reference](https://docs.nilemarkets.com/smart-contracts) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Natural-language responses grounded in MCP tool data, with setup guidance for the Nile Markets MCP endpoint.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NILE_MCP_URL. MCP responses include protocol, network, data, and may include freshness metadata such as _meta.lastIndexedBlock.] <br>

## Skill Version(s): <br>
0.3.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
