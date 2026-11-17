## Description:

Traces execution paths through the code graph with criticality scoring and Mermaid charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to trace how a function executes through a codebase, assess the path's criticality factors, and present the results as a call tree and Mermaid flowchart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes a configuration-directory search and had medium confidence because inspection was partial.

Mitigation: Review the skill instructions and confirm that the described search fits your intended use before installing.

Risk: Two local references could not be matched to bundled files during inspection.

Mitigation: Check any referenced resources you rely on before following their guidance.

## Reference(s):

- [ClawHub call-chain release](https://clawhub.ai/athola/skills/nm-cartograph-call-chain)
- [Cartograph project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with an indented call tree, Mermaid flowchart, and criticality breakdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Graph-based tracing requires the gauntlet plugin and graph data; otherwise the skill guides static call-pattern analysis.]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
