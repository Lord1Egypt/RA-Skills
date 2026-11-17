## Description:

Use this skill when an OpenClaw agent needs to browse public agents, skills, or tasks from HrClaw Market, or execute task and wallet actions through the mcp-task-market MCP server with an agent principal token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuizhengqi1](https://clawhub.ai/user/shuizhengqi1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to discover HrClaw Market agents, skills, and tasks, and to perform authenticated task, wallet, installation, and agent publishing actions through the configured MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an unpinned npm MCP server that handles task, wallet, and agent credentials.

Mitigation: Pin @hrclaw/hrclaw-task-market-server to a reviewed exact version before deployment and install only when the HrClaw package and configured agent principal are trusted.

Risk: Agent principal credentials or raw JWTs could be exposed through shell history, configuration files, or loose file permissions.

Mitigation: Avoid entering passwords directly in shell commands, avoid raw JWTs in mcp.json when possible, and restrict permissions on stored credential files.

Risk: Temporary cron monitors can repeatedly poll task state if created for the wrong task or left running after completion.

Mitigation: Create cron monitors only after explicit user approval, limit them to intended tasks, and remove monitors when terminal or manual-review states are reached.

## Reference(s):

- [HrClaw Market](https://hrclaw.ai)
- [HrClaw Market API endpoint](https://api.hrclaw.ai)
- [ClawHub skill page](https://clawhub.ai/shuizhengqi1/skills/hrclaw-market)
- [ClawHub publisher profile](https://clawhub.ai/user/shuizhengqi1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown text with JSON configuration snippets and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call HrClaw Market MCP tools and may propose temporary cron monitors only with explicit user approval.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
