## Description:

Monitors websites, APIs, and cron jobs using Watch.dog, including status checks, uptime review, monitor creation, watchdog setup, and monitored-resource management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinson0594](https://clawhub.ai/user/robinson0594)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and operations teams use this skill to connect an agent to Watch.dog for uptime monitoring, heartbeat watchdogs, status summaries, and monitor or status-page management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Watch.dog API key that can access and manage monitoring resources.

Mitigation: Use environment-injected secrets where possible, avoid committing skill-local .env files, and prefer narrowly scoped API keys if Watch.dog supports them.

Risk: The skill can delete monitors or watchdogs and change public status-page configuration.

Mitigation: Require explicit user confirmation before deletions or public status-page changes and manually review the affected monitor, watchdog, or page before execution.

Risk: Changing WATCHDOG_API_URL can direct credentials and tool calls to a non-default endpoint.

Mitigation: Keep WATCHDOG_API_URL pinned to the official Watch.dog endpoint unless the alternative endpoint is fully trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/robinson0594/skills/oda-monitor)
- [Publisher Profile](https://clawhub.ai/user/robinson0594)
- [Watch.dog](https://watch.dog)
- [Watch.dog MCP API Endpoint](https://api.watch.dog/api/mcp_server.php)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with configuration values, status summaries, and command or endpoint instructions when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include monitor IDs, public status-page links, uptime summaries, or watchdog endpoint URLs returned by Watch.dog.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
