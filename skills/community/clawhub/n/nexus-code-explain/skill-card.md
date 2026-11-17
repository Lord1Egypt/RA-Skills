## Description:

Explain code in plain language with complexity analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to send code or related questions to the NEXUS hosted service and receive a plain-language explanation with complexity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided code or text is sent to the NEXUS hosted service for processing.

Mitigation: Avoid submitting secrets, credentials, private keys, or proprietary code unless your organization permits that provider.

Risk: The skill depends on a configured payment proof for a paid remote service.

Mitigation: Install only when you are comfortable using the configured NEXUS_PAYMENT_PROOF value with the NEXUS service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/skills/nexus-code-explain)
- [NEXUS platform](https://ai-service-hub-15.emergent.host)
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON response containing a result string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured NEXUS_PAYMENT_PROOF value and sends user-provided input to a remote NEXUS API.]

## Skill Version(s):

2.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
