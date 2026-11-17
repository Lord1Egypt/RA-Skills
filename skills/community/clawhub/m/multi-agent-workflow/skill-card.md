## Description:

A Chinese-language workflow helper that splits complex tasks, assigns agent roles, and summarizes task status for multi-agent collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn a user task into subtasks, select an appropriate role such as content expert, researcher, developer, or reviewer, and prepare structured task status output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect a full multi-agent executor, while the artifact evidence shows a lightweight task splitter and role-assignment helper.

Mitigation: Review the generated task plan and perform any actual agent spawning separately in the host environment.

Risk: Keyword-based role assignment can select an unsuitable role for ambiguous or mixed-language tasks.

Mitigation: Review assigned roles before execution and override the role when the task requires a different specialist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxie48892-jpg/skills/multi-agent-workflow)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-language task, role, capability, and status fields for downstream review or execution.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
