## Description: <br>
Comprehensive image understanding for objects, text, and colors through the NEXUS paid image-analysis API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to submit image-analysis requests to the NEXUS service and receive structured understanding of image content. It is intended for paid API use with sandbox testing available before payment-backed calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user-provided image content or prompts to the third-party NEXUS service. <br>
Mitigation: Configure the agent to ask before sending images or sensitive content, and avoid private screenshots, IDs, secrets, faces, or regulated content unless the user trusts NEXUS and its retention practices. <br>
Risk: The skill can use payment credentials or payment proofs for paid image-analysis calls. <br>
Mitigation: Use the sandbox proof first, set per-use approval for payment-backed requests, and limit payment credentials available to the agent. <br>
Risk: Clawscan marked the release suspicious because per-use approval rules for content transfer and payment credentials are not clear. <br>
Mitigation: Review the skill before installing and keep agent permissions scoped to network-only access required for the NEXUS endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-image-analysis) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [Image analysis API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/image-analysis) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [Stellar payment information](https://ai-service-hub-15.emergent.host/api/mpp/stellar) <br>
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples and JSON service responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to the NEXUS API and a NEXUS_PAYMENT_PROOF value or supported payment credential for paid requests.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
