## Description:

Auto-monitor MCP servers and AI services with health checks, auto-restart on failure, and Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reikys](https://clawhub.ai/user/reikys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up recurring health checks for MCP servers and related AI services, with failure logging, optional Telegram alerts, and configurable service restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The healthcheck script loads a shell environment file, so an unsafe or writable config file can execute shell code whenever the monitor runs.

Mitigation: Use a dedicated, locked-down config file and review the configuration before enabling scheduled execution.

Risk: Configured service labels can be stopped and started automatically when checks fail.

Mitigation: Confirm every service label and test the monitor manually before enabling LaunchAgent, cron, or systemd scheduling.

Risk: Telegram alerts can send service failure details to Telegram when credentials are configured.

Mitigation: Use Telegram alerts only where that disclosure is acceptable and keep bot tokens and chat IDs in a protected config file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reikys/skills/mcp-health-monitor)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for a configurable Bash healthcheck script that can log service status, send Telegram alerts, and restart configured services.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
