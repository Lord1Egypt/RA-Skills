## Description: <br>
Give AI agents on-chain spending guardrails by deploying ERC-4337 smart accounts with policy-enforced limits at the contract level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnwollenberg](https://clawhub.ai/user/shawnwollenberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams building AI agents that transact on-chain use this skill to prepare smart account, policy, permission, validation, audit, and setup guidance for AgentGuardrail workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent workflows can prepare or trigger blockchain operations involving real funds. <br>
Mitigation: Use testnet or small limits first, review actions before execution, and enable autonomous execution only after secure signing and policy limits are configured. <br>
Risk: RPC URLs, signer tokens, dashboard API keys, private keys, or seed phrases can expose wallet authority if mishandled. <br>
Mitigation: Use secure secret storage, prefer an external signer or wallet approval, and never paste private keys or seed phrases into chat. <br>
Risk: Incorrect provider identity or contract addresses can cause transactions to target the wrong service or contracts. <br>
Mitigation: Independently verify provider identity and contract addresses before using mainnet funds. <br>


## Reference(s): <br>
- [AgentGuardrail homepage](https://agentguardrail.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/shawnwollenberg/guardrail-smart-accounts) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Solidity and JavaScript code examples, configuration tables, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blockchain transaction preparation guidance and environment variable requirements; does not handle private keys directly.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
