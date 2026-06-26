## Description: <br>
Configure and operate oh-my-openagent (OmO), an OpenCode plugin that adds multi-agent orchestration, skills, hooks, MCPs, and multi-provider model routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kolyanberoks-23loud](https://clawhub.ai/user/kolyanberoks-23loud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to configure OmO agents, model routing, task categories, hooks, slash commands, provider authentication, and MCP integrations for OpenCode workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures a powerful local OpenCode orchestration plugin with broad coding-agent authority. <br>
Mitigation: Install only from a reviewed version, use a clean branch or disposable workspace, and supervise autonomous loops. <br>
Risk: Hooks, background tasks, MCPs, and mutating tools can change local workflow behavior or execute actions the user did not expect. <br>
Mitigation: Disable or restrict hooks, background tasks, MCPs, and mutating tools that are not needed for the current workflow. <br>
Risk: Provider authentication tokens are stored locally and could be exposed if printed, committed, or shared. <br>
Mitigation: Do not print or share auth.json, and review configuration files before committing or transmitting workspace contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kolyanberoks-23loud/oh-my-openagent) <br>
- [oh-my-openagent Repository](https://github.com/code-yeongyu/oh-my-openagent) <br>
- [Configuration Schema](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json) <br>
- [Agents Reference](references/agents.md) <br>
- [Categories Reference](references/categories.md) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Providers Reference](references/providers.md) <br>
- [Tools Reference](references/tools.md) <br>
- [Hooks Reference](references/hooks.md) <br>
- [MCPs Reference](references/mcps.md) <br>
- [Skills Reference](references/skills.md) <br>
- [Commands Reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local configuration changes, agent settings, hook settings, MCP configuration, and provider authentication guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
