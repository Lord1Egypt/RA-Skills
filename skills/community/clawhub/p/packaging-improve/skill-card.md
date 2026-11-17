## Description:

Analyzes Amazon customer reviews for packaging damage, missing parts, unboxing, and storage issues, then proposes evidence-backed packaging improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product operators use this skill to turn review evidence about shipping damage, missing parts, unboxing, and storage into prioritized packaging improvement tasks. It does not handle claims, purchasing, or inventory execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaging-analysis release exposes broader paid services and can initiate paid analysis through a documented preview path.

Mitigation: Use a packaging-only release, keep preview paths free, and check the quote and obtain explicit confirmation before paid analysis.

Risk: Recurring collection or monitoring can create ongoing charges.

Mitigation: Check existing collection schedules and get separate approval for monitoring frequency and cost; use manual collection for a one-time result.

## Reference(s):

- [Packaging operations workflow](references/operation-workflow.md)
- [ARI CLI and API reference](references/reference.md)
- [ARI operations workspace](https://ari.funewa.com/zh/operations)
- [ClawHub release](https://clawhub.ai/funewa/skills/packaging-improve)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with review evidence, packaging improvement tasks, and prioritization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include review sample scope and supporting evidence; an ARI API key is required.]

## Skill Version(s):

1.5.3 (source: server-resolved release version, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
