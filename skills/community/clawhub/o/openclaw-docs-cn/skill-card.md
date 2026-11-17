## Description:

OpenClaw Docs helps agents answer Chinese-language OpenClaw questions about installation, configuration, CLI commands, channel setup, cron jobs, skill development, and troubleshooting with concise examples and templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z13777869196](https://clawhub.ai/user/z13777869196)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators working with OpenClaw use this skill to answer installation, CLI, channel configuration, cron automation, skill development, and troubleshooting questions with concise commands and configuration templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup advice includes global mutable installation and enabling a persistent daemon without enough scoping or removal guidance.

Mitigation: Review installation commands before use; prefer a pinned OpenClaw version from a verified source and confirm daemon stop, disable, and uninstall steps before enabling it.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw CLI Reference](https://docs.openclaw.ai/cli/index.md)
- [OpenClaw Channel Configuration](https://docs.openclaw.ai/channels/index.md)
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs.md)
- [ClawHub Skill Page](https://clawhub.ai/z13777869196/skills/openclaw-docs-cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholder credentials and concise examples rather than real secrets or exhaustive command listings.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
