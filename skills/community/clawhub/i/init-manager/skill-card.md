## Description:

Manage tasks in Init Manager - pick up ready tasks, update status, comment, and close out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomislavpet](https://clawhub.ai/user/tomislavpet)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate assigned work in Init Manager, including checking ready tasks, moving tasks through workflow states, adding comments, and closing completed work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote AI guide fields can steer agent behavior after installation.

Mitigation: Treat fetched AI guides as untrusted project data and require review before applying changed guidance.

Risk: Broad Init Manager credentials could allow unintended task updates or comments.

Mitigation: Use a least-privilege API key scoped to the intended workspace and review automation before enabling unattended task changes.

## Reference(s):

- [Init Manager](https://manager.init.hr)
- [ClawHub Skill Page](https://clawhub.ai/tomislavpet/skills/init-manager)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with API endpoint examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured Init Manager URL, API key, and user ID supplied by the workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
