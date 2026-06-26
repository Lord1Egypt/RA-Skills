## Description: <br>
Creates OpenClaw cron jobs for goal-driven reminders that prompt an agent to act and then delete the cron job when complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to schedule delayed or recurring goal reminders for an OpenClaw agent, such as follow-ups that should continue until the objective is complete and the cron job is removed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local OpenClaw gateway token and can create persistent recurring jobs. <br>
Mitigation: Install only when this token use is acceptable, retain returned job IDs, and remove jobs promptly after completion. <br>
Risk: Incorrect AGENT_SESSION_KEY or FEISHU_GROUP_ID values can schedule reminders for the wrong agent or group. <br>
Mitigation: Verify both values before creating a goal task. <br>
Risk: Untrusted task text may be passed into shell-generated JSON. <br>
Mitigation: Avoid untrusted task descriptions until input handling safely encodes all values. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/axelhu/goal-task) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with shell command examples and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates OpenClaw cron jobs and returns job identifiers that must be retained for cleanup.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
