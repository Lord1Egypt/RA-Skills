## Description:

backend-api-designer helps agents provide Chinese-language backend architecture, business solution, workflow diagram, Go-style API, and MySQL schema design guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjypink1211](https://clawhub.ai/user/jjjypink1211)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze existing backend projects and produce business solution documents, architecture plans, Mermaid diagrams, Go-style gRPC/HTTP interfaces, and MySQL table designs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The engineering-analysis mode may inspect project files such as proto, SQL, Go, and service code.

Mitigation: Provide only project paths that the agent is intended to inspect, and review generated architecture or schema recommendations before implementation.

## Reference(s):

- [Common Business Scenario Design Patterns](references/patterns.md)
- [Architecture Design Patterns](references/architecture-patterns.md)
- [Mermaid Diagram Syntax Quick Reference](references/mermaid-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Mermaid, protobuf, SQL, and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language design guidance; repository analysis mode may read user-provided project files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
