## Description: <br>
Monitors the freshness of routine checks such as email, calendar, weather, and todo status, raises threshold alerts, and helps generate heartbeat health reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangkai258](https://clawhub.ai/user/yangkai258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to track when recurring checks last ran, detect stale email, calendar, weather, or todo checks, and produce a concise monitoring health report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local heartbeat history for email, calendar, weather, and todo checks can expose activity patterns or operational freshness. <br>
Mitigation: Decide whether local heartbeat history is acceptable before installation and keep the state file limited to the checks the operator intends to monitor. <br>
Risk: Cron reminders or automatic repair could trigger sensitive email or calendar checks unexpectedly. <br>
Mitigation: Set clear thresholds and require confirmation before sensitive checks or repair actions are triggered. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yangkai258/openclaw-heartbeat-monitor) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local heartbeat state, threshold settings, reminders, and repair prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
