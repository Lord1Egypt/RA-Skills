## Description: <br>
Generate and explain cron expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an OpenClaw agent to generate or explain cron expressions. Requests are sent to the hosted NEXUS cron-builder service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron-related prompts are sent to a third-party paid endpoint. <br>
Mitigation: Review inputs before use, avoid sending sensitive schedule details, and use an offline cron-expression tool when remote processing is not needed. <br>
Risk: The skill requires payment proof credentials and supports paid service flows. <br>
Mitigation: Keep NEXUS_PAYMENT_PROOF scoped, prefer explicit confirmation before paid remote calls, and use sandbox testing where supported. <br>
Risk: The security scan verdict is suspicious because the artifact combines a simple cron helper with paid remote-service behavior and ambiguous automatic invocation. <br>
Mitigation: Review the invocation behavior and payment terms before installing, monitor usage, and disable the skill if automatic invocation is unsuitable for the environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-cron-builder) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [Cron Builder Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/cron-builder) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API calls] <br>
**Output Format:** [JSON service response, typically rendered by the agent as text or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and NEXUS_PAYMENT_PROOF for paid requests; sandbox_test may be available for testing.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
