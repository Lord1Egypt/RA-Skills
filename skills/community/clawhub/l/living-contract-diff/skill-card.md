## Description:

Compare observed API responses with an OpenAPI 3.x specification to identify contract drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT

## Use Case:

Developers and API engineers use the skill to compare recorded API traffic with an existing OpenAPI specification, review contract drift, and check API changes in CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions retrieve the package from a GitHub repository.

Mitigation: Verify that you trust the repository and review the package before installing it.

Risk: A baseline may retain low-cardinality field values, which can include sensitive data.

Mitigation: Treat baselines as internal artifacts when the recorded traffic may contain sensitive values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raktikoo/skills/living-contract-diff)
- [Repository listed in installation instructions](https://github.com/RakTikoo/living-contract-diff)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [A contract-drift report in plain text, Markdown, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports findings from recorded traffic and an existing specification; does not generate an OpenAPI specification.]

## Skill Version(s):

0.3.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
