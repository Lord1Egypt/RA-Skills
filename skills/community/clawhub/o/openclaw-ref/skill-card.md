## Description:

OpenClaw reference guidance for configuration, CLI operations, troubleshooting, and model management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[astralwaveorg](https://clawhub.ai/user/astralwaveorg)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill as a Chinese-language OpenClaw operations manual when editing openclaw.json, running CLI commands, configuring providers and channels, or troubleshooting deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may include reset, uninstall, force, shell execution, node execution, plugin, hook, webhook, credential, camera, screen, or location operations with administrative impact.

Mitigation: Review and explicitly approve these operations before use; prefer allowlists, pairing, sandboxing, audit logs, backups, gateway tokens, and environment-variable secrets.

Risk: Configuration guidance can affect OpenClaw gateway access, channel routing, automation behavior, and credential handling.

Mitigation: Back up configuration before changes, validate field paths and types, avoid hard-coded secrets, and test changes with the documented diagnostic workflow.

## Reference(s):

- [Openclaw Ref on ClawHub](https://clawhub.ai/astralwaveorg/skills/openclaw-ref)
- [OpenClaw Configuration Fields Reference](artifact/core/config-fields.md)
- [OpenClaw CLI Reference](artifact/core/cli.md)
- [OpenClaw API and Security Reference](artifact/reference/api-security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; examples may include administrative OpenClaw commands that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
