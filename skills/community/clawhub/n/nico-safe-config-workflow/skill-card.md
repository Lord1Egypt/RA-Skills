## Description:

Guides agents through safer OpenClaw configuration changes by checking documentation, confirming changes, running repair commands, comparing backups, recording lessons, and validating Gateway status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoxia](https://clawhub.ai/user/nicoxia)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill when modifying OpenClaw configuration, especially Gateway, channel, model, session, or authentication settings in ~/.openclaw/openclaw.json. It provides a confirmation-first workflow with repair, diff review, hot-reload validation, and troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can modify sensitive OpenClaw configuration, including settings related to channels, models, sessions, and authentication.

Mitigation: Require explicit user confirmation before changes, review proposed edits, and validate the final Gateway status after repair or restart.

Risk: Repair and troubleshooting output can contain credentials, tokens, raw diffs, logs, endpoint secrets, or authentication values.

Mitigation: Filter user-facing output and avoid persisting secrets or raw sensitive diagnostics in MEMORY.md or other records.

Risk: Automated doctor checks may not catch every operational problem, such as a syntactically valid but unusable port.

Mitigation: Compare the generated backup diff, check OpenClaw logs when Gateway fails, and manually validate critical configuration values against documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicoxia/skills/nico-safe-config-workflow)
- [OpenClaw configuration documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration)
- [OpenClaw doctor documentation](https://docs.openclaw.ai/zh-CN/cli/doctor)
- [OpenClaw Gateway manual](https://docs.openclaw.ai/zh-CN/gateway/index.md)
- [OpenClaw Gateway troubleshooting](https://docs.openclaw.ai/zh-CN/gateway/troubleshooting)
- [OpenClaw FAQ](https://docs.openclaw.ai/zh-CN/help/faq.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese/zh-CN focused user-facing workflow text; expects agent review before configuration edits.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
