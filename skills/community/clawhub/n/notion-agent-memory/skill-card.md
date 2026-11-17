## Description:

Structured memory system for AI agents using Notion, local memory files, ACT framework databases, MEMORY.md templates, and the Continuity Cycle pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladchatware](https://clawhub.ai/user/vladchatware)

### License/Terms of Use:


## Use Case:

Developers, operators, and agent builders use this skill to set up persistent memory files, session continuity routines, optional Notion-backed databases, and check-in templates for agents that need context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may capture sensitive context, credentials, or personal data.

Mitigation: Use the skill only in workspaces where persistent memory is intended, and keep passwords, API keys, cookies, tokens, and other secrets out of memory files, daily logs, AGENTS.md, and Notion pages.

Risk: Heartbeat schedules, cron jobs, or email and calendar monitoring may run without clear operator consent.

Mitigation: Enable scheduled monitoring only after explicitly approving the schedule, command, account, data sources, and removal process.

Risk: Notion API credentials can be mishandled when configuring the optional integration.

Mitigation: Store Notion tokens outside shared memory artifacts, restrict Notion integration permissions, and review workspace sharing before connecting databases.

## Reference(s):

- [Continuity Cycle](references/continuity-cycle.md)
- [Notion Integration Guide](references/notion-integration.md)
- [ACT Framework Database Schemas](references/act-framework.md)
- [Notion API Documentation](https://developers.notion.io)
- [ClawHub Skill Page](https://clawhub.ai/vladchatware/skills/notion-agent-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown templates and setup guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local memory file templates, optional Notion API patterns, and heartbeat state JSON.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
