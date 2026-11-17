## Description:

Helps agents look up company details and return field-level source evidence, including excerpts, retrieval dates, and source agreement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arzuo](https://clawhub.ai/user/arzuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check company identity, location, leadership, and other details against cited public sources before relying on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names or domains submitted for lookup are sent to an external service.

Mitigation: Only submit lookup inputs you are comfortable sharing with the Mercator endpoint.

Risk: Paid lookups use an agent-controlled x402 payment flow; unresolved or insufficient-evidence lookups may still incur the stated $0.10 USDC charge.

Mitigation: Use the free validation route first, apply tight wallet spending limits, and check the charged response header.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/arzuo/skills/mercator-entity-evidence)
- [Mercator Entity Evidence service](https://mercator-entity-evidence.fly.dev)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell examples and sourced company facts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The service describes field-level source URLs, excerpts, retrieval dates, confidence, and source agreement; unsupported fields return UNKNOWN.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
