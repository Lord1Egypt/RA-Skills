## Description:

Summarize long documents while preserving key information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to condense long text into concise summaries through the NEXUS remote summarization API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text and payment proof or credential headers are sent to the NEXUS API at ai-service-hub-15.emergent.host.

Mitigation: Avoid confidential, regulated, or secret material unless the provider's privacy and retention claims are trusted and use is approved.

Risk: Normal use is a paid remote AI service request.

Mitigation: Review the payment challenge and selected asset before retrying with credentials; use the documented sandbox flow for testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-summarize)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [JSON response containing a summary string, commonly rendered as plain text or bullet-point Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote service response; input text and payment credentials are sent to the NEXUS API.]

## Skill Version(s):

2.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
