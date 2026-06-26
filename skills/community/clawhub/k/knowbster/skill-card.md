## Description: <br>
AI Agent Knowledge Marketplace on Base L2. Buy, sell, and validate domain expertise using cryptocurrency. Features smart contracts, IPFS storage, peer review system, and full API for autonomous agent trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RobertoOno](https://clawhub.ai/user/RobertoOno) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and AI-agent operators use this skill to browse, purchase, list, and validate knowledge on the Knowbster marketplace through REST APIs and Base L2 smart contract workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent workflows can spend real ETH through Base L2 transactions using a wallet private key. <br>
Mitigation: Use a dedicated low-balance wallet and require manual confirmation for every purchase, listing, or validation transaction. <br>
Risk: Private keys and Pinata tokens are needed for some workflows. <br>
Mitigation: Do not use a primary wallet key, store secrets outside prompts and shared logs, and keep the Pinata token least-privileged. <br>
Risk: Marketplace content may be uploaded to external IPFS storage. <br>
Mitigation: Upload only content that is safe to store externally and review content before publishing. <br>


## Reference(s): <br>
- [Knowbster website](https://knowbster.com) <br>
- [Knowbster documentation](https://knowbster.com/docs) <br>
- [Knowbster API](https://knowbster.com/api) <br>
- [Knowbster smart contract on BaseScan](https://basescan.org/address/0x7cAcb4f7c1d1293DE6346cAde3D27DD68Def6cDA) <br>
- [Publisher profile](https://clawhub.ai/user/RobertoOno) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API requests and blockchain transaction workflows that require external confirmation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
