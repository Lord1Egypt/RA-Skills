## Description:

OpenClaw-optimized skill for Texas residential electricity shopping, address completion, candidate confirmation, ESIID lookup, usage estimation, plan recommendation, self-service plan routing, and daily or weekly savings monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catkennel](https://clawhub.ai/user/catkennel)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a Texas residential electricity advisor to confirm a service address, compare current plan options, route to a Personalized Energy address page, and set up daily or weekly monitoring.

### Deployment Geography for Use:

United States (Texas service addresses)

## Known Risks and Mitigations:

Risk: The skill may process exact Texas service addresses, including apartment or unit details, through external services.

Mitigation: Use only when that address data flow is acceptable and give users clear privacy notice and choice before address lookup or plan retrieval.

Risk: Generated Personalized Energy URLs can contain address-specific path data.

Mitigation: Share address-specific URLs only after the user provides and confirms the service address.

Risk: The skill needs an intentionally provisioned POWERLEGO_API_TOKEN for live lookup behavior.

Mitigation: Review configuration before installation and provide the token only in approved environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/catkennel/skills/monitor-openclaw)
- [Personalized Energy Texas Rates](https://www.personalized.energy/electricity-rates/texas)
- [Address Completeness](artifact/references/address-completeness.md)
- [Intent Routing](artifact/references/intent-routing.md)
- [OpenClaw Execution Guide](artifact/references/openclaw-execution.md)
- [Response Strategy](artifact/references/response-strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise advisor responses with numbered address or plan lists and destination URLs when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate addresses, ESIID, estimated usage, top plans, current best plan, Personalized Energy URL, and monitoring recommendation when supported by lookup results.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
