## Description: <br>
Chain multiple AI services into automated workflows - describe a goal and the orchestrator plans, executes, and summarizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send a goal to the NEXUS service, which plans and executes a multi-step AI workflow and returns a summarized result. It is suited to paid, networked orchestration tasks where the user trusts the NEXUS service and payment flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad task prompts to a paid third-party AI service with unclear automatic trigger and spending controls. <br>
Mitigation: Review the task before invocation, use only approved payment proofs or wallet flows, and set local controls for when the skill may spend or call the service. <br>
Risk: Prompts and task data are sent to ai-service-hub-15.emergent.host for server-side AI processing. <br>
Mitigation: Avoid submitting secrets, private code, regulated data, or sensitive business content unless that sharing is approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-orchestrator) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [Orchestrator API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/orchestrator) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [text, API responses, guidance] <br>
**Output Format:** [JSON response summarized as agent-facing text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to the NEXUS service and a payment proof or payment credential.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
