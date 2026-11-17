## Description:

Helps agents validate OpenClaw configuration options against local documentation, schema lookup, and online docs before editing OpenClaw config files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leon2023happy](https://clawhub.ai/user/leon2023happy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent is asked to modify OpenClaw configuration files such as openclaw.json or config/*.json. It guides the agent to confirm that each configuration option exists, is used correctly, and matches the expected type before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may introduce invalid OpenClaw settings if configuration validation is skipped or incomplete.

Mitigation: Check local OpenClaw documentation and schema lookup before editing; use the online docs or changelog when local docs do not cover the option.

Risk: The trigger scope covers broad OpenClaw configuration paths.

Mitigation: Limit use to intended OpenClaw configuration files or tighten trigger wording for deployments that only permit specific config paths.

Risk: The skill instructions are currently Chinese-only.

Mitigation: Have operators who rely on the card review the Chinese instructions or provide an approved localized version before broad deployment.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/leon2023happy/skills/openclaw-cfg-safe-edit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
