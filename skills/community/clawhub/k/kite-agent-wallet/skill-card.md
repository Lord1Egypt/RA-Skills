## Description: <br>
Provides a modular smart wallet protocol for AI agents, including session keys, spending limits, and delegated transaction management on the Kite AI network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nihaovand](https://clawhub.ai/user/nihaovand) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and wallet operators use this skill to guide smart wallet setup and delegated transaction workflows for AI agents on Kite AI, including session-key authorization, spending limits, and contract configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes real on-chain wallet delegation and transaction execution without enough contract provenance. <br>
Mitigation: Start on testnet and independently verify the Kite chain IDs, RPC endpoints, contract source, ownership, and deployed addresses before use. <br>
Risk: Delegated session keys and spending limits can expose wallets to unauthorized or excessive transactions if configured too broadly. <br>
Mitigation: Use isolated wallets with minimal funds, narrow function allowlists, low spending limits, revocable session keys, and explicit approval before wallet creation, session-key grants, or transaction execution. <br>


## Reference(s): <br>
- [Kite AI Docs](https://docs.gokite.ai) <br>
- [Biconomy Nexus Documentation](https://docs.biconomy.io/new/learn-about-biconomy/nexus) <br>
- [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) <br>
- [ERC-7579](https://eips.ethereum.org/EIPS/eip-7579) <br>
- [ClawHub Release Page](https://clawhub.ai/nihaovand/kite-agent-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with JavaScript examples and contract configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Kite network chain IDs, RPC endpoints, explorer URLs, and deployed testnet contract addresses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
