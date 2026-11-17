## Description:

Create blog posts, social media, emails, marketing copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send content-generation prompts to the NEXUS hosted service for blog posts, social media posts, emails, and marketing copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic-use behavior could send ordinary writing prompts to a third-party hosted service unexpectedly.

Mitigation: Install only when ordinary writing requests should be eligible for NEXUS hosted processing, and review agent routing before enabling the skill.

Risk: Prompts and payment proof may be sent to a third party, and paid requests may occur when the agent decides the skill matches.

Mitigation: Avoid secrets or regulated content in prompts, and configure payment proof only when paid hosted requests are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-content-generator)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Content Generator Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/content-generator)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Config](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Config](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Text or Markdown content returned in a JSON service response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hosted API response; requests may require payment proof or x402/MPP payment credentials.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
