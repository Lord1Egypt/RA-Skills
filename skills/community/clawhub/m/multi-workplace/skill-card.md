## Description: <br>
Manage multiple project workplaces with per-workspace agents, isolated memory, IDE context sync, and inter-agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dickwu](https://clawhub.ai/user/dickwu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize, switch, scan, link, and synchronize project workplaces while coordinating role-based agents across related codebases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update project-management files in target project directories and the OpenClaw workplace registry. <br>
Mitigation: Confirm the target path before running workplace init, scan, switch, link, import, or recursive parent-folder operations. <br>
Risk: IDE synchronization can modify agent-facing context files such as CLAUDE.md, .cursor/rules/workplace.mdc, and opencode.jsonc. <br>
Mitigation: Review generated IDE context before relying on it, especially when a project already has local instructions or coding-agent configuration. <br>
Risk: Kernel and agent workflows may start long-running local coordination processes and update .workplace/process-status.json. <br>
Mitigation: Use the workplace status and agent stop commands to monitor or stop running agents and file-watcher activity. <br>


## Reference(s): <br>
- [Multi Workplace README](README.md) <br>
- [Command Reference](references/commands.md) <br>
- [Init Guide](references/init-guide.md) <br>
- [Agent System](references/agent-system.md) <br>
- [Chat Protocol](references/chat-protocol.md) <br>
- [IDE Sync Guide](references/ide-sync.md) <br>
- [Telegram UI](references/telegram-ui.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenCode Config Schema](https://opencode.ai/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local files or configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .workplace/, ~/.openclaw/workspace/.workplaces/, CLAUDE.md, .cursor/rules/workplace.mdc, opencode.jsonc, and deployment templates.] <br>

## Skill Version(s): <br>
0.4.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
