## Description:

Issue Register creates standardized issue-registration notes in a WizNote project issue directory and maintains a project issue overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangfengxiang](https://clawhub.ai/user/wangfengxiang)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using WizNote use this skill to capture, update, and track project issues as collaborative notes. It is intended for issue intake, status tracking, ownership assignment, and overview maintenance within a configured project path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically read and rewrite collaborative issue notes with unclear project scoping.

Mitigation: Review the configured project name, category path, and overview docGuid before installing, and use it only in WizNote workspaces where creating, updating, and rebuilding issue notes is acceptable.

Risk: Overview rebuilding may affect existing issue records if matching searches are broader than the intended project.

Mitigation: Scope overview searches to the selected project path and show the resolved target before writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangfengxiang/skills/issue-register)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown issue notes and overview content, with a shell command used to obtain the current date]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates WizNote issue records and regenerates a project overview from matching issue notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
