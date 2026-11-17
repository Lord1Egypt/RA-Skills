## Description:

Give AI agents on-chain spending guardrails. Deploy ERC-4337 smart accounts with policy-enforced limits - agents cannot move funds beyond what you authorize, enforced at the contract level, not just in software.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnwollenberg](https://clawhub.ai/user/shawnwollenberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure ERC-4337 smart accounts, policies, permissions, validation, and audit workflows for AI agents that need constrained on-chain spending authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports workflows involving financial authority through smart accounts and transaction signing.

Mitigation: Start on testnet, use explicit allowlists and low spending limits, and enable autonomous execution only with secure signing configured.

Risk: Dashboard credentials and planned transaction details may be sent to AgentGuardrail or a configured API endpoint.

Mitigation: Install only when the API endpoint is trusted, use scoped and revocable API keys, and do not set GUARDRAIL_API_URL to an endpoint you do not control or trust.

Risk: Signer tokens and RPC URLs can grant sensitive access or contain embedded credentials.

Mitigation: Store signer tokens, dashboard API keys, and RPC URLs in secure secret storage and avoid exposing them in chat, prompts, logs, or long-lived agent memory.

## Reference(s):

- [AgentGuardrail homepage](https://agentguardrail.xyz)
- [ClawHub skill page](https://clawhub.ai/shawnwollenberg/skills/guardrail-smart-accounts)
- [Publisher profile](https://clawhub.ai/user/shawnwollenberg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include smart contract addresses, environment variable requirements, API request examples, and safety guidance for signing and credentials.]

## Skill Version(s):

1.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
