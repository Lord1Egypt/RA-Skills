## Description: <br>
Multi-Topic Board helps an agent track unresolved discussions, update aging days, send reminders after three days without an execution task, and create follow-up task files when appropriate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kzclaw](https://clawhub.ai/user/kzclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to keep multi-session discussions from being forgotten by recording unresolved topics, reminding on stale items, and linking follow-up task files when work is ready to execute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent topic-tracking files and recurring reminder workflows in a workspace. <br>
Mitigation: Require explicit opt-in before first setup, confirm where HEARTBEAT.md, memory/multi-topic.md, and tasks/ will be created, and document how to disable scheduled maintenance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kzclaw/multi-topic-board) <br>
- [Publisher profile](https://clawhub.ai/user/kzclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates workspace files such as HEARTBEAT.md, memory/multi-topic.md, and tasks/*.md when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); 1.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
