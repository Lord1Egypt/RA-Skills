## Description:

Generates architecture and sequence diagrams as PNG files using Mermaid syntax and the mermaid.ink renderer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opietaylor911](https://clawhub.ai/user/opietaylor911)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create Mermaid-based architecture, network, cloud, microservices, API flow, authentication flow, CI/CD, and database flow diagrams as editable source and rendered PNG files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram source is sent to the external mermaid.ink renderer, which may expose confidential architecture, topology, customer data, credentials, tokens, or regulated information.

Mitigation: Use this skill only for non-confidential diagrams unless it is changed to use a local renderer or require explicit consent before each upload.

Risk: The skill text mentions local rendering with mmdc while its workflow actually uses mermaid.ink.

Mitigation: Review the selected rendering path before deployment and document whether rendering is local or external.

## Reference(s):

- [Mermaid Architecture Diagram Patterns](references/architecture-patterns.md)
- [Mermaid Sequence Diagram Patterns](references/sequence-patterns.md)
- [mermaid.ink renderer](https://mermaid.ink/img/${ENCODED}?bgColor=white&width=2048)
- [ClawHub skill page](https://clawhub.ai/opietaylor911/skills/isai-mermaid-diagrams)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with Mermaid code, shell commands, .mmd source files, and PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagram source is encoded and sent to mermaid.ink for rendering; default PNG width is 2048px.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
