## Description:

Generates a Mermaid dependency graph showing import relationships between modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand module dependencies, find circular dependencies, assess coupling, and plan refactors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering may send module names and dependency relationships from a codebase to Mermaid Chart.

Mitigation: Before analyzing a private repository, review Mermaid Chart's destination and data-handling practices; use local rendering or obtain appropriate approval if repository details are sensitive.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-cartograph-dependency-graph)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Code, Text]

**Output Format:** [Mermaid flowchart syntax with concise dependency analysis notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directed dependency relationships, including internal and external imports.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
