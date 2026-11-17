## Description:

Manages project requirement documents by organizing them in a standard ProductManagement folder, reading current project context, and guiding updates to project overview files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinqianfei](https://clawhub.ai/user/jinqianfei)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, developers, and project teams use this skill to keep product requirement, design, development, testing, and release documents organized. It also guides agents to read the latest relevant project files before analysis, design, development, testing, or project-management work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad ProductManagement path could give an agent access to more project documents than intended.

Mitigation: Set PM_PATH narrowly to the intended ProductManagement folder and confirm the resolved path before use.

Risk: Directory creation, file moves, or project overview updates could alter project documentation.

Mitigation: Review proposed document changes and explicitly approve file moves, new directories, and project overview edits before execution.

Risk: Defaulting to the latest version can skip historical documents that are relevant to a task.

Mitigation: Specify exact historical versions when older project context is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinqianfei/skills/project-doc-management)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to use a configured PM_PATH or project-doc configuration file, select the latest document versions by default, and propose document organization changes.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
