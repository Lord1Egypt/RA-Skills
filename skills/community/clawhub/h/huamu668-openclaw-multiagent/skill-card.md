## Description: <br>
Configure multi-agent TG group system with shared Workspace + MemOS memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huamu668](https://clawhub.ai/user/huamu668) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure multiple Telegram bots as specialized agents in a shared OpenClaw workspace with shared MemOS memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and OpenClaw configuration files can expose sensitive access if shared in chats or workspace files. <br>
Mitigation: Use dedicated bots, keep tokens out of shared conversations and files, and restrict access to ~/.openclaw/openclaw.json. <br>
Risk: Multiple bots in a Telegram group may read group messages when privacy is disabled. <br>
Mitigation: Use Telegram group allowlists, inform group members that bots may read messages, and avoid sending secrets in the configured group. <br>
Risk: Shared workspace and MemOS memory can expose context across agents. <br>
Mitigation: Deploy only in trusted groups and keep sensitive or unrelated data out of the shared workspace and memory pool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huamu668/huamu668-openclaw-multiagent) <br>
- [OpenClaw agent creation guide](https://github.com/bozhouDev/openclaw_agent_create_prompt) <br>
- [Telegram raw data bot](https://t.me/raw_data_bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps for Telegram bot accounts, shared workspace files, OpenClaw agent bindings, and validation checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
