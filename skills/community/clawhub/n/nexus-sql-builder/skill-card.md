## Description:

Generate complex SQL queries from requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to turn natural-language SQL requirements into complex SQL query output through the paid NEXUS remote service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and payment proof data are sent to the external NEXUS service.

Mitigation: Install only if you trust NEXUS; avoid production credentials, raw customer data, and confidential schema details unless your organization permits sharing them.

Risk: Generated SQL may be incorrect, inefficient, or unsafe for the target database.

Mitigation: Review and test generated SQL in a sandbox or with least-privilege access before using it against production systems.

Risk: Paid remote use can incur spending through the supported payment flows.

Mitigation: Use sandbox testing and spending controls where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-sql-builder)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [SQL Builder API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/sql-builder)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON service response containing a result string, often SQL text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF and sends input plus payment proof data to NEXUS over HTTPS.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
