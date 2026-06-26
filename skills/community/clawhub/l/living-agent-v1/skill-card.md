## Description: <br>
Helps an OpenClaw agent combine practical user support with autonomous reflection, exploration, memory updates, and scheduled background thinking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Linsongrong](https://clawhub.ai/user/Linsongrong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure a persistent agent posture that records important context, schedules reflection tasks, explores topics during idle periods, and reports notable findings back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous background tasks can read prior conversations, update cron jobs, and store inferred user context. <br>
Mitigation: Review each cron job before enabling it, limit readable files and exploration topics, and enable the skill only when persistent autonomous behavior is intended. <br>
Risk: The skill can message users and includes weak consent boundaries around notification behavior. <br>
Mitigation: Configure the target user ID deliberately and disable or remove messaging behavior unless the user explicitly wants those notifications. <br>
Risk: Stored state, queue, and memory files may retain sensitive or inaccurate inferred information over time. <br>
Mitigation: Regularly inspect or delete thinking-state.json, thinking-queue.json, and memory/thoughts files, and correct retained information before relying on it. <br>


## Reference(s): <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Setup guide](artifact/SETTING.md) <br>
- [ClawHub skill page](https://clawhub.ai/Linsongrong/living-agent-v1) <br>
- [Heartbeat-Like-A-Man design reference](https://github.com/loryoncloud/Heartbeat-Like-A-Man) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw cron jobs and workspace memory files when enabled.] <br>

## Skill Version(s): <br>
1.1.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
