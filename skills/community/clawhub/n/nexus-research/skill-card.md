## Description: <br>
Deep research on any topic with structured findings and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to send research prompts to the NEXUS remote service and receive structured findings, analysis with sources, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make paid remote research requests and carries payment authority. <br>
Mitigation: Use the sandbox first, require explicit approval for paid calls, and configure spending limits before adding a real payment proof. <br>
Risk: Research prompts are sent to the NEXUS remote service for processing. <br>
Mitigation: Avoid sending secrets, regulated data, or private business data unless the service provider is trusted for that use. <br>
Risk: Automatic invocation could trigger unexpected paid requests when broad research tasks are detected. <br>
Mitigation: Review invocation rules and run the skill only in agent setups that gate network and payment actions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cyberforexblockchain/nexus-research) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [Research API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/research) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object containing a result string from the remote research service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or sandbox_test; paid requests may cost $0.50 each.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
