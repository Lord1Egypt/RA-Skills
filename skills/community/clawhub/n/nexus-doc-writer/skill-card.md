## Description:

Generate technical documentation from code or specs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to generate technical documentation from source code, specifications, or short documentation prompts through the NEXUS remote documentation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted code or specifications are sent to a remote service for processing.

Mitigation: Use the skill only with approved material, avoid secrets or confidential source unless authorized, and install it only if the NEXUS service provider is trusted.

Risk: The payment flow can direct blockchain payments from server-provided terms without a clear local approval gate.

Mitigation: Use sandbox_test first and require manual confirmation plus local checks of recipient, chain, asset, and amount before any real payment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-doc-writer)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Documentation Writer API](https://ai-service-hub-15.emergent.host/api/original-services/doc-writer)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON object containing a result string with generated documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to NEXUS and a payment proof or sandbox credential.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
