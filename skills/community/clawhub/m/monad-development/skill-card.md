## Description: <br>
Builds dapps on Monad blockchain. Use when deploying contracts, setting up frontends with viem/wagmi, or verifying contracts on Monad testnet or mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[portdeveloper](https://clawhub.ai/user/portdeveloper) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure Monad projects, deploy and verify smart contracts with Foundry, and set up frontend integrations with viem or wagmi. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to persist or disclose blockchain private keys. <br>
Mitigation: Use a dedicated low-value deployment wallet or secure secret manager, and avoid storing valuable keys in plaintext. <br>
Risk: The skill can guide transaction broadcasts on Monad testnet or mainnet. <br>
Mitigation: Use testnet by default and require explicit user confirmation before any mainnet transaction or broadcast. <br>
Risk: The skill can send contract verification payloads to external APIs. <br>
Mitigation: Review verification payloads before submission, especially compiler metadata, constructor arguments, and contract addresses. <br>


## Reference(s): <br>
- [Monad Development ClawHub Release](https://clawhub.ai/portdeveloper/monad-development) <br>
- [Monad Documentation](https://docs.monad.xyz) <br>
- [Monad LLM Documentation Index](https://docs.monad.xyz/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blockchain transaction, wallet, faucet, and contract verification instructions that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
