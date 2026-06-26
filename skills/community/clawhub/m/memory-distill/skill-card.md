## Description: <br>
Extracts key information from conversations, condenses long dialogues into concise summaries, stores classified memory files, and supports scheduled cleanup through Cron or HEARTBEAT triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to distill active conversation context into structured memory files, daily summaries, task lists, and longer-term notes before context becomes too large or is reset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation details may be persisted into local memory files, including sensitive temporary information. <br>
Mitigation: Configure or instruct the agent not to store verification codes, login links, secrets, personal contact details, or other short-lived sensitive data. <br>
Risk: Scheduled Cron or HEARTBEAT automation may run distillation without a fresh human review. <br>
Mitigation: Review the skill before enabling automation and keep automatic cleanup or reset behavior disabled unless the retention policy is understood. <br>


## Reference(s): <br>
- [Configuration schema](references/distill-config.json) <br>
- [ClawHub skill page](https://clawhub.ai/systiger/memory-distill) <br>
- [Publisher profile](https://clawhub.ai/user/systiger) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries, structured memory file entries, JSON Cron configuration examples, and short command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update MEMORY.md, USER.md, and dated memory files when the agent applies the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
