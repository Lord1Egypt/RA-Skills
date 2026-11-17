## Description:

Smart multi-model AI gateway on Cardano that routes prompts to supported LLMs with automatic fallback, tiered pricing, and an OpenAI-compatible format paid through Masumi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to send prompts or OpenAI-compatible message arrays to a paid remote LLM gateway that can route across multiple model tiers and payment protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and OpenAI-compatible message arrays are sent to a remote LLM gateway for processing.

Mitigation: Avoid sending secrets, regulated data, or confidential prompts unless the service has been reviewed for the intended data class.

Risk: The skill can make paid remote LLM calls under broad auto-invocation conditions.

Mitigation: Use sandbox or short-lived, limited payment credentials where possible, and confirm the agent's invocation and spending controls before deployment.

Risk: Payment proofs or credentials may be included in request headers for paid or legacy flows.

Mitigation: Limit credential scope and lifetime, store payment proof values outside prompts, and rotate them if exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-llm-gateway)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [LLM Gateway Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/llm-gateway)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar Fee Sponsorship](https://ai-service-hub-15.emergent.host/api/mpp/stellar/sponsor-info)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON service response containing model-generated content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires payment authorization for normal use; legacy calls may use NEXUS_PAYMENT_PROOF, and sandbox_test is documented for free testing.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
