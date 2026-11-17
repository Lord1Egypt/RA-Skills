## Description:

High-quality translations with cultural awareness across 50+ languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send text to the NEXUS translation service and receive culturally aware translations. It supports paid agent requests through x402, MPP, Masumi, AP2, and XRPL payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for translation and payment proof data are sent to an external NEXUS API.

Mitigation: Use the skill only with text and payment credentials approved for third-party processing, and avoid secrets, regulated data, or proprietary content unless organizational policy allows it.

Risk: Non-sandbox requests are priced per request.

Mitigation: Confirm payment network, asset, and amount before retrying a request with a payment credential.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-translate)
- [Publisher Profile](https://clawhub.ai/user/cyberforexblockchain)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Translation API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/translate)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, API Calls, Shell commands, guidance]

**Output Format:** [Text or JSON service response with Markdown usage guidance and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NEXUS payment proof or supported payment credential for paid requests; sandbox testing is described in the artifact.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
