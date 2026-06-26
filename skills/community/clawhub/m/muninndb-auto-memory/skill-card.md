## Description: <br>
Automatically uses MuninnDB as a proactive memory layer via MCP so an agent can recall prior session context without manual triggering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitsonwheels](https://clawhub.ai/user/bitsonwheels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect a MuninnDB vault as persistent cross-session memory, recall prior context, save important decisions or preferences, and optionally maintain periodic local context snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist cross-session memory, which may retain sensitive, regulated, or outdated context if used carelessly. <br>
Mitigation: Avoid saving secrets or regulated data, and review or prune the MuninnDB vault periodically. <br>
Risk: The MuninnDB API key is a sensitive local credential. <br>
Mitigation: Protect ~/.muninn/openclaw.key with restrictive permissions and only install the skill when persistent memory is intended. <br>
Risk: The optional 30-minute cron snapshot can store local workspace and recent-session metadata in the vault. <br>
Mitigation: Enable the snapshot only when that storage behavior is acceptable, and pause or remove the cron job when it is no longer needed. <br>


## Reference(s): <br>
- [Setup Companion](references/setup-companion.md) <br>
- [ClawHub skill page](https://clawhub.ai/bitsonwheels/muninndb-auto-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell, YAML, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MCP tool usage guidance, REST API fallback commands, and optional cron snapshot setup instructions.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
