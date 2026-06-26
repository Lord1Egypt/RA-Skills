## Description: <br>
Statistical profiling and quality assessment of datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and data teams use this skill to send dataset input to the NEXUS service for statistical profiling and quality assessment after satisfying the required payment flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dataset contents are sent to a third-party NEXUS API for processing. <br>
Mitigation: Do not use the skill with secrets, proprietary data, personal data, or regulated records unless provider terms, retention practices, and data handling controls have been reviewed. <br>
Risk: Paid remote calls can create spend or payment exposure. <br>
Mitigation: Use sandbox credentials for testing, set payment limits, and require explicit approval for paid requests. <br>
Risk: The scanner did not identify clear auto-invocation or spend guardrails. <br>
Mitigation: Configure agent policy so profiling requests and payment-bearing calls require deliberate user intent before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-data-profile) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [Stellar payment information](https://ai-service-hub-15.emergent.host/api/mpp/stellar) <br>
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Analysis] <br>
**Output Format:** [JSON object containing a service response string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a network request to the NEXUS API and a valid payment proof or supported payment credential.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
