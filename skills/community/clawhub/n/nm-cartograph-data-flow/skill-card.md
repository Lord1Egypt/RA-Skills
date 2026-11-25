## Description:

Generates a Mermaid sequence diagram showing how data moves between components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to trace request flows, API call chains, and data transformations in a codebase. It turns the structural model into a Mermaid sequence diagram for documenting how data moves between components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send diagram syntax and codebase-derived scope information to Mermaid Chart for rendering, which may disclose private repository details.

Mitigation: Check organizational disclosure rules before using the external renderer; for private repositories, use a local rendering workflow or return Mermaid source unless external sharing is authorized.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-cartograph-data-flow)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Diagram, Text, Code]

**Output Format:** [Mermaid sequence diagram with a brief Markdown description]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Request and response flow with up to 10 participants.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
