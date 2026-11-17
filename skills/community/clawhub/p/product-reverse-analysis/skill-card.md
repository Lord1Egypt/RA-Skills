## Description:

Analyzes product interface screenshots to infer the product's business loop, technical architecture, and design rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Product, design, and engineering practitioners use this skill to analyze product screenshots, identify interface modules, infer business logic and data flows, and document design strengths and risks. The generated analysis is intended for competitive research, product review, and architecture discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots of confidential internal interfaces may expose sensitive product, workflow, or user data during analysis.

Mitigation: Use sanitized screenshots or obtain approval before analyzing confidential interfaces.

Risk: The skill directs the agent to create an MD report, which may persist sensitive screenshot-derived observations.

Mitigation: Confirm the report destination and review the generated file before sharing or retaining it.

Risk: Business logic, architecture, and data-flow conclusions are inferred from screenshots and may be incomplete or inaccurate.

Mitigation: Treat the report as analysis requiring human review, especially before using it for product, security, or compliance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yz6214589-hash/skills/product-reverse-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Chinese Markdown report with tables and Mermaid diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to save the analysis as an MD file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
