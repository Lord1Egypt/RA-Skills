## Description: <br>
Autonomous AI agent for DeFi on Hedera - natural language trading, portfolio management, Power Law BTC rebalancing, HCS signal publishing, limit orders, staking, NFTs, and multi-account wallet operations via SaucerSwap V1/V2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chris0x88](https://clawhub.ai/user/Chris0x88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to manage Hedera DeFi wallet activity through natural-language requests, including portfolio checks, token swaps, transfers, staking, NFT views, limit orders, and BTC rebalancing. The skill is intended to propose and execute live wallet operations through a local launcher with explicit approval for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests powerful wallet access and can execute live Hedera DeFi transactions. <br>
Mitigation: Use a testnet or dedicated low-balance wallet, avoid primary wallet keys, and require explicit approval for every transaction. <br>
Risk: The skill documents daemon activity for rebalancing, limit orders, HCS publication, and related wallet automation. <br>
Mitigation: Inspect the launcher and Python CLI before installation and require explicit approval before daemon start, restart, or any autonomous wallet operation. <br>
Risk: The artifact describes interaction logging and training-data workflows that may retain account and transaction details. <br>
Mitigation: Avoid enabling log or training-data workflows until the retained data and sharing behavior are understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Chris0x88/pacman-hedera) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversational responses with inline shell commands and occasional JSON parsing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Hedera wallet configuration and the PRIVATE_KEY, HEDERA_ACCOUNT_ID, and PACMAN_NETWORK environment variables; ClawHub metadata lists darwin and linux support.] <br>

## Skill Version(s): <br>
5.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
