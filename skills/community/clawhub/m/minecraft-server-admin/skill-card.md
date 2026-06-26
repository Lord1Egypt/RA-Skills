## Description: <br>
Execute Minecraft Java Edition admin commands through the RCON remote console for player moderation, whitelist management, item and state commands, world rules, broadcast messages, and recent log review on servers you control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[en1r0py1865](https://clawhub.ai/user/en1r0py1865) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External server administrators and developers use this skill to manage Minecraft Java Edition servers they control through RCON, including moderation, world state changes, broadcasts, and recent log review. It is intended for in-game administration, not server lifecycle management, backups, or plugin installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RCON credentials provide full administrator access to the target Minecraft server. <br>
Mitigation: Install only for servers you control, keep MC_RCON_PASSWORD secret, and restrict RCON network exposure. <br>
Risk: Destructive or privilege-changing commands can ban users, grant operator privileges, modify large world areas, stop the server, or pause auto-save. <br>
Mitigation: Review every generated command before execution and require confirmation for high-impact actions such as ban, op, fill, kill, stop, and save-off. <br>
Risk: Log analysis and audit memory can expose or retain player activity, chat, command history, and administrative actions. <br>
Mitigation: Limit log access to necessary files and handle generated summaries and audit entries as server administration records. <br>


## Reference(s): <br>
- [Vanilla Command Reference](references/commands.md) <br>
- [Minecraft Server Log Patterns](references/log-patterns.md) <br>
- [Project homepage](https://github.com/en1r0py1865/minecraft-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON log summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute RCON commands against a configured Minecraft server and may summarize recent server logs when MC_SERVER_LOG is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
