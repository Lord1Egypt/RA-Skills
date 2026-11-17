## Description:

Converts PRDs, requirement documents, or business descriptions into AI-friendly DDD domain design documents in Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qitongfire](https://clawhub.ai/user/qitongfire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and AI coding agents use this skill before implementation to turn natural language requirements into DDD models, aggregate designs, ER diagrams, database schema mappings, domain logic placement, API contracts, and behavior diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated domain designs may misinterpret requirements or introduce architecture decisions that are not valid for the target system.

Mitigation: Review the generated design document and complete the included quality checklist before using it for implementation.

Risk: The default output may mix Chinese business descriptions with English technical names, which can be unsuitable for some teams or review processes.

Mitigation: Normalize language and naming conventions during review if the project requires a single-language document.

## Reference(s):

- [Skill workflow](artifact/SKILL.md)
- [Phase guide](artifact/phase-guide.md)
- [DDD design template](artifact/ddd-design-template.md)
- [ClawHub skill page](https://clawhub.ai/qitongfire/skills/prd-to-ddd-design)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Structured Markdown with Mermaid diagrams, tables, API contracts, database schema mappings, and package structure guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact directs business descriptions to be written in Chinese and technical names in English.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
