## Description: <br>
Know Your Agent (KYA). Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billionsnetwork](https://clawhub.ai/user/billionsnetwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage a persistent decentralized identity for an AI agent, link it to a human owner, sign or verify identity challenges, and complete confirmed x402 payment flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived agent private keys may be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not configured. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, use a dedicated no-funds identity key, and restrict ~/.openclaw/billions with chmod 700. <br>
Risk: The skill can sign x402 payments from the agent identity. <br>
Mitigation: Require explicit user confirmation before phase-2 payment execution and present the resource, amount, asset, network, and attestation status before signing. <br>
Risk: Payment challenges and signatures are time-sensitive and should not be reused. <br>
Mitigation: Run the payment discovery flow for each request and use only the fresh paymentRequiredFilePath and selected paymentHash returned by the script. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/billionsnetwork/identity) <br>
- [Billions Network](https://billions.network/) <br>
- [README](README.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Identity Reference](reference/identity/SKILL.md) <br>
- [x402 Payment Reference](reference/x402/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce verification links, DID strings, signed challenge results, payment-option summaries, and protected-resource response data.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
