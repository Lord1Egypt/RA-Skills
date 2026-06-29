## Description: <br>
Use Pi Coding Agent (@earendil-works/pi-coding-agent) for AI-assisted programming. Pi is an extensible terminal programming assistant supporting multiple model providers, TypeScript extensions, Skills, Prompt Templates, Themes, and Pi Packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate Pi Coding Agent for AI-assisted programming, including installation, configuration, model and provider selection, extension development, session management, and SDK or RPC integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model provider credentials and OAuth tokens may be exposed if configured or shared carelessly. <br>
Mitigation: Use trusted providers only, protect API keys and OAuth tokens, prefer environment variables or secure credential storage, and avoid pasting secrets into prompts or shared sessions. <br>
Risk: Saved or shared sessions can contain sensitive work context, and the share workflow uploads content to GitHub Gist. <br>
Mitigation: Use temporary sessions for sensitive work, review session content before sharing, and avoid using the share command for confidential data. <br>
Risk: Pi packages and extensions can affect local files or execute system-level behavior. <br>
Mitigation: Install packages and extensions only from trusted sources, audit source before use, and disable extensions, telemetry, or startup networking when the environment requires stricter controls. <br>


## Reference(s): <br>
- [Pi Coding Agent ClawHub listing](https://clawhub.ai/openlark/pi-coding-agent) <br>
- [Pi homepage](https://pi.dev) <br>
- [Pi documentation](https://pi.dev/docs/latest) <br>
- [Agent Skills standard](https://agentskills.io) <br>
- [Runtime API](references/agent-core.md) <br>
- [LLM API](references/ai.md) <br>
- [CLI reference](references/cli.md) <br>
- [Configuration reference](references/config.md) <br>
- [Provider authentication](references/providers.md) <br>
- [Extension API](references/extensions.md) <br>
- [SDK integration](references/sdk.md) <br>
- [RPC mode](references/rpc.md) <br>
- [Session management](references/sessions.md) <br>
- [Session format and compaction](references/session-format.md) <br>
- [Pi packages](references/packages.md) <br>
- [Pi skills](references/skills.md) <br>
- [Keyboard shortcuts](references/shortcuts.md) <br>
- [TUI components](references/tui.md) <br>
- [Themes](references/themes.md) <br>
- [Custom models and providers](references/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code examples, shell commands, JSON snippets, TypeScript snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent output may include provider requests, file or shell command guidance, session artifacts, and package or extension instructions depending on the user's task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
