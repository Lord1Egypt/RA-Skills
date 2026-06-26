## Description: <br>
Proactive daily planning assistant that helps organize the user's day, track tasks, and provide motivation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akshaymemane](https://clawhub.ai/user/akshaymemane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and OpenClaw users use this skill to generate time-of-day planning prompts, check progress, receive motivation, and prepare evening reviews from local templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Planning history may be retained in local OpenClaw memory files. <br>
Mitigation: Review storage paths in config.json and periodically delete old files under ~/.openclaw/workspace/memory if you do not want planning history retained. <br>
Risk: Suggested cron or HEARTBEAT integration can run the planner unattended. <br>
Mitigation: Add scheduled execution only when unattended daily runs are intended, and review the configured schedule before enabling it. <br>
Risk: Notification settings may route planning reminders through configured channels. <br>
Mitigation: Review config.json notification settings before installation and disable or change channels that do not match the user's privacy expectations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/akshaymemane/proactive-daily-planner) <br>
- [Publisher profile](https://clawhub.ai/user/akshaymemane) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text and Markdown planning/review templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily plans to configured local OpenClaw memory paths when run.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
