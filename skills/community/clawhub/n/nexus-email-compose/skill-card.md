## Description:

Draft professional communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft professional emails and messages through the NEXUS remote service after providing an accepted payment proof or sandbox credential.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft content and payment proof information are sent to the NEXUS remote endpoint.

Mitigation: Use only when NEXUS is approved for the data being submitted, and avoid prompts containing secrets, regulated data, or highly sensitive business content.

Risk: The skill requires payment proof handling for normal use.

Mitigation: Use the documented sandbox credential for testing and validate payment details before submitting paid requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-email-compose)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [NEXUS email compose API](https://ai-service-hub-15.emergent.host/api/original-services/email-compose)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON object containing a result string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a remote service response for the submitted input; requires NEXUS_PAYMENT_PROOF for normal paid use.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
