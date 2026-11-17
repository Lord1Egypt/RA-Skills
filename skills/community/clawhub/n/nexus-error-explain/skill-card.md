## Description:

Explain error messages and suggest fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send error text to the NEXUS service and receive explanations with suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Error text can contain secrets, private code, internal hostnames, customer data, or credentials that would be sent to a paid third-party service.

Mitigation: Review and redact sensitive error details before use, and install only when the NEXUS service is trusted for the data being submitted.

Risk: The skill may make paid external requests using payment credentials without clear per-request consent boundaries.

Mitigation: Use sandbox mode or require explicit confirmation before each paid request where the agent runtime supports it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-error-explain)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [NEXUS x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [NEXUS MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [NEXUS AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [NEXUS XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [NEXUS Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [NEXUS A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object containing a result string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill calls a paid external HTTPS service and returns the service response.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
