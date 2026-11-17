## Description:

Guides users through Palantir Foundry Ontology concepts and helps model Object Types, Link Types, Action Types, Functions, and Interfaces from business scenarios or supplied documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theosunny](https://clawhub.ai/user/theosunny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and Foundry implementers use this skill to understand ontology modeling concepts, extract entities and relationships from Feishu or local documents, and produce implementation-ready ontology designs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Feishu documents, local Markdown files, folders, PDFs, and images supplied for ontology extraction.

Mitigation: Provide only the specific documents needed for modeling and avoid broad folders that may contain unrelated confidential data.

Risk: The skill may save full raw-source copies under ontology/ during document-based modeling.

Mitigation: Review and delete raw_source files when they are no longer needed, especially when inputs contain sensitive business data.

Risk: Generated HTML visualizations may be unsafe when based on documents from untrusted sources.

Mitigation: Treat generated HTML as untrusted content and review it before opening or sharing outside a controlled environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theosunny/skills/ontology-modeling)
- [Object Type](reference/object-type.md)
- [Link Type](reference/link-type.md)
- [Action Type](reference/action-type.md)
- [Function](reference/function.md)
- [Interface](reference/interface.md)
- [Project Management Ontology Example](reference/example-project-mgmt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON, Markdown, OWL/Turtle, HTML, and step-by-step implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated ontology files and raw source extracts under ontology/ during document-based modeling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
