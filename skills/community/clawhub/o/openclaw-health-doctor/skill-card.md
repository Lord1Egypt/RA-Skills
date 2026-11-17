## Description:

OpenClaw Doctor checks OpenClaw configuration, model connectivity, cron tasks, memory files, and installed skills, then reports a health score and repair suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l6366616-lang](https://clawhub.ai/user/l6366616-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to diagnose an OpenClaw installation, review local configuration and service health, and identify concrete repair steps before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostics may expose sensitive configuration, credential status, cron output, or memory/workspace file contents.

Mitigation: Show reports only to the system owner or administrator, redact secrets and credential values, and apply stricter allowlisting for openclaw.json, cron output, MEMORY.md, TOOLS.md, and API-key checks.

Risk: Broad automatic activation may inspect local OpenClaw state before the user expects it.

Mitigation: Ask for explicit confirmation before reading sensitive files or running local status and cron checks.

Risk: Repair suggestions or health scores may be incomplete or misleading if local commands fail or files are stale.

Mitigation: Present the checked source or command with each finding and require user review before applying any configuration changes.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw Doctor on ClawHub](https://clawhub.ai/l6366616-lang/skills/openclaw-health-doctor)
- [Publisher profile](https://clawhub.ai/user/l6366616-lang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health report with status bullets, a numeric health score, and repair suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should redact sensitive values and should not modify configuration unless the user explicitly requests changes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
