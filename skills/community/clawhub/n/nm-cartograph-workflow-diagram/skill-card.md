## Description:

Generates a Mermaid workflow diagram showing process steps, decisions, and state transitions

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn code or documentation about CI/CD pipelines, lifecycle processes, and state machines into workflow diagrams that show their steps and decision points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Codebase-derived diagram content sent to Mermaid Chart could disclose confidential deployment steps, identifiers, security gates, or operational logic.

Mitigation: Check repository privacy rules before use and avoid sending diagram content that includes confidential operational details.

## Reference(s):


## Skill Output:

**Output Type(s):** [Code, Markdown]

**Output Format:** [Mermaid flowchart syntax with a rendered diagram and brief description]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagrams are limited to 20 nodes and include a decision point. Error or fallback paths use dotted arrows when present.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
