## Description:

Audits a specified product flow for business-logic gaps, UX friction, edge cases, and feature modularity using evidence from project files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bergschloss](https://clawhub.ai/user/bergschloss)

### License/Terms of Use:

MIT-0

## Use Case:

Product teams and developers use this skill to review one user flow or module at a time, identify evidence-backed UX and product-logic issues, and prioritize improvements without changing project source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may be stored in a synced or shared Desktop folder.

Mitigation: Review the output folder and choose a private location before auditing sensitive project files.

Risk: The optional multi-agent pipeline can increase tool usage and repeat repository reading.

Mitigation: Use a single scoped audit unless independent parallel runs are needed, and monitor tool usage.

## Reference(s):

- [Product Ux Audit on ClawHub](https://clawhub.ai/bergschloss/skills/product-ux-audit)
- [Source repository (server-resolved provenance)](https://github.com/Bergschloss/product-ux-audit)
- [Multi-agent audit pipeline example](artifact/tasks-pipeline-example.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped, evidence-backed phase reports and a consolidated summary; optional journey map and competitor benchmark.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
