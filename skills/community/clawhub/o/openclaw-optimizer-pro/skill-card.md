## Description:

OpenClaw token cost reduction, performance tuning, and security hardening guide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[learsea](https://clawhub.ai/user/learsea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to tune OpenClaw configuration, reduce token and search costs, restore missing capabilities, and review local security settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends broad persistent changes to OpenClaw configuration and SOUL.md policy.

Mitigation: Review each proposed configuration or policy change manually before applying it, especially changes that affect long-term agent behavior.

Risk: The skill may lead users to expose sensitive OpenClaw configuration, account identifiers, API keys, or credentials while auditing settings.

Mitigation: Inspect only needed fields locally and redact tokens or infrastructure details from chat, logs, and shared outputs.

Risk: The skill recommends enabling a full tools profile, which can expand the available tool surface.

Mitigation: Avoid setting tools.profile to full unless the user understands and needs the additional enabled tools.

Risk: The skill includes unpinned global npx or npm install commands.

Mitigation: Verify package source, version, and behavior before running global installation commands.

## Reference(s):

- [Openclaw Optimizer Pro on ClawHub](https://clawhub.ai/learsea/skills/openclaw-optimizer-pro)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [qmd GitHub Repository](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with tables and inline shell, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent OpenClaw policy, configuration, permission, firewall, and global package changes that should be reviewed before use.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
