## Description: <br>
Persistent reminder system that keeps bugging you until you confirm completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madebydia](https://clawhub.ai/user/madebydia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up recurring reminders that continue through cron and heartbeat checks until the task is confirmed. It is intended for daily habits, ignored tasks, and follow-up workflows that need configurable nag windows, escalation, and natural-language confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep producing reminder nags after the user no longer wants them. <br>
Mitigation: Review reminder schedules before enabling the skill, and remove the cron job plus nag-config.json and memory/nag-state.json when reminders are no longer wanted. <br>
Risk: Broad confirmation patterns or unintended reminder entries could track tasks the user did not mean to monitor. <br>
Mitigation: Review each reminder's schedule, nag window, and confirmation patterns before use. <br>


## Reference(s): <br>
- [Nag Config Examples](references/config-examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/madebydia/nag) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace-local reminder configuration, state-file guidance, cron setup guidance, and a HEARTBEAT.md nag check block.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
