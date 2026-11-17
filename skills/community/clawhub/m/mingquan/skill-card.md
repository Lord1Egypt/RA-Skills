## Description:

Mingquan helps agents query Rain Classroom account, teaching, class, warning, lesson, homework, notice, and grading data through a configured Rain Classroom MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuetangop](https://clawhub.ai/user/xuetangop)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and teaching staff use this skill to inspect Rain Classroom account identity, teaching lists, class metrics, warning lists, daily lesson status, reservations, grading workload, homework completion, and notice reading status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer handles YUKETANG_SECRET as an account credential and the security evidence flags unsafe secret handling.

Mitigation: Prefer manual MCP configuration or a fixed installer that does not pass the secret through shell-string execution; rotate the secret if it may have been exposed.

Risk: The installer changes MCP configuration for the local project.

Mitigation: Review the generated MCP configuration before use and enable it only in projects where Rain Classroom access is intended.

Risk: The skill can reserve lessons through the Rain Classroom MCP service.

Mitigation: Require user confirmation before reservation actions and verify class, time, title, duration, and meeting type before calling the reservation tool.

Risk: The Unix setup script silently sends an authenticated install-duration report.

Mitigation: Review setup.sh before running it and remove or disable the reporting call if install telemetry is not acceptable.

## Reference(s):

- [Rain Classroom MCP API reference](references/api_references.md)
- [ClawHub skill page](https://clawhub.ai/xuetangop/skills/mingquan)
- [Rain Classroom Secret setup](https://ykt-env-example.rainclassroom.com/ai-workspace/open-claw-skill)
- [Rain Classroom MCP service endpoint](https://open-envning.rainclassroom.com/openapi/v1/mcp-server/sse)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured lists, tables, inline shell commands, and MCP tool call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves tool-returned emoji and original wording; relies on Rain Classroom tool responses for course data.]

## Skill Version(s):

1.0.327851 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
