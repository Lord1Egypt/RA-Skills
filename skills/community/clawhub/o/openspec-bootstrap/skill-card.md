## Description:

Bootstraps OpenSpec/SDD workflows for projects by installing and initializing OpenSpec and customizing openspec/config.yaml with project-specific stack, structure, and engineering conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nieen](https://clawhub.ai/user/nieen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add OpenSpec/SDD workflows to new or existing projects, initialize supported agent integrations, and replace the default OpenSpec config with project-specific context and rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may perform a global npm install of OpenSpec.

Mitigation: Confirm the package and installation approach are acceptable before running the skill.

Risk: The workflow may generate or overwrite OpenSpec-related project files.

Mitigation: Run it in a clean git worktree and review the resulting diff before keeping the changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nieen/skills/openspec-bootstrap)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec npm Package](https://www.npmjs.com/package/@fission-ai/openspec)
- [OpenSpec Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install OpenSpec globally and create or overwrite OpenSpec-related project files, including openspec/config.yaml and selected agent integration files.]

## Skill Version(s):

2.0.0 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
