## Description:

OpenClaw setup and configuration service that helps users install, configure, optimize, and customize the OpenClaw AI assistant for individual or enterprise deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lover876](https://clawhub.ai/user/lover876)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and small businesses use this skill to install OpenClaw, create configuration files, connect Telegram, and prepare an OpenClaw assistant environment for personal or enterprise use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run high-impact installation and configuration steps on a host.

Mitigation: Inspect the scripts first, run them only on a host you control, and prefer a local or pinned installation path.

Risk: Installation may require elevated access and persistent root credentials.

Mitigation: Avoid sharing persistent root credentials; use temporary, owner-controlled access and revoke it after installation.

Risk: Telegram bot tokens are entered interactively and written into configuration files.

Mitigation: Store tokens with owner-only file permissions or a secrets manager, and rotate exposed tokens.

Risk: The generated gateway configuration binds the server host to 0.0.0.0.

Mitigation: Change the gateway host to 127.0.0.1 unless remote access is intentionally protected by network controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lover876/skills/jarvis-setup-service)
- [Artifact README](artifact/README.md)
- [OpenClaw Configuration Template](artifact/templates/config.yaml)
- [ClawHub Marketplace](https://clawhub.ai)
- [SkillHub Marketplace](https://skillhub.tencent.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash snippets, YAML configuration, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, environment check, OpenClaw configuration, and Telegram setup workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
