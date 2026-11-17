## Description:

Generates a Mermaid architecture diagram showing high-level component relationships

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to map how packages, plugins, or modules relate, supporting onboarding, architecture documentation, and PR reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The architecture diagram workflow reportedly sends codebase details to Mermaid Chart, which may disclose sensitive system structure.

Mitigation: Before rendering, check whether the architecture details can be shared with Mermaid Chart; remove sensitive components or obtain approval before submitting them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-cartograph-architecture-diagram)
- [Cartograph plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Code, Image]

**Output Format:** [Mermaid flowchart syntax and rendered diagram]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A high-level diagram that groups related modules into package subgraphs.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
