## Description:

Statistical profiling and quality assessment of datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to send dataset text or dataset descriptions to the NEXUS service for statistical profiling and quality assessment, with payment proof credentials when required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text or dataset content is sent to a third-party remote service for processing.

Mitigation: Avoid submitting secrets, regulated personal data, or proprietary datasets unless the user trusts the provider and has authorization.

Risk: The skill depends on a payment proof flow for paid remote requests.

Mitigation: Confirm payment credentials, selected network, and expected request cost before using the skill with production workflows.

Risk: Returned profiling or quality assessment results may be incomplete or unsuitable for high-stakes decisions without review.

Mitigation: Review service output before relying on it for operational, compliance, financial, or safety-impacting decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-data-profile)
- [NEXUS Agent-as-a-Service Platform](https://ai-service-hub-15.emergent.host)
- [NEXUS Data Profile Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/data-profile)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON object containing a result string, typically surfaced to the agent as text or Markdown guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote HTTPS service response; no local filesystem or shell output.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
