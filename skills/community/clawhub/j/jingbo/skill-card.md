## Description:

Provides Rain Classroom account and class query support for user IDs, teaching lists, class data, warning lists, today's lessons, homework status, and announcement-read status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuetangop](https://clawhub.ai/user/xuetangop)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and teaching staff use this skill to configure access to a Rain Classroom MCP service and query classroom, teaching, warning, reservation, homework, and announcement data through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow handles the Rain Classroom secret and writes MCP configuration.

Mitigation: Use an environment variable for the secret, avoid pasting it into chat or logs, and review generated MCP configuration before use.

Risk: Security evidence reports hidden authenticated install reporting and an unsafe shell command path.

Mitigation: Review the setup scripts before installing, avoid elevated privileges, and prefer manual MCP configuration until those issues are fixed.

## Reference(s):

- [Jingbo ClawHub Skill Page](https://clawhub.ai/xuetangop/skills/jingbo)
- [Rain Classroom Secret Setup](https://ykt-envning.rainclassroom.com/ai-workspace/open-claw-skill)
- [API References](references/api_references.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured lists, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool call guidance, manual MCP configuration snippets, and reminders to preserve returned course data without inventing records.]

## Skill Version(s):

1.0.327852 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
