## Description: <br>
Provides Rain Classroom/Yuketang account and class query support, including user ID, teaching classes, class statistics, warning lists, today's teaching, homework submission, and notice-read status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuetangop](https://clawhub.ai/user/xuetangop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers and education staff use this skill to configure a Rain Classroom/Yuketang MCP service and query account, class, warning, teaching, homework, notice, and lesson-reservation data through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Rain Classroom/Yuketang account secret and may store it in MCP client configuration. <br>
Mitigation: Treat YUKETANG_SECRET like a password, avoid pasting it into chat, and rotate it if exposed. <br>
Risk: The security summary says setup behavior is under-disclosed, including a silent install report. <br>
Mitigation: Review setup.sh before installation and remove or disable the claw_report step if telemetry is not acceptable. <br>
Risk: Lesson reservation can create or modify scheduled teaching activity. <br>
Mitigation: Require explicit final user confirmation before calling reservation tools. <br>
Risk: The server verdict is suspicious. <br>
Mitigation: Install only when the publisher is trusted with Rain Classroom/Yuketang account access. <br>


## Reference(s): <br>
- [Rain Classroom secret setup](https://ykt-env-example.rainclassroom.com/ai-workspace/open-claw-skill) <br>
- [Yuketang MCP server](https://open-envning.rainclassroom.com/openapi/v1/mcp-server/sse) <br>
- [API references](references/api_references.md) <br>
- [ClawHub skill page](https://clawhub.ai/xuetangop/mingquan) <br>
- [Publisher profile](https://clawhub.ai/user/xuetangop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YUKETANG_SECRET and a configured yuketang-mcp MCP server.] <br>

## Skill Version(s): <br>
1.0.327851 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
