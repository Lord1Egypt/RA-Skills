## Description: <br>
Generate technical documentation from code or specs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to send code or specifications to the NEXUS documentation service and receive generated technical documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided code or specifications to a remote NEXUS service for processing. <br>
Mitigation: Avoid submitting sensitive content unless the service is trusted for that data, and keep secrets out of submitted inputs. <br>
Risk: Normal use can trigger paid remote requests through payment credentials or payment proofs. <br>
Mitigation: Use sandbox or tightly scoped payment credentials where possible, and configure confirmations or spending limits for paid calls. <br>


## Reference(s): <br>
- [NEXUS Agent-as-a-Service Platform](https://ai-service-hub-15.emergent.host) <br>
- [NEXUS Doc Writer API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/doc-writer) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON object containing a generated documentation string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a payment proof or payment credential for paid service calls; sandbox testing is available through the documented payment-proof header.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
