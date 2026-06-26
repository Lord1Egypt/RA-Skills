## Description: <br>
Intelligent data quality checks and schema validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send input text to the NEXUS data validation API for data quality checks and schema validation. The service requires network access and a NEXUS payment proof or supported payment credential. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input data is sent to an external paid AI validation service. <br>
Mitigation: Install only when the user trusts NEXUS with the data being validated, and redact secrets or regulated data before use. <br>
Risk: Automatic invocation can trigger payment-backed requests. <br>
Mitigation: Require explicit confirmation before sending paid requests, and use sandbox_test or narrowly scoped payment credentials where possible. <br>
Risk: The skill requires payment proof or payment credentials for normal operation. <br>
Mitigation: Configure the NEXUS_PAYMENT_PROOF environment variable only in trusted environments and avoid broad credential reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-data-validation) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [Data validation API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/data-validation) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object containing a result string from the external validation service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and NEXUS_PAYMENT_PROOF or a supported payment credential.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
