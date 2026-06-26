## Description: <br>
Context-aware AI partner for data processing, debugging, workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call a paid NEXUS AI teammate for data processing, debugging, and workflow assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan reports this as a disclosed paid remote AI service whose broad automatic invocation and payment authority need review before use. <br>
Mitigation: Use sandbox testing first, restrict payment credentials, and require explicit human approval before making paid requests. <br>
Risk: Prompts, code, logs, and workflow data sent through the skill are processed by NEXUS. <br>
Mitigation: Install only if you trust NEXUS with that data, and avoid sending confidential data unless the service is approved for that use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-teammate) <br>
- [NEXUS Agent-as-a-Service Platform](https://ai-service-hub-15.emergent.host) <br>
- [NEXUS service endpoint](https://ai-service-hub-15.emergent.host/api/original-services/teammate) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [JSON object with a result string from the remote NEXUS service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or a supported payment credential; requests are sent to the NEXUS service.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata, changelog, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
