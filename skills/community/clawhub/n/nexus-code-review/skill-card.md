## Description: <br>
Security, performance, and style analysis for code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to send code to the NEXUS remote service for security, performance, and style review. It can return bug, vulnerability, and improvement guidance after payment proof or sandbox authorization is supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Source code and prompts are sent to a third-party remote service for analysis. <br>
Mitigation: Review code before submission and redact secrets, credentials, customer data, and proprietary material that should not leave the environment. <br>
Risk: The skill can process payment authorization for paid remote requests. <br>
Mitigation: Use sandbox_test or a tightly scoped payment proof where possible, and configure the agent to ask before each paid request. <br>
Risk: Security evidence marks the release as suspicious because approval limits for remote paid requests are not clear. <br>
Mitigation: Install only when the publisher and NEXUS service are trusted for the intended code and payment workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-code-review) <br>
- [NEXUS Agent-as-a-Service platform](https://ai-service-hub-15.emergent.host) <br>
- [NEXUS code review API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/code-review) <br>
- [MPP discovery endpoint](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [x402 discovery endpoint](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [AP2 configuration endpoint](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration endpoint](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry endpoint](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, API Calls] <br>
**Output Format:** [JSON service response with text review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to the NEXUS service and a payment proof or sandbox test value.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
