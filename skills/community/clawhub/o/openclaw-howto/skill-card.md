## Description:

Provides guidance on OpenClaw features, configuration, CLI commands, troubleshooting, and best practices, with local reference use and optional web search workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparkmilkway](https://clawhub.ai/user/sparkmilkway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to answer OpenClaw usage questions, configure agents and cron jobs, manage skills, and troubleshoot CLI or environment issues. It supports local CLI/reference workflows and optional web search when current external information is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist and automatically reuse user-provided web search tool call formats.

Mitigation: Use local mode unless web search is explicitly needed, and periodically inspect or delete memory/openclaw-env-info.md and memory/openclaw-knowledge.

Risk: User-provided queries, tool call formats, or error messages may include secrets or internal URLs.

Mitigation: Do not place secrets, private URLs, or sensitive operational details in search queries, cached tool configuration, or troubleshooting messages.

Risk: Generated OpenClaw shell commands and configuration examples can alter local agents, cron jobs, skills, gateway state, or workspace files.

Mitigation: Review commands before execution, prefer help or dry-run modes when available, and apply changes in a controlled workspace.

## Reference(s):

- [OpenClaw HowTo ClawHub release](https://clawhub.ai/sparkmilkway/skills/openclaw-howto)
- [OpenClaw Best Practices Guide](references/best-practices.md)
- [OpenClaw Command Cheatsheet](references/commands-cheatsheet.md)
- [OpenClaw Search Strategy Guide](references/search-strategies.md)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and configuration examples should be reviewed before execution.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
