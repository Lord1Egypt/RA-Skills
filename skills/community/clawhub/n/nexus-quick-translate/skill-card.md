## Description:

Fast lightweight translation for short texts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to translate short text through the NEXUS remote service after satisfying supported payment requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends text to a remote NEXUS service for translation.

Mitigation: Do not use it for secrets, credentials, regulated data, or confidential documents unless remote processing by this provider is acceptable.

Risk: The skill requires a payment proof or payment credential for billed requests.

Mitigation: Install only when the user trusts NEXUS with the payment proof used for billing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-quick-translate)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Quick Translate API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/quick-translate)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [JSON service response containing a result string, with Markdown usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or a supported x402, MPP, AP2, or legacy payment credential.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
