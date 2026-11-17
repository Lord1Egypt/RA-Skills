## Description:

Security, performance, and style analysis for code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to send code to the NEXUS service for security, performance, and style review before making changes or releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code is sent to a third-party remote service for analysis.

Mitigation: Avoid submitting secrets or private source unless approved for this service; use sandbox mode for evaluation.

Risk: Automatic invocation can trigger a paid cryptocurrency payment workflow.

Mitigation: Require manual confirmation and local checks of amount, recipient, asset, and network before any wallet signs or submits a transaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-code-review)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)
- [Stellar Info](https://ai-service-hub-15.emergent.host/api/mpp/stellar)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Structured service response with code-review findings and suggested improvements.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and NEXUS_PAYMENT_PROOF or sandbox_test; paid requests use x402, MPP, or legacy payment proof headers.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
