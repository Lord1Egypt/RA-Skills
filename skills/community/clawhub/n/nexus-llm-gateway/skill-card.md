## Description: <br>
Smart multi-model AI gateway on Cardano that routes prompts to the best LLM (GPT-5.2, Claude Sonnet 4.5, GPT-4o, Claude Haiku 4.5, GPT-4o-mini) with automatic fallback, tiered pricing, OpenAI-compatible format, and ADA payment via Masumi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to route prompts or OpenAI-compatible message arrays to a paid multi-model LLM gateway with tiered routing, fallback, and Cardano, Stellar, and XRPL payment support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and payment credentials are sent to a hosted third-party service. <br>
Mitigation: Install only if you trust NEXUS, avoid secrets or regulated data, and prefer sandbox or tightly limited payment credentials. <br>
Risk: The skill can trigger paid remote calls with unclear per-use limits. <br>
Mitigation: Require explicit confirmation before paid calls and enforce spending limits where the agent environment supports them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-llm-gateway) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON service response containing a result string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a remote HTTPS request and a payment proof or payment credential.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
