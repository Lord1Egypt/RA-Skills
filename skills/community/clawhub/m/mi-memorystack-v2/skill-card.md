## Description: <br>
Mi-MemoryStack helps an agent retrieve and save user-scoped conversation memories for historical context, preferences, identity details, and multi-turn continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yifan66www](https://clawhub.ai/user/Yifan66www) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add persistent memory to OpenClaw-style agent conversations by retrieving prior context before a reply and queueing new user and assistant turns for later recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently logs user messages and assistant replies linked to user IDs. <br>
Mitigation: Install only where users expect persistent memory, and add consent, skip controls, and deletion procedures for sensitive conversations. <br>
Risk: The install flow edits global agent instructions and relies on a background daemon. <br>
Mitigation: Review install.sh before running it, document how to stop the daemon, and confirm the modified instructions match the intended memory policy. <br>
Risk: Conversation data can be sent to an unspecified API endpoint. <br>
Mitigation: Confirm the API endpoint and token handling before use, and restrict deployment to environments where that data flow is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yifan66www/mi-memorystack-v2) <br>
- [Skill usage guide](artifact/SKILL.md) <br>
- [Installation note](artifact/安装教程.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user ID and a configured memory API before search or save commands can return useful results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
