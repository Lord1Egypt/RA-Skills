## Description:

OpenClaw 记忆系统 helps agents manage multimodal memory, project/agent/user isolation, and natural-language memory correction with version history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nick-liu1989](https://clawhub.ai/user/nick-liu1989)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to add persistent multimodal memory, scoped project/agent/user namespaces, and natural-language memory correction workflows to agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release claims broad persistent memory, sharing, import/export, deletion, cleanup, and Feishu webhook behavior without clearly explaining privacy, retention, consent, or data egress.

Mitigation: Review privacy and retention expectations before installation, use a disposable workspace for evaluation, and keep webhook configuration disabled until data-flow behavior is understood.

Risk: The package is under-scoped and does not ship the advertised implementation files for the documented memory modules.

Mitigation: Verify installed files and runnable tests before relying on the skill for production memory workflows.

Risk: The install script creates memory directories and copies configuration into the OpenClaw workspace.

Mitigation: Set OPENCLAW_WORKSPACE to an intended test workspace and review filesystem changes before running the installer in a shared or production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nick-liu1989/skills/openclaw-memory-system)
- [README.md](artifact/README.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [RELEASE.md](artifact/RELEASE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with JavaScript examples, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The package advertises persistent memory behavior, optional Feishu webhook integration, and workspace configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
