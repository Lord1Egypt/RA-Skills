## Description: <br>
On-chain credit scoring and soulbound identity for autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create or query on-chain agent identities, retrieve credit scores, record attestations, compare agents, and generate reputation reports for AI-agent markets, DeFi access, collaboration, and risk assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend wallet gas and create permanent public on-chain identity or attestation records. <br>
Mitigation: Use a dedicated low-balance wallet, prefer Base Sepolia or another testnet, and require explicit approval after reviewing the action, wallet, network, gas estimate, target identity, and permanence. <br>
Risk: The skill requires an Ethereum private key for transaction signing. <br>
Mitigation: Keep private keys out of prompts, logs, and shared files; use a dedicated wallet with minimal funds and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/openclaw-agent-reputation) <br>
- [Project homepage](https://github.com/ZhenRobotics/openclaw-agent-reputation) <br>
- [Project documentation](https://github.com/ZhenRobotics/openclaw-agent-reputation/blob/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language responses with transaction hashes, Markdown tables, JSON reports, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a wallet private key for transaction signing; on-chain writes can spend gas and create permanent public records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
