## Description: <br>
Draft professional communications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to draft professional email or message content through a paid NEXUS remote service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make paid remote drafting requests and has payment authority. <br>
Mitigation: Confirm before paid requests or payment transactions, and set clear spending controls before use. <br>
Risk: Inputs are sent to an external NEXUS service for LLM processing. <br>
Mitigation: Do not send secrets, regulated data, or sensitive personal or business communications unless that external processing is approved. <br>
Risk: Broad auto-invocation could route matching communication tasks to the remote provider. <br>
Mitigation: Review the invocation scope and payment proof environment variable before installing or enabling the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-email-compose) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [Email Compose API](https://ai-service-hub-15.emergent.host/api/original-services/email-compose) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [Stellar Fee Sponsorship](https://ai-service-hub-15.emergent.host/api/mpp/stellar/sponsor-info) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object containing a result string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or a supported payment credential; requests are sent to an external NEXUS API.] <br>

## Skill Version(s): <br>
2.1.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
