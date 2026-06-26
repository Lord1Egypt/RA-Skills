## Description: <br>
Explain error messages and suggest fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send error text to the NEXUS service and receive explanations plus suggested fixes. It is intended for agent workflows that can approve paid external requests and handle payment proof credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Error text may be sent to an external AI service and can include sensitive diagnostics, secrets, tokens, customer data, or internal hostnames. <br>
Mitigation: Redact sensitive data before use and install only where sending error text to NEXUS is acceptable. <br>
Risk: The skill can use payment credentials for paid external requests without clear per-use approval. <br>
Mitigation: Require explicit approval before each paid call and prefer sandbox or tightly scoped payment credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-error-explain) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [Error explain API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/error-explain) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object with a result string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF for paid requests; sandbox usage is documented by the artifact.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
