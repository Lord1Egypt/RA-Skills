## Description: <br>
Autonomous task tracking with retry loops, proactive updates, completion reporting, and heartbeat checks for stale tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal assistant operators use this skill to register owned tasks, persist task state, retry blocked work on a schedule, and close the loop with the person or group that initiated the task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad ongoing authority to store task details, retry work, and send WhatsApp status messages. <br>
Mitigation: Use only where persistent task ownership is desired, narrow the trigger phrases, and require confirmation for high-impact tasks and retries. <br>
Risk: Task records and memory updates may retain sensitive task context. <br>
Mitigation: Define retention, redaction, deletion, and sensitivity limits for task details before deployment. <br>
Risk: The artifact sources a local .context shell file during setup. <br>
Mitigation: Remove or constrain local context sourcing so only expected, non-sensitive configuration values are loaded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/pa-ownership) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON task records, Markdown notes, short status messages, and procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists task status changes and retry metadata; may produce completion, blocked, or failure notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
