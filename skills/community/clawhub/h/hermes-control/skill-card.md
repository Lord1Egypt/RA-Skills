## Description:

Hermes Control is a Chinese-language reference skill for operating Hermes Agent through OpenClaw, covering CLI commands, slash commands, tools, configuration, gateways, multi-agent coordination, scheduled jobs, skill management, and automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[internettrollwatt](https://clawhub.ai/user/internettrollwatt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill as a command reference when administering Hermes Agent through OpenClaw, including local CLI operation, messaging gateways, MCP servers, scheduled automation, and skill management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes unsafe installation guidance such as a curl-to-bash installer.

Mitigation: Install only after trusting the publisher and independently verifying the installer; prefer pinned versions or package installation where possible.

Risk: The skill documents broad local and remote administration flows, including gateways, cron jobs, MCP servers, and webhooks.

Mitigation: Audit any gateway service, scheduled job, webhook, or MCP server before enabling it, and restrict credentials and permissions to the minimum needed.

Risk: The skill references approval bypass behavior such as --yolo or approvals.mode off.

Mitigation: Keep approvals in smart or manual mode for untrusted tasks and avoid approval bypass for commands that can modify files, services, or remote systems.

Risk: Debug reports or logs may contain sensitive local information.

Mitigation: Review debug reports and logs before upload or sharing.

## Reference(s):

- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/)
- [Hermes Agent source repository](https://github.com/NousResearch/hermes-agent)
- [Hermes slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands)
- [Hermes skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)
- [Hermes tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference)
- [Hermes configuration guide](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [Hermes messaging guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)
- [Hermes MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- [Hermes cron guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reference text with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language operational reference; commands may require local review before execution.]

## Skill Version(s):

2.0.1 (source: server release metadata, released 2026-07-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
