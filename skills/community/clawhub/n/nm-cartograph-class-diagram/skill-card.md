## Description:

Generates a Mermaid class diagram showing types, inheritance, and composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to understand class hierarchies, composition, and public APIs in a codebase. It produces a Mermaid class diagram with a brief structural analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Codebase-derived details may be sent to Mermaid Chart during rendering without users being warned or checking whether sharing is allowed.

Mitigation: Before rendering, check repository sharing rules and Mermaid Chart's data-handling practices.

## Reference(s):

- [Class Diagram skill on ClawHub](https://clawhub.ai/athola/skills/nm-cartograph-class-diagram)
- [Cartograph plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Code, Analysis]

**Output Format:** [Mermaid class diagram source with concise Markdown analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows public methods and key attributes; the skill specifies a limit of 12–15 classes.]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
