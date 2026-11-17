## Description:

OpenClaw overview helps agents quickly understand OpenClaw architecture, core concepts, tool systems, configuration structure, directory layout, and common operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tryxin](https://clawhub.ai/user/tryxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill as a concise OpenClaw reference for architecture, sessions, models, tools, automation, security controls, CLI commands, and documentation locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may propose shell commands, device pairing, cron jobs, or configuration changes after using this overview.

Mitigation: Review any later agent-proposed command, device pairing, cron job, or configuration change before allowing it.

Risk: The skill documents powerful runtime features, including shell execution, messaging, device nodes, cron, memory, and gateway configuration.

Mitigation: Treat the skill as informational and review the resulting operational plan against the user's OpenClaw security model before deployment.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/tryxin/skills/openclaw-overview)
- [Publisher Profile](https://clawhub.ai/user/tryxin)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language overview intended for quick agent reference.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
