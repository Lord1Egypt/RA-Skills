## Description:

Use when managing work with OrgX to report progress, request decisions, register artifacts, sync memory, check quality gates, or view org status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hopeatina](https://clawhub.ai/user/hopeatina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agent work to OrgX for progress reporting, decision requests, artifact registration, quality scoring, entity tracking, and run control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send status, task details, memory summaries, and logs to an external OrgX service.

Mitigation: Use it only where this data sharing is acceptable, and avoid syncing raw memory or daily logs that may contain secrets or sensitive internal information.

Risk: The skill uses ORGX_API_KEY and plugin installation paths that could expose credentials if copied into chats, logs, or repositories.

Mitigation: Keep ORGX_API_KEY out of chats, logs, and repositories, and prefer a pinned reviewed plugin version before deployment.

## Reference(s):

- [OrgX ClawHub Skill Page](https://clawhub.ai/hopeatina/skills/orgx)
- [hopeatina ClawHub Publisher Profile](https://clawhub.ai/user/hopeatina)
- [OrgX Live Dashboard](http://127.0.0.1:18789/orgx/live)
- [OrgX MCP Server](https://mcp.useorgx.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown with inline shell commands and structured tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference ORGX_API_KEY and OrgX MCP tools for reporting, synchronization, quality scoring, and entity management.]

## Skill Version(s):

3.1.0 (source: server release metadata; artifact frontmatter says 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
