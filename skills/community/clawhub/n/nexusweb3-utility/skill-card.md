## Description: <br>
Read-only API reference for NexusWeb3 utility protocols 11-20 on Base mainnet covering scheduling, oracle, voting, storage, messaging, staking, whitelist, auctions, revenue splitting, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexusweb3dev](https://clawhub.ai/user/nexusweb3dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill as a read-only reference for querying NexusWeb3 utility protocol contracts on Base mainnet. It helps agents find contract addresses, view functions, fee notes, and Solidity call examples without requiring credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes itself as read-only but includes actionable examples for fee-bearing blockchain transactions. <br>
Mitigation: Treat transaction examples as documentation only; do not connect a signing wallet or approve ETH, USDC, or NEXUS operations without independently verifying the contract, amount, recipient, fee, lock period, and permanence of any on-chain data. <br>
Risk: Some documented write operations can spend funds, create permanent on-chain records, or enforce token lock periods. <br>
Mitigation: Prefer read-only calls from this skill, confirm protocol state through trusted sources, and use a transaction-signing workflow only with explicit review of every parameter before signing. <br>


## Reference(s): <br>
- [NexusWeb3 Protocols](https://github.com/nexusweb3dev/nexusweb3-protocols) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>
- [BaseScan](https://basescan.org) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with Solidity code blocks and protocol reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no credentials, downloads, or executable files are included.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; SKILL.md frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
