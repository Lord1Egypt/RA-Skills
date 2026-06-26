## Description: <br>
Summarize long documents while preserving key information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to condense long documents into concise summaries through a NEXUS remote API. It is suited for paid remote summarization workflows where sending document text to the service provider is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document text is sent to a paid remote summarization provider. <br>
Mitigation: Use only with documents that are acceptable under the provider's privacy and billing terms; avoid confidential, regulated, credential-containing, or proprietary content unless approved. <br>
Risk: The skill handles payment-proof values and can use paid remote API workflows. <br>
Mitigation: Configure NEXUS_PAYMENT_PROOF deliberately, review expected cost and currency before use, and restrict installation to agents authorized for payment workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-summarize) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [Summarize API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/summarize) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Text or JSON service response, often presented as a concise summary in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a remote HTTPS API call and a configured payment proof or payment credential.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
