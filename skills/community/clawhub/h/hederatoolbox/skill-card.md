## Description: <br>
Query live Hedera blockchain data - token prices, whale movements, HCS topics, governance proposals, identity/KYC screening, and smart contract analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mountainmystic](https://clawhub.ai/user/mountainmystic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use HederaToolbox to query Hedera market, HCS, governance, identity, compliance, and smart contract data through pay-per-call MCP tools. It is suited for workflows such as whale alerts, DAO governance digests, compliance record checks, and smart contract due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent tool calls can spend prepaid HBAR from the configured HederaToolbox balance. <br>
Mitigation: Start with a small prepaid balance, monitor the balance, and require manual approval for paid calls. <br>
Risk: HCS write operations can create persistent on-chain records that include submitted data. <br>
Mitigation: Require manual approval for HCS writes and avoid sending sensitive identity or compliance data unless it is necessary. <br>
Risk: Tool calls send account IDs, contract addresses, token IDs, and query parameters to the HederaToolbox API. <br>
Mitigation: Review data handling requirements before use and avoid sending sensitive data that is not needed for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mountainmystic/hederatoolbox) <br>
- [Publisher Profile](https://clawhub.ai/user/mountainmystic) <br>
- [HederaToolbox Website](https://hederatoolbox.com) <br>
- [HederaToolbox GitHub Repository](https://github.com/mountainmystic/hederatoolbox) <br>
- [HederaToolbox MCP Endpoint](https://api.hederatoolbox.com/mcp) <br>
- [Platform Wallet on Hashscan](https://hashscan.io/mainnet/account/0.0.10309126) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and structured tool responses from MCP calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live blockchain data, account identifiers, token identifiers, contract identifiers, HCS topic data, compliance records, and risk summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
