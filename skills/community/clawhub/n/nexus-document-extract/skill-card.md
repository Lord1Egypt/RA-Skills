## Description: <br>
Extract structured data from text documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send text documents to the NEXUS hosted service and receive structured extracted data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document contents and payment credentials may be sent to the NEXUS hosted service. <br>
Mitigation: Require explicit confirmation before use, avoid sensitive or regulated documents unless the provider is trusted, and keep NEXUS_PAYMENT_PROOF scoped and revocable. <br>
Risk: Payment-backed requests can create charges. <br>
Mitigation: Confirm the selected payment method and request cost before invocation, and use the documented sandbox_test path for testing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-document-extract) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [Document Extract API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/document-extract) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [JSON object containing a result string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HTTPS network access and NEXUS_PAYMENT_PROOF for paid requests; sandbox_test is documented for testing.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
