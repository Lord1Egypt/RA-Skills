## Description: <br>
Routes prompts to the best AI model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to send prompts to the NEXUS multi-model routing service and receive a model-generated response after satisfying the configured payment flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and payment credentials can be sent to the external NEXUS service. <br>
Mitigation: Use the skill only when the operator trusts NEXUS with the submitted prompt content and configured payment credential. <br>
Risk: Paid requests may create spending exposure if payment credentials are used without clear limits. <br>
Mitigation: Confirm retention terms and spending controls before using production payment credentials; use sandbox testing where appropriate. <br>
Risk: Sensitive or regulated information may be exposed through server-side AI processing. <br>
Mitigation: Avoid sending secrets, regulated data, or proprietary context unless the service terms and data handling controls have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-multi-model) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [Multi-model API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/multi-model) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [text, API response, shell commands, guidance] <br>
**Output Format:** [JSON response containing a result string; documentation includes Markdown and curl examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a NEXUS payment proof or supported payment credential before normal paid use.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
