## Description:

Convert meeting transcripts into structured notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and agents use this skill to turn meeting transcripts into structured notes through the NEXUS hosted service after presenting a payment proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts and a payment proof are sent to the NEXUS hosted service.

Mitigation: Use only for meetings whose contents are approved for that provider and data handling model; avoid confidential, regulated, legal, HR, or customer-sensitive meetings unless approved by the organization.

Risk: The skill depends on a paid external API and payment headers or credentials.

Mitigation: Confirm payment requirements, supported networks, and request costs before production use; use the documented sandbox path for testing where appropriate.

Risk: Generated notes may omit or misstate meeting details because processing is performed by a server-side AI service.

Mitigation: Review generated notes before sharing them or using them as an authoritative record.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-meeting-notes)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Meeting Notes API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/meeting-notes)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar Info](https://ai-service-hub-15.emergent.host/api/mpp/stellar)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Structured meeting notes returned as a service response string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a NEXUS payment proof; no local filesystem or shell access is required.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
