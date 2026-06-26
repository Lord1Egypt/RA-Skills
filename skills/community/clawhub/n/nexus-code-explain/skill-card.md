## Description: <br>
Explain code in plain language with complexity analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send code or code-related questions to the NEXUS service for plain-language explanation and complexity analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code or text submitted for explanation is sent to a third-party NEXUS endpoint for remote processing. <br>
Mitigation: Avoid sending secrets, credentials, or proprietary code unless the NEXUS service is approved for that data. <br>
Risk: Requests can require payment authorization or a payment proof. <br>
Mitigation: Use sandbox_test or a tightly scoped payment proof when evaluating the skill, and configure the agent to ask before paid remote calls if supported. <br>
Risk: The security summary flags unclear per-request control over paid remote calls. <br>
Mitigation: Install only in trusted environments and review payment requirements before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-code-explain) <br>
- [NEXUS Agent-as-a-Service Platform](https://ai-service-hub-15.emergent.host) <br>
- [Code Explain API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/code-explain) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON object containing a result string; human-facing content may be plain text or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and a NEXUS_PAYMENT_PROOF or supported payment credential; no filesystem or shell access is declared.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
