## Description:

Comprehensive image understanding - objects, text, colors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to submit image-analysis requests to the NEXUS service and receive object, text, and color understanding after payment authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-analysis inputs and payment proofs are sent to a remote NEXUS API for processing.

Mitigation: Use the skill only with data appropriate for the provider, and avoid sending secrets, private images, regulated data, or sensitive account information unless provider handling is acceptable.

Risk: The service is paid per request and requires a payment proof or payment credential.

Mitigation: Confirm payment requirements before use and use the documented sandbox path only when testing behavior without paid settlement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-image-analysis)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [Image analysis endpoint](https://ai-service-hub-15.emergent.host/api/original-services/image-analysis)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar information](https://ai-service-hub-15.emergent.host/api/mpp/stellar)

## Skill Output:

**Output Type(s):** [text, API Calls, guidance]

**Output Format:** [JSON service response with text result content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NEXUS payment proof or x402/MPP payment credential.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
