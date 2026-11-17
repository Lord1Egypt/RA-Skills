## Description:

CLI skill for managing TickTick and dida365 tasks and projects with OAuth2 authentication, task operations, batch updates, priorities, tags, due dates, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage TickTick and dida365 tasks and projects from the command line, including creating, updating, listing, completing, abandoning, and attaching files to tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses TickTick credentials, OAuth tokens, and optional session cookies that can grant read/write access to tasks and projects.

Mitigation: Keep the local config file private with restrictive permissions, avoid sharing or syncing it, and rotate TickTick credentials or session cookies if exposure is suspected.

Risk: Completion, abandonment, batch operations, and attachment uploads can modify real TickTick task data.

Mitigation: Confirm project names, task IDs, and file paths before executing mutating commands, especially batch operations.

Risk: Secrets passed directly on command lines may be retained in shell history or logs.

Mitigation: Prefer interactive entry or controlled configuration workflows and avoid pasting real client secrets or session cookies into logged commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuboacean/skills/liubo-ticktick-cli)
- [TickTick Developer Center](https://developer.ticktick.com/manage)
- [TickTick Open API v1](https://developer.ticktick.com/api)
- [dida365](https://dida365.com)

## Skill Output:

**Output Type(s):** [text, json, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task and project data returned by TickTick APIs; some commands support JSON output for agent workflows.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
