## Description: <br>
Complete financial infrastructure for AI agents on Base mainnet: wallet, identity, payments, yield, insurance, reputation, marketplace, bridge, governance, and launchpad. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexusweb3dev](https://clawhub.ai/user/nexusweb3dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to configure AI agents for NexusWeb3 protocol interactions on Base mainnet, including vault setup, identity registration, payments, yield, insurance, reputation, marketplace, bridge, governance, and launchpad workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables agent interaction with real Base mainnet contracts and live wallet authority. <br>
Mitigation: Use only a dedicated low-balance wallet or tightly capped operator key, never a primary wallet key. <br>
Risk: Approval and fund-moving transactions can expose assets if executed incorrectly. <br>
Mitigation: Manually review every approval, recipient, amount, contract address, and fund-moving transaction before execution. <br>
Risk: A leaked or misused operator key can spend up to its configured allowance. <br>
Mitigation: Set narrow spending limits and be prepared to revoke or rotate the key immediately if activity looks wrong. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nexusweb3dev/nexusweb3) <br>
- [AgentVaultFactory contract on BaseScan](https://basescan.org/address/0x1F28579F8C2dffde8746169116bb3a4d9E516f5A) <br>
- [Publisher profile](https://clawhub.ai/user/nexusweb3dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, configuration notes, contract call examples, and transaction guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Base mainnet addresses, required environment variable guidance, and risk-sensitive setup recommendations] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
