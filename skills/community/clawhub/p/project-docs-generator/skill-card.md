## Description:

Analyzes a codebase and helps generate a customized documentation system, including structure recommendations, technical documentation, API or developer guides, and PlantUML diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardo-lb](https://clawhub.ai/user/leonardo-lb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect a project, identify its technology stack and structure, and create or improve project documentation for onboarding, architecture review, APIs, and development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web searches for unfamiliar frameworks or best practices could expose private project names, module names, endpoints, or architecture details.

Mitigation: Keep analysis local for private repositories unless a human approves sanitized search terms.

Risk: Generated documentation, API descriptions, or architecture diagrams can be incomplete or inaccurate if project analysis misses behavior or context.

Mitigation: Have project maintainers review generated files, examples, links, and PlantUML diagrams before publishing or relying on them.

## Reference(s):

- [Project documentation structure guide](references/doc-structure.md)
- [Technology stack detection methods](references/tech-detection.md)
- [PlantUML diagram patterns](references/diagram-patterns.md)
- [PlantText](https://www.planttext.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation, PlantUML diagram blocks, JSON analysis summaries, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a docs/ directory, documentation templates, and validation output for PlantUML blocks.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
