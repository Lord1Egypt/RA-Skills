## Description:

Provides an OpenClaw workflow for creating and maintaining a personal Feishu Bitable worklist, including task capture, status updates, reminders, reviews, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13929110463](https://clawhub.ai/user/13929110463)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use this skill to set up a Feishu Bitable worklist, add tasks after required field confirmation, update task status, receive reminders, and review progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent OpenClaw reminders automatically.

Mitigation: Review reminder setup before installing and verify created reminders are scoped to the intended Feishu recipient.

Risk: The skill requires Feishu Bitable read/write authority, Feishu app credentials, permission-management ability, and access to a user's open_id.

Mitigation: Use a least-privilege Feishu app, restrict table access to the intended worklist, and provide credentials only through the expected configuration path.

Risk: Evidence flags unsafe command and credential configuration handling.

Mitigation: Fix the open_id/config handling before normal use and run the skill only in a trusted OpenClaw workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/13929110463/skills/personal-worklist-via-feishu)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute bundled Node.js scripts to read or write Feishu Bitable records, configure table permissions, and create OpenClaw reminders.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
