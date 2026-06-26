## Description: <br>
Sets up a structured Obsidian vault for persistent agent memory, daily journals, project documentation, knowledge capture, and OpenClaw/Discord workspace integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catteres](https://clawhub.ai/user/catteres) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize and maintain a local memory vault for OpenClaw agents, including brain files, journals, project notes, learning logs, semantic search setup, and Discord workspace configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic long-term logging can capture sensitive conversations, secrets, or private messages. <br>
Mitigation: Keep command confirmations on, avoid logging secrets or private messages, and review memory files before syncing or sharing them. <br>
Risk: The documented Discord/OpenClaw full-access configuration can connect an agent to messaging channels while disabling command confirmations and sandboxing. <br>
Mitigation: Use sandboxing, keep command confirmations enabled, restrict allowlists, and reserve full-access settings for isolated trusted machines. <br>
Risk: Scheduled memory sync can overwrite or propagate persistent memory files unexpectedly. <br>
Mitigation: Test cron or sync behavior with backups and a dry run before enabling scheduled updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/catteres/obsidian-memory-system) <br>
- [Brain Files Reference](artifact/references/brain-files.md) <br>
- [Discord Workspace Setup](artifact/references/discord-setup.md) <br>
- [Self-Improvement Logging Format](artifact/references/logging-format.md) <br>
- [Memory Management Rules](artifact/references/memory-rules.md) <br>
- [OpenClaw Configuration](artifact/references/openclaw-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON5 configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local vault setup steps, file templates, symlink guidance, memory workflow instructions, and OpenClaw/Discord configuration examples.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
