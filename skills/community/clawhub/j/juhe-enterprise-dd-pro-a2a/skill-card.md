## Description:

Generates a paid standard enterprise due-diligence report using Juhe data, combining company registry details with public business abnormality, enforcement, dishonesty, and high-consumption restriction signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run paid pre-cooperation checks on a specified company, supplier, or customer when they need a concise public-risk report rather than only registry facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment setup references a mutable Alipay installer and enables payment capability.

Mitigation: Use a pinned, reviewed installer version and require explicit user approval before enabling payment features.

Risk: The API example could be unsafe if implemented by interpolating user input into a shell command.

Mitigation: Implement the Juhe request with a structured HTTPS client and JSON serialization rather than shell interpolation.

Risk: Reports may contain sensitive public company and identity-related fields.

Mitigation: Minimize display and retention, mask values identified as personal ID numbers, and avoid logging full reports or raw query keywords.

Risk: Risk modules only query recent first-page records and cap what the report displays.

Mitigation: Label outputs as partial recent records and direct users to official sources for complete and current verification.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/juhemcp/skills/juhe-enterprise-dd-pro-a2a)
- [Skill Instructions](artifact/SKILL.md)
- [Product Definition](artifact/PRODUCT.md)
- [Output Format](artifact/OUT_FORMAT.md)
- [API Response Examples](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown report with structured tables, summary risk light, payment-flow guidance, and HTTPS request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk modules are partial recent records with display caps; identity-card-like values must be masked when shown.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
