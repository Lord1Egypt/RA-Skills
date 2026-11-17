## Description:

Extract structured data from text documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to send document text to the NEXUS service and receive extracted structured data. It is suited to workflows that can use a paid remote extraction API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document text is sent to NEXUS for server-side AI processing.

Mitigation: Do not submit secrets, regulated data, or confidential documents unless the organization permits this provider and endpoint.

Risk: The skill uses a per-request payment model for normal service calls.

Mitigation: Confirm payment requirements before use and use the documented sandbox path only for testing.

Risk: The skill depends on a remote service endpoint being trusted and available.

Mitigation: Deploy only where remote processing by this provider is acceptable, and handle API failures or payment challenges in the calling workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-document-extract)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Document Extract API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/document-extract)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar Info](https://ai-service-hub-15.emergent.host/api/mpp/stellar)
- [Fee Sponsorship](https://ai-service-hub-15.emergent.host/api/mpp/stellar/sponsor-info)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing a result string with extracted structured data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and NEXUS_PAYMENT_PROOF; sends input text to a remote NEXUS API.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
