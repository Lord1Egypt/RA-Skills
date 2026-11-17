## Description:

Boss AI Agent is an AI management middleware skill that connects messaging, project management, knowledge-base, and email systems with mentor-guided management workflows for Claude Code, ChatGPT, and Gemini via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonypk](https://clawhub.ai/user/tonypk)

### License/Terms of Use:

MIT-0

## Use Case:

Managers, founders, and team leads use this skill to run check-ins, project patrols, briefings, one-on-one preparation, signal scanning, knowledge capture, and emergency response across connected workplace systems. It can also expose management status and board-discussion tools through MCP clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workplace monitoring and employee profiling can collect sensitive employee activity, sentiment, and performance context.

Mitigation: Require explicit employee and organization consent, define retention and deletion rules for profiles, and limit monitoring to approved channels and employees.

Risk: Scheduled jobs can send messages, alerts, and summaries on a recurring basis without fresh review.

Mitigation: Require per-job approval before enabling cron tasks, keep an auditable job list, and pause or remove jobs that are no longer needed.

Risk: Optional cloud configuration can send prompts, employee data, or analytics outside the local environment.

Mitigation: Do not set BOSS_AI_AGENT_API_KEY or BOSS_AI_AGENT_URL unless the endpoint is trusted and a documented cloud data-flow policy is in place.

Risk: Host command and MCP behavior can expand the skill's operational reach beyond ordinary chat guidance.

Mitigation: Pin MCP package versions, restrict available tools, and require review before allowing host command execution in production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonypk/skills/management-brain)
- [Publisher profile](https://clawhub.ai/user/tonypk)
- [Boss AI Agent website](https://manageaibrain.com)
- [Boss AI Agent MCP endpoint](https://manageaibrain.com/mcp)
- [Project repository link from artifact](https://github.com/tonypk/ai-management-brain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, schedule recurring jobs, send messages, write memory records, issue MCP calls, and summarize workplace signals when the host environment grants the required tools.]

## Skill Version(s):

1.3.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
