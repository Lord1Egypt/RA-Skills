## Description:

多 Agent 项目协作工厂 - 一键实现智能分工完成互联网项目

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninetyhe-90](https://clawhub.ai/user/ninetyhe-90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to scaffold and run a multi-agent project workflow for software projects. It helps divide work into requirements, research, architecture, implementation, and testing outputs coordinated across specialized agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can recursively delete an existing directory if an unsafe project path is supplied and overwrite is confirmed.

Mitigation: Run it from an isolated workspace, pass only a simple new directory name, and resolve and verify any existing path before confirming overwrite.

Risk: Agent-generated project plans, code, and test reports can contain incorrect or incomplete guidance.

Mitigation: Review generated requirements, architecture, code, and tests before relying on them for deployment or customer-facing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninetyhe-90/skills/multi-agent-project-builder)
- [Related skill: multi-agent-coordination](../multi-agent-coordination/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown project documents, YAML configuration, generated directories, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a project workspace with PROJECT_CONFIG.yaml, EXECUTION_GUIDE.md, README.md, .gitignore, and staged output folders for requirements, research, architecture, implementation, and testing.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
