## Description:

Chain multiple AI services into automated workflows - describe a goal and the orchestrator plans, executes, and summarizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to send a goal to the NEXUS orchestration service, which plans and executes a multi-step AI workflow and returns a summarized result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, file snippets, business context, and payment proof values may be sent to the NEXUS remote orchestration service.

Mitigation: Install only when the publisher and service are trusted, treat payment proof values as sensitive, and avoid sending secrets or regulated data unless that data sharing is approved.

Risk: Paid use may create charges through the supported payment protocols and currencies.

Mitigation: Review payment requirements, currency, amount, and destination before authorizing a paid request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-orchestrator)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Orchestrator API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/orchestrator)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar Info](https://ai-service-hub-15.emergent.host/api/mpp/stellar)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [JSON service response with human-readable result text; documentation examples use Markdown with curl commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NEXUS payment proof or supported x402, MPP, AP2, or legacy payment credential.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
