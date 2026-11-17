## Description:

Context-aware AI partner for data processing, debugging, workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to send task context to the NEXUS AI Teammate service for data processing, debugging, and workflow support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends task inputs and payment proof data to the NEXUS remote service over HTTPS.

Mitigation: Avoid sending secrets, private customer data, or internal source context unless the provider is trusted for that data.

Risk: Normal use may require paid requests through supported payment protocols.

Mitigation: Use a low-scope or sandbox payment proof where possible and confirm the selected payment requirement before retrying a paid request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-teammate)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON service response containing a result string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HTTPS network access and a NEXUS_PAYMENT_PROOF value or supported payment credential.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
