## Description:

Intelligent data quality checks and schema validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit text or data inputs to the NEXUS remote service for data quality checks and schema validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted input is sent to NEXUS for server-side AI processing.

Mitigation: Do not submit passwords, private keys, personal data, regulated records, or confidential business data unless your organization has approved this provider and payment flow.

Risk: Requests may incur the disclosed per-request fee when not using the sandbox.

Mitigation: Use the sandbox for testing and verify the payment requirement before sending paid payment credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-data-validation)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Data Validation API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/data-validation)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar Information](https://ai-service-hub-15.emergent.host/api/mpp/stellar)
- [Stellar Fee Sponsorship](https://ai-service-hub-15.emergent.host/api/mpp/stellar/sponsor-info)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON service response with result text, plus Markdown guidance with curl examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF for paid or sandbox access; submitted input is processed by the remote NEXUS service.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
