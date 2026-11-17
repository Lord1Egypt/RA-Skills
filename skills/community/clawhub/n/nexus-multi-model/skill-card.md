## Description:

Routes prompts to the best AI model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to route prompts through the NEXUS hosted multi-model service when they want model selection based on task type and cost optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt contents and payment proof material are sent to the NEXUS hosted service.

Mitigation: Ask before sending sensitive prompts or payment proof material, and use sandbox testing until the provider and payment flow are trusted.

Risk: The skill invokes a paid remote service.

Mitigation: Confirm payment requirements before retrying requests with payment credentials, and prefer sandbox_test for initial validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-multi-model)
- [Publisher profile](https://clawhub.ai/user/cyberforexblockchain)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [Multi-model API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/multi-model)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [JSON response containing a result string, with payment and receipt headers when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or a supported payment credential; sandbox_test is documented for free sandbox use.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
