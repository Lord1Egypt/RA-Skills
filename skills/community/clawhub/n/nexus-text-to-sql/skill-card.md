## Description:

Convert natural language to optimized SQL queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert natural-language requests into optimized SQL queries through the hosted NEXUS text-to-SQL service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text-to-SQL prompts, payment proof data, and any schema details included in prompts are sent to the hosted NEXUS service.

Mitigation: Avoid sending credentials, personal data, proprietary schema details, or sensitive records unless the organization has approved the external processing and payment flow.

Risk: Normal use may incur paid requests through supported payment protocols and currencies.

Mitigation: Confirm the payment credential, network, asset, and expected cost before use; use the documented sandbox path for testing when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-text-to-sql)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [Text-to-SQL API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/text-to-sql)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)

## Skill Output:

**Output Type(s):** [text, code]

**Output Format:** [JSON object containing a result string with generated SQL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a payment proof or supported x402/MPP payment credential for paid requests.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
