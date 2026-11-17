## Description:

Create, edit, improve, or audit AgentSkills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuchang8877](https://clawhub.ai/user/liuchang8877)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create new AgentSkills, improve or audit existing skill directories, validate skill structure, and package skills for distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or edited skill content could add incorrect guidance, persistent memory, hooks, or secrets that affect later agent behavior.

Mitigation: Review generated skill changes before use or publication, avoid embedding real secrets, and scan skills before deployment.

Risk: Packaging a local skill directory could distribute unintended files if the source folder is not reviewed first.

Mitigation: Package only reviewed skill directories, use the bundled validation and packaging checks, and inspect archive contents before distribution.

## Reference(s):

- [Agent Skill Design Patterns](references/patterns.md)
- [Workflow Patterns](references/workflows.md)
- [Output Patterns & Templates](references/output-patterns.md)
- [Skill Creator on ClawHub](https://clawhub.ai/liuchang8877/skills/liuchang-skill-creator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code blocks, generated files, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill directories and produce .skill package archives when its bundled scripts are used.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
