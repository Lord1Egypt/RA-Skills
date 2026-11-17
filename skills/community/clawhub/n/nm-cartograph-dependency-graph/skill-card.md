## Description:

Generates a Mermaid dependency graph showing import relationships between modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to visualize import dependencies between modules, packages, or plugins, helping them understand coupling, find circular dependencies, and assess refactoring impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency names and relationships may be sent to Mermaid Chart without a privacy warning.

Mitigation: Before installing, check whether sharing dependency information with Mermaid Chart is acceptable and whether that destination is approved under your repository’s data-sharing rules.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-cartograph-dependency-graph)
- [Project page listed in Clawdis metadata](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Mermaid flowchart with dependency analysis notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows directed import relationships, dependency groupings, external or optional dependencies, and any detected cycles.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
