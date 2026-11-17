## Description:

Pi Coding Agent is an extensible terminal programming assistant for AI-assisted programming with multiple model providers, TypeScript extensions, Skills, Prompt Templates, Themes, and Pi Packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, and operate Pi Coding Agent for terminal-based AI programming workflows, including model selection, session management, SDK/RPC integration, extensions, skills, prompts, themes, and package distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pi can run shell commands, use provider credentials, and store authentication material such as auth.json when configured.

Mitigation: Audit commands before following them, protect API keys and auth.json, and use controls such as --no-tools, --no-builtin-tools, or PI_OFFLINE when tighter execution boundaries are needed.

Risk: Pi Packages, Extensions, and Skills can change agent behavior and may have broad local system access.

Mitigation: Install only trusted packages or extensions, audit source before installation, and disable resource loading with --no-extensions or --no-skills when reviewing untrusted projects.

Risk: Session content and the /share workflow can expose sensitive context if reviewed carelessly.

Mitigation: Review session contents before sharing or exporting, remove secrets from prompts and files, and avoid sharing sessions that include credentials or private data.

Risk: Startup network checks or telemetry can be undesirable in restricted environments.

Mitigation: Use PI_TELEMETRY=0, PI_OFFLINE=1, and PI_SKIP_VERSION_CHECK=1 when operating under stricter privacy or network controls.

## Reference(s):

- [Pi Coding Agent Skill](SKILL.md)
- [Pi Documentation](https://pi.dev/docs/latest)
- [Pi Homepage](https://pi.dev)
- [Agent Skills Standard](https://agentskills.io)
- [Pi CLI Reference](references/cli.md)
- [Pi Configuration Reference](references/config.md)
- [Pi Provider Authentication](references/providers.md)
- [Pi Custom Models and Providers](references/models.md)
- [Pi SDK Integration](references/sdk.md)
- [Pi RPC Mode](references/rpc.md)
- [Pi Extensions](references/extensions.md)
- [Pi Skills Reference](references/skills.md)
- [Pi Packages Reference](references/packages.md)
- [Pi Session Management](references/sessions.md)
- [Pi Compaction and Session Format](references/session-format.md)
- [Pi Keyboard Shortcuts](references/shortcuts.md)
- [Pi TUI Component System](references/tui.md)
- [Pi TUI Themes](references/themes.md)
- [@earendil-works/pi-agent-core](references/agent-core.md)
- [@earendil-works/pi-ai](references/ai.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and TypeScript/JSON code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill output for an agent; no executable payloads are shipped in the skill artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
