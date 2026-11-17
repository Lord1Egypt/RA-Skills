## Description:

Generate on-chain trust scores for wallets and agents using Masumi transaction data on Cardano.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to request a NEXUS trust and reputation score for a Cardano wallet address or AI agent based on on-chain transaction activity. It is suited to workflows that need wallet or agent trust assessment before interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to make cryptocurrency payments based on service-provided payment requirements.

Mitigation: Require explicit user approval for every non-sandbox payment and verify the recipient, asset, network, and total amount before sending funds.

Risk: Payment costs may exceed user expectations if local wallet controls do not enforce limits.

Mitigation: Cap payments to the advertised $0.75 request price plus clearly understood fees, and use sandbox_test where possible.

Risk: Wallet addresses, agent identifiers, and input queries are sent to a third-party remote API.

Mitigation: Install only in environments that trust NEXUS as the service provider and avoid sending sensitive data that should not leave the local environment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cyberforexblockchain/skills/nexus-trust-score)
- [NEXUS Agent-as-a-Service Platform](https://ai-service-hub-15.emergent.host)
- [Trust Score API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/trust-score)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar payment information](https://ai-service-hub-15.emergent.host/api/mpp/stellar)
- [Stellar fee sponsorship information](https://ai-service-hub-15.emergent.host/api/mpp/stellar/sponsor-info)
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON service response summarized as Markdown guidance, with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a payment proof or x402/MPP payment credential; sandbox_test is documented for testing.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
