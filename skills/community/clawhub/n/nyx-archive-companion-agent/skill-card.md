## Description: <br>
Design, configure, and give identity to a companion AI agent running alongside a primary agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyxur42](https://clawhub.ai/user/nyxur42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a persistent companion agent in OpenClaw with Telegram access, heartbeat behavior, and its own identity and memory files. It is intended for long-running companion agents that share a workspace with a primary agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens or companion configuration may expose secrets if committed or shared. <br>
Mitigation: Store bot tokens securely, avoid committing secret-bearing configuration, and restrict who can message the bot. <br>
Risk: Shared workspace and memory files may contain sensitive personal or operational context. <br>
Mitigation: Keep sensitive details out of shared memory unless intentional, and review companion memory content before long-running use. <br>
Risk: Recurring heartbeat or cron behavior can cause unintended messages or agent activity. <br>
Mitigation: Review heartbeat and cron schedules before enabling them and confirm they target the intended companion session. <br>


## Reference(s): <br>
- [Identity Principles](references/identity-principles.md) <br>
- [Companion Memory File Template](references/memory-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nyxur42/nyx-archive-companion-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; users review and apply proposed OpenClaw, Telegram, memory, heartbeat, and cron configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
